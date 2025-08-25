"""
GrowMaster Pro - Basic Notification System
Windows desktop notifications, task reminders, and alert management
"""

import logging
import platform
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NotificationType(Enum):
    """Types of notifications"""
    TASK_REMINDER = "task_reminder"
    TASK_OVERDUE = "task_overdue"
    SYSTEM_ALERT = "system_alert"
    GROWTH_MILESTONE = "growth_milestone"
    RESOURCE_ALERT = "resource_alert"
    HARVEST_READY = "harvest_ready"

@dataclass
class NotificationPreferences:
    """User notification preferences"""
    enabled: bool = True
    task_reminders: bool = True
    overdue_alerts: bool = True
    system_notifications: bool = True
    growth_milestones: bool = True
    sound_enabled: bool = True
    reminder_advance_minutes: int = 30
    quiet_hours_start: int = 22  # 10 PM
    quiet_hours_end: int = 7     # 7 AM

class BasicNotificationSystem:
    """Basic notification system for desktop alerts and task reminders"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.preferences = self._load_preferences()
        self.notification_queue = []
        self.active_reminders = {}
        self.system_platform = platform.system()
        self.running = False
        self.notification_thread = None
        
        # Initialize platform-specific notification system
        self._initialize_notification_backend()
        
    def _load_preferences(self) -> NotificationPreferences:
        """Load user notification preferences from database"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT setting_key, setting_value FROM user_settings 
                    WHERE setting_key LIKE 'notification_%'
                """)
                
                settings = dict(cursor.fetchall())
                
                return NotificationPreferences(
                    enabled=settings.get('notification_enabled', 'true').lower() == 'true',
                    task_reminders=settings.get('notification_task_reminders', 'true').lower() == 'true',
                    overdue_alerts=settings.get('notification_overdue_alerts', 'true').lower() == 'true',
                    system_notifications=settings.get('notification_system', 'true').lower() == 'true',
                    growth_milestones=settings.get('notification_growth', 'true').lower() == 'true',
                    sound_enabled=settings.get('notification_sound', 'true').lower() == 'true',
                    reminder_advance_minutes=int(settings.get('notification_advance', '30')),
                    quiet_hours_start=int(settings.get('notification_quiet_start', '22')),
                    quiet_hours_end=int(settings.get('notification_quiet_end', '7'))
                )
                
        except Exception as e:
            logger.error(f"Error loading notification preferences: {e}")
            return NotificationPreferences()
    
    def _initialize_notification_backend(self):
        """Initialize platform-specific notification backend"""
        if self.system_platform == "Windows":
            try:
                import win10toast
                self.toaster = win10toast.ToastNotifier()
                self.backend = "win10toast"
                logger.info("Initialized Windows 10 toast notifications")
            except ImportError:
                logger.warning("win10toast not available, falling back to basic notifications")
                self.backend = "basic"
        else:
            # For Linux/macOS, we'll use a simple approach
            self.backend = "basic"
            logger.info(f"Using basic notifications for {self.system_platform}")
    
    def start_notification_service(self):
        """Start the notification service background thread"""
        if self.running:
            return
        
        self.running = True
        self.notification_thread = threading.Thread(target=self._notification_worker, daemon=True)
        self.notification_thread.start()
        logger.info("Notification service started")
    
    def stop_notification_service(self):
        """Stop the notification service"""
        self.running = False
        if self.notification_thread:
            self.notification_thread.join(timeout=5)
        logger.info("Notification service stopped")
    
    def _notification_worker(self):
        """Background worker for processing notifications"""
        while self.running:
            try:
                # Check for task reminders
                self._check_task_reminders()
                
                # Check for overdue tasks
                self._check_overdue_tasks()
                
                # Check for growth milestones
                self._check_growth_milestones()
                
                # Check for resource alerts
                self._check_resource_alerts()
                
                # Process notification queue
                self._process_notification_queue()
                
                # Sleep for 1 minute before next check
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Error in notification worker: {e}")
                time.sleep(60)  # Continue after error
    
    def _check_task_reminders(self):
        """Check for tasks that need reminders"""
        if not self.preferences.task_reminders:
            return
        
        try:
            # Calculate reminder time window
            now = datetime.now()
            reminder_time = now + timedelta(minutes=self.preferences.reminder_advance_minutes)
            
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT t.id, t.title, t.due_date, t.priority, t.task_type,
                           g.name as garden_name
                    FROM tasks t
                    JOIN gardens g ON t.garden_id = g.id
                    WHERE t.is_completed = 0 
                    AND datetime(t.due_date) <= datetime(?)
                    AND datetime(t.due_date) > datetime(?)
                    AND t.id NOT IN (SELECT task_id FROM notification_history 
                                   WHERE notification_type = 'task_reminder' 
                                   AND sent_date > datetime('now', '-1 day'))
                """, (reminder_time.isoformat(), now.isoformat()))
                
                for row in cursor.fetchall():
                    task_id, title, due_date, priority, task_type, garden_name = row
                    
                    self._queue_notification({
                        'type': NotificationType.TASK_REMINDER,
                        'priority': NotificationPriority.MEDIUM if priority == 'High' else NotificationPriority.LOW,
                        'title': f"Task Reminder: {garden_name}",
                        'message': f"{title} is due at {due_date}",
                        'task_id': task_id,
                        'garden_name': garden_name
                    })
                    
        except Exception as e:
            logger.error(f"Error checking task reminders: {e}")
    
    def _check_overdue_tasks(self):
        """Check for overdue tasks"""
        if not self.preferences.overdue_alerts:
            return
        
        try:
            now = datetime.now()
            
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT t.id, t.title, t.due_date, t.priority, 
                           g.name as garden_name,
                           (julianday('now') - julianday(t.due_date)) * 24 as hours_overdue
                    FROM tasks t
                    JOIN gardens g ON t.garden_id = g.id
                    WHERE t.is_completed = 0 
                    AND datetime(t.due_date) < datetime('now')
                    AND t.id NOT IN (SELECT task_id FROM notification_history 
                                   WHERE notification_type = 'task_overdue' 
                                   AND sent_date > datetime('now', '-4 hours'))
                """)
                
                for row in cursor.fetchall():
                    task_id, title, due_date, priority, garden_name, hours_overdue = row
                    
                    # Determine notification priority based on how overdue
                    if hours_overdue < 2:
                        notif_priority = NotificationPriority.MEDIUM
                    elif hours_overdue < 12:
                        notif_priority = NotificationPriority.HIGH
                    else:
                        notif_priority = NotificationPriority.CRITICAL
                    
                    hours_text = f"{int(hours_overdue)} hour(s)" if hours_overdue >= 1 else f"{int(hours_overdue * 60)} minute(s)"
                    
                    self._queue_notification({
                        'type': NotificationType.TASK_OVERDUE,
                        'priority': notif_priority,
                        'title': f"⚠️ Overdue Task: {garden_name}",
                        'message': f"{title} is {hours_text} overdue!",
                        'task_id': task_id,
                        'garden_name': garden_name
                    })
                    
        except Exception as e:
            logger.error(f"Error checking overdue tasks: {e}")
    
    def _check_growth_milestones(self):
        """Check for growth milestones and stage transitions"""
        if not self.preferences.growth_milestones:
            return
        
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT id, name, planted_date, current_stage,
                           (julianday('now') - julianday(planted_date)) as days_since_planting
                    FROM gardens 
                    WHERE is_active = 1
                """)
                
                for row in cursor.fetchall():
                    garden_id, name, planted_date, current_stage, days_since = row
                    
                    # Check for stage transitions
                    expected_stage = self._get_expected_stage(days_since)
                    if expected_stage != current_stage:
                        self._queue_notification({
                            'type': NotificationType.GROWTH_MILESTONE,
                            'priority': NotificationPriority.MEDIUM,
                            'title': f"🌱 Growth Milestone: {name}",
                            'message': f"Ready to transition from {current_stage} to {expected_stage} stage",
                            'garden_id': garden_id,
                            'garden_name': name
                        })
                        
                        # Update garden stage in database
                        conn.execute("""
                            UPDATE gardens 
                            SET current_stage = ?, stage_start_date = datetime('now')
                            WHERE id = ?
                        """, (expected_stage, garden_id))
                        conn.commit()
                        
        except Exception as e:
            logger.error(f"Error checking growth milestones: {e}")
    
    def _get_expected_stage(self, days_since_planting: float) -> str:
        """Determine expected growth stage based on days since planting"""
        if days_since_planting < 7:
            return "germination"
        elif days_since_planting < 21:
            return "seedling"
        elif days_since_planting < 56:
            return "vegetative"
        elif days_since_planting < 112:
            return "flowering"
        else:
            return "harvest"
    
    def _check_resource_alerts(self):
        """Check for resource-related alerts"""
        try:
            # Check for low inventory levels
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT name, current_quantity, minimum_threshold
                    FROM inventory_items 
                    WHERE current_quantity <= minimum_threshold 
                    AND current_quantity > 0
                """)
                
                for row in cursor.fetchall():
                    name, current, threshold = row
                    
                    self._queue_notification({
                        'type': NotificationType.RESOURCE_ALERT,
                        'priority': NotificationPriority.HIGH,
                        'title': "📦 Low Inventory Alert",
                        'message': f"{name} is running low ({current} remaining, threshold: {threshold})",
                        'resource_name': name
                    })
                    
        except Exception as e:
            logger.error(f"Error checking resource alerts: {e}")
    
    def _queue_notification(self, notification: Dict[str, Any]):
        """Add notification to queue for processing"""
        # Check if we're in quiet hours
        if self._is_quiet_hours():
            notification['delayed'] = True
            notification['original_time'] = datetime.now().isoformat()
        
        self.notification_queue.append(notification)
    
    def _is_quiet_hours(self) -> bool:
        """Check if current time is within quiet hours"""
        current_hour = datetime.now().hour
        
        if self.preferences.quiet_hours_start > self.preferences.quiet_hours_end:
            # Quiet hours span midnight (e.g., 22:00 to 07:00)
            return (current_hour >= self.preferences.quiet_hours_start or 
                   current_hour <= self.preferences.quiet_hours_end)
        else:
            # Quiet hours within same day
            return (self.preferences.quiet_hours_start <= current_hour <= 
                   self.preferences.quiet_hours_end)
    
    def _process_notification_queue(self):
        """Process queued notifications"""
        if not self.notification_queue:
            return
        
        # Process up to 5 notifications per cycle to avoid spam
        for _ in range(min(5, len(self.notification_queue))):
            if not self.notification_queue:
                break
                
            notification = self.notification_queue.pop(0)
            
            # Skip delayed notifications during quiet hours
            if notification.get('delayed') and self._is_quiet_hours():
                self.notification_queue.append(notification)  # Re-queue
                continue
            
            self._send_notification(notification)
    
    def _send_notification(self, notification: Dict[str, Any]):
        """Send a single notification using the appropriate backend"""
        if not self.preferences.enabled:
            return
        
        try:
            title = notification['title']
            message = notification['message']
            priority = notification.get('priority', NotificationPriority.MEDIUM)
            
            if self.backend == "win10toast":
                self._send_windows_notification(title, message, priority)
            else:
                self._send_basic_notification(title, message, priority)
            
            # Log notification
            self._log_notification(notification)
            
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
    
    def _send_windows_notification(self, title: str, message: str, priority: NotificationPriority):
        """Send Windows 10 toast notification"""
        try:
            # Determine duration based on priority
            duration = {
                NotificationPriority.LOW: 5,
                NotificationPriority.MEDIUM: 10,
                NotificationPriority.HIGH: 15,
                NotificationPriority.CRITICAL: 20
            }.get(priority, 10)
            
            icon_path = None  # Can add custom icons later
            
            self.toaster.show_toast(
                title=title,
                msg=message,
                icon_path=icon_path,
                duration=duration,
                threaded=True
            )
            
            logger.info(f"Sent Windows notification: {title}")
            
        except Exception as e:
            logger.error(f"Error sending Windows notification: {e}")
            self._send_basic_notification(title, message, priority)
    
    def _send_basic_notification(self, title: str, message: str, priority: NotificationPriority):
        """Send basic notification (fallback method)"""
        try:
            # For basic notifications, we'll just log them
            # In a full implementation, this could use system-specific commands
            priority_symbol = {
                NotificationPriority.LOW: "ℹ️",
                NotificationPriority.MEDIUM: "⚠️",
                NotificationPriority.HIGH: "🚨",
                NotificationPriority.CRITICAL: "🔥"
            }.get(priority, "ℹ️")
            
            logger.info(f"NOTIFICATION {priority_symbol} {title}: {message}")
            
            # On Linux, could use notify-send if available
            if self.system_platform == "Linux":
                try:
                    import subprocess
                    subprocess.run([
                        "notify-send", 
                        "-t", "10000",  # 10 second timeout
                        title, 
                        message
                    ], check=False)
                except (subprocess.SubprocessError, FileNotFoundError):
                    pass  # notify-send not available
                    
        except Exception as e:
            logger.error(f"Error sending basic notification: {e}")
    
    def _log_notification(self, notification: Dict[str, Any]):
        """Log notification to database for history tracking"""
        try:
            with self.db_manager.get_connection() as conn:
                conn.execute("""
                    INSERT INTO notification_history 
                    (notification_type, title, message, priority, task_id, garden_id, sent_date)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    notification['type'].value,
                    notification['title'],
                    notification['message'],
                    notification.get('priority', NotificationPriority.MEDIUM).value,
                    notification.get('task_id'),
                    notification.get('garden_id')
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error logging notification: {e}")
    
    def send_manual_notification(self, title: str, message: str, 
                               priority: NotificationPriority = NotificationPriority.MEDIUM):
        """Send a manual notification immediately"""
        notification = {
            'type': NotificationType.SYSTEM_ALERT,
            'priority': priority,
            'title': title,
            'message': message
        }
        
        self._send_notification(notification)
    
    def update_preferences(self, new_preferences: Dict[str, Any]):
        """Update notification preferences"""
        try:
            with self.db_manager.get_connection() as conn:
                for key, value in new_preferences.items():
                    conn.execute("""
                        INSERT OR REPLACE INTO user_settings (setting_key, setting_value)
                        VALUES (?, ?)
                    """, (f"notification_{key}", str(value).lower() if isinstance(value, bool) else str(value)))
                
                conn.commit()
            
            # Reload preferences
            self.preferences = self._load_preferences()
            logger.info("Notification preferences updated")
            
        except Exception as e:
            logger.error(f"Error updating notification preferences: {e}")
    
    def get_notification_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get notification history for the last N days"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT notification_type, title, message, priority, sent_date
                    FROM notification_history 
                    WHERE sent_date >= datetime('now', '-{} days')
                    ORDER BY sent_date DESC
                """.format(days))
                
                history = []
                for row in cursor.fetchall():
                    history.append({
                        'type': row[0],
                        'title': row[1],
                        'message': row[2],
                        'priority': row[3],
                        'sent_date': row[4]
                    })
                
                return history
                
        except Exception as e:
            logger.error(f"Error getting notification history: {e}")
            return []
    
    def create_notification_tables(self):
        """Create notification-related database tables if they don't exist"""
        try:
            with self.db_manager.get_connection() as conn:
                # Notification history table
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS notification_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        notification_type TEXT NOT NULL,
                        title TEXT NOT NULL,
                        message TEXT NOT NULL,
                        priority TEXT DEFAULT 'medium',
                        task_id INTEGER,
                        garden_id INTEGER,
                        sent_date TEXT NOT NULL,
                        FOREIGN KEY (task_id) REFERENCES tasks (id),
                        FOREIGN KEY (garden_id) REFERENCES gardens (id)
                    )
                """)
                
                # User settings table (if not exists)
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS user_settings (
                        setting_key TEXT PRIMARY KEY,
                        setting_value TEXT NOT NULL,
                        updated_date TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Notification database tables created/verified")
                
        except Exception as e:
            logger.error(f"Error creating notification tables: {e}")
    
    def test_notifications(self):
        """Send test notifications for each priority level"""
        test_notifications = [
            {
                'title': "🧪 Test - Low Priority",
                'message': "This is a low priority test notification",
                'priority': NotificationPriority.LOW
            },
            {
                'title': "🧪 Test - Medium Priority", 
                'message': "This is a medium priority test notification",
                'priority': NotificationPriority.MEDIUM
            },
            {
                'title': "🧪 Test - High Priority",
                'message': "This is a high priority test notification", 
                'priority': NotificationPriority.HIGH
            },
            {
                'title': "🧪 Test - Critical Priority",
                'message': "This is a critical priority test notification",
                'priority': NotificationPriority.CRITICAL
            }
        ]
        
        for notification in test_notifications:
            self.send_manual_notification(
                notification['title'],
                notification['message'],
                notification['priority']
            )
            time.sleep(2)  # Space out test notifications
        
        logger.info("Test notifications sent")
