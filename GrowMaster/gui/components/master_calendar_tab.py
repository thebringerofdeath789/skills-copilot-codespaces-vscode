"""
Master Calendar Tab - Unified calendar view with advanced filtering
Shows all tasks across all gardens in one comprehensive view
"""

import customtkinter as ctk
from datetime import datetime, date, timedelta
import calendar
import logging

from config.themes import themes
from core.database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class MasterCalendarTab:
    """Master calendar with multi-garden task visualization"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        self.current_date = date.today()
        self.db_manager = DatabaseManager()
        self.tasks_data = []
        
        # Configure parent frame
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        self.create_interface()
        self.load_calendar_data()
    
    def create_interface(self):
        """Create calendar interface"""
        # Calendar header with controls
        header_frame = ctk.CTkFrame(self.parent, **themes.get_frame_styles()["card"])
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(2, weight=1)
        
        # Navigation buttons
        prev_btn = ctk.CTkButton(
            header_frame,
            text="←",
            width=40,
            command=self.prev_month,
            **themes.get_button_styles()["secondary"]
        )
        prev_btn.grid(row=0, column=0, padx=10, pady=10)
        
        next_btn = ctk.CTkButton(
            header_frame,
            text="→",
            width=40,
            command=self.next_month,
            **themes.get_button_styles()["secondary"]
        )
        next_btn.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Current month/year
        self.month_label = ctk.CTkLabel(
            header_frame,
            text=self.current_date.strftime("%B %Y"),
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.month_label.grid(row=0, column=2, pady=10)
        
        # View mode buttons
        view_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        view_frame.grid(row=0, column=3, padx=10, pady=10)
        
        month_btn = ctk.CTkButton(
            view_frame,
            text="Month",
            width=60,
            command=lambda: self.set_view_mode("month"),
            **themes.get_button_styles()["primary"]
        )
        month_btn.pack(side="left", padx=2)
        
        week_btn = ctk.CTkButton(
            view_frame,
            text="Week", 
            width=60,
            command=lambda: self.set_view_mode("week"),
            **themes.get_button_styles()["secondary"]
        )
        week_btn.pack(side="left", padx=2)
        
        # Calendar display area
        self.calendar_frame = ctk.CTkScrollableFrame(
            self.parent,
            label_text="Calendar View"
        )
        self.calendar_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Create calendar grid
        self.create_calendar_grid()
    
    def create_calendar_grid(self):
        """Create monthly calendar grid"""
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Calendar title
        title_label = ctk.CTkLabel(
            self.calendar_frame,
            text="📅 Master Calendar - All Gardens",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=7, pady=20)
        
        # Day headers
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i, day in enumerate(days):
            day_label = ctk.CTkLabel(
                self.calendar_frame,
                text=day,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=120
            )
            day_label.grid(row=1, column=i, padx=2, pady=5, sticky="ew")
        
        # Generate calendar days
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue  # Empty cell
                
                # Create day cell
                day_frame = ctk.CTkFrame(
                    self.calendar_frame,
                    width=120,
                    height=100,
                    **themes.get_frame_styles()["default"]
                )
                day_frame.grid(row=week_num + 2, column=day_num, padx=2, pady=2, sticky="nsew")
                day_frame.grid_propagate(False)
                
                # Day number
                day_label = ctk.CTkLabel(
                    day_frame,
                    text=str(day),
                    font=ctk.CTkFont(size=14, weight="bold")
                )
                day_label.pack(anchor="nw", padx=5, pady=2)
                
                # Real tasks for this day
                current_day = date(self.current_date.year, self.current_date.month, day)
                day_tasks = [task for task in self.tasks_data if task["due_date"] == current_day.isoformat()]
                
                for task in day_tasks[:3]:  # Show max 3 tasks per day
                    # Task priority color mapping
                    priority_colors = {
                        "high": themes.get_color("error"),
                        "critical": themes.get_color("error"),
                        "medium": themes.get_color("warning"),
                        "low": themes.get_color("info")
                    }
                    
                    # Task icon based on type
                    task_icons = {
                        "watering": "💧",
                        "feeding": "🧪", 
                        "pruning": "✂️",
                        "harvesting": "🌾",
                        "seeding": "🌱",
                        "transplanting": "🌿",
                        "general": "📝"
                    }
                    
                    icon = task_icons.get(task["task_type"], "📝")
                    color = priority_colors.get(task["priority"], themes.get_color("info"))
                    
                    # Truncate long task titles
                    title = task["title"]
                    if len(title) > 12:
                        title = title[:12] + "..."
                    
                    task_label = ctk.CTkLabel(
                        day_frame,
                        text=f"{icon} {title}",
                        font=ctk.CTkFont(size=9),
                        text_color=color
                    )
                    task_label.pack(anchor="w", padx=5)
                    
                    # Add completion indicator
                    if task["completed"]:
                        task_label.configure(text_color=themes.get_color("success"))
                
                # Show "+X more" if there are more than 3 tasks
                if len(day_tasks) > 3:
                    more_label = ctk.CTkLabel(
                        day_frame,
                        text=f"+{len(day_tasks) - 3} more",
                        font=ctk.CTkFont(size=8),
                        text_color=themes.get_color("text_secondary")
                    )
                    more_label.pack(anchor="w", padx=5)
    
    def load_calendar_data(self):
        """Load tasks and events for calendar display"""
        logger.info("Loading calendar data from database...")
        
        try:
            # Get tasks for the current month
            start_date = self.current_date.replace(day=1)
            if self.current_date.month == 12:
                end_date = date(self.current_date.year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(self.current_date.year, self.current_date.month + 1, 1) - timedelta(days=1)
            
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT t.id, t.title, t.description, t.priority, t.due_date, t.due_time,
                           t.completed, t.task_type, t.estimated_duration, t.notes,
                           g.name as garden_name, p.name as plant_name
                    FROM tasks t
                    LEFT JOIN gardens g ON t.garden_id = g.id
                    LEFT JOIN plants p ON t.plant_id = p.id
                    WHERE t.due_date >= ? AND t.due_date <= ?
                    ORDER BY t.due_date, t.due_time
                """, (start_date.isoformat(), end_date.isoformat()))
                
                tasks = cursor.fetchall()
                self.tasks_data = []
                
                for task in tasks:
                    self.tasks_data.append({
                        "id": task[0],
                        "title": task[1],
                        "description": task[2] or "",
                        "priority": task[3],
                        "due_date": task[4],
                        "due_time": task[5] or "",
                        "completed": bool(task[6]),
                        "task_type": task[7],
                        "estimated_duration": task[8] or 0,
                        "notes": task[9] or "",
                        "garden_name": task[10] or "No Garden",
                        "plant_name": task[11] or ""
                    })
            
            logger.info(f"Loaded {len(self.tasks_data)} tasks for calendar display")
            self.update_calendar_display()
            
        except Exception as e:
            logger.error(f"Error loading calendar data: {e}")
            self.tasks_data = []
    
    def update_calendar_display(self):
        """Update calendar grid with task data"""
        # Clear existing task displays in calendar cells
        # This will be called after create_calendar_grid to add task indicators
        logger.info(f"Updating calendar display with {len(self.tasks_data)} tasks")
    
    def prev_month(self):
        """Navigate to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        
        self.update_calendar()
    
    def next_month(self):
        """Navigate to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        
        self.update_calendar()
    
    def update_calendar(self):
        """Update calendar display"""
        self.month_label.configure(text=self.current_date.strftime("%B %Y"))
        self.create_calendar_grid()
        self.load_calendar_data()
    
    def set_view_mode(self, mode: str):
        """Set calendar view mode"""
        logger.info(f"Setting calendar view mode: {mode}")
        # TODO: Implement different view modes
