"""
GrowMaster Pro - Main Application Window
Central GUI controller with modern tabbed interface
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import logging
from typing import Optional

from config.settings import Settings
from config.themes import themes
from core.database.database_manager import DatabaseManager
from core.schedulers.intelligent_task_generator import IntelligentTaskGenerator
from core.schedulers.multi_garden_coordinator import MultiGardenTaskCoordinator
from core.schedulers.notification_system import BasicNotificationSystem
from .components.dashboard_tab import DashboardTab
from .components.master_calendar_tab import MasterCalendarTab
from .components.grow_plans_tab import GrowPlansTab
from .components.task_manager_tab import TaskManagerTab
from .components.cost_calculator_tab import CostCalculatorTab
from .components.inventory_tab import InventoryTab
from .components.notes_tab import NotesTab
from .components.settings_tab import SettingsTab
from .dialogs.new_grow_wizard import NewGrowWizard
from .dialogs.quick_task_dialog import QuickTaskDialog

logger = logging.getLogger(__name__)

class MainWindow:
    """Main application window with tabbed interface"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.root = ctk.CTk()
        self.tabs = {}
        
        # Initialize database and automation systems
        self.initialize_automation_systems()
        
        # Configure main window
        self.setup_window()
        
        # Initialize main components
        self.create_menu_bar()
        self.create_main_interface()
        self.create_status_bar()
        
        # Start automation services
        self.start_automation_services()
        
        # Show welcome wizard on first run
        if self.settings.is_first_run():
            self.root.after(500, self.show_welcome_wizard)
    
    def setup_window(self):
        """Configure main window properties"""
        self.root.title("GrowMaster Pro - Professional Multi-Garden Management")
        
        # Window size and position
        width = self.settings.get("gui", "window_width", 1200)
        height = self.settings.get("gui", "window_height", 800)
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Window properties
        self.root.minsize(1000, 700)
        if self.settings.get("gui", "window_maximized", False):
            self.root.state('zoomed')
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Set theme
        theme = self.settings.get("app", "theme", "dark")
        themes.set_theme(theme)
        
        # Window icon (if available)
        try:
            self.root.iconbitmap("data/resources/icons/growmaster.ico")
        except:
            pass  # Icon file not found, continue without
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def initialize_automation_systems(self):
        """Initialize database manager and automation systems"""
        try:
            # Initialize database manager
            self.db_manager = DatabaseManager()
            logger.info("Database manager initialized")
            
            # Initialize automation systems
            self.task_generator = IntelligentTaskGenerator(self.db_manager)
            logger.info("Intelligent task generator initialized")
            
            self.task_coordinator = MultiGardenTaskCoordinator(self.db_manager)
            logger.info("Multi-garden task coordinator initialized")
            
            self.notification_system = BasicNotificationSystem(self.db_manager)
            logger.info("Notification system initialized")
            
            # Create notification tables if they don't exist
            self.notification_system.create_notification_tables()
            
        except Exception as e:
            logger.error(f"Failed to initialize automation systems: {e}")
            # Continue without automation systems for now
            self.db_manager = DatabaseManager()
            self.task_generator = None
            self.task_coordinator = None
            self.notification_system = None
    
    def start_automation_services(self):
        """Start background automation services"""
        try:
            # Start notification worker if available
            if self.notification_system:
                self.notification_system.start_worker()
                logger.info("Notification worker started")
            
            # Schedule daily task coordination
            if self.task_coordinator:
                self.schedule_daily_coordination()
                logger.info("Daily task coordination scheduled")
                
        except Exception as e:
            logger.error(f"Failed to start automation services: {e}")
    
    def schedule_daily_coordination(self):
        """Schedule daily task coordination to run automatically"""
        def run_coordination():
            try:
                if self.task_coordinator:
                    result = self.task_coordinator.coordinate_daily_tasks()
                    logger.info(f"Daily coordination completed: {result}")
            except Exception as e:
                logger.error(f"Daily coordination failed: {e}")
            
            # Schedule next run in 24 hours (86400000 ms)
            self.root.after(86400000, run_coordination)
        
        # Run first coordination after 5 seconds, then daily
        self.root.after(5000, run_coordination)
    
    def create_menu_bar(self):
        """Create application menu bar"""
        self.menu_frame = ctk.CTkFrame(self.root, height=50, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.menu_frame.grid_columnconfigure(1, weight=1)
        
        # Application title and logo
        title_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🌱 GrowMaster Pro",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=themes.get_color("primary")
        )
        title_label.pack(side="left")
        
        # Quick action buttons
        button_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        button_frame.grid(row=0, column=2, sticky="e", padx=20, pady=10)
        
        # New Garden button
        new_garden_btn = ctk.CTkButton(
            button_frame,
            text="+ New Garden",
            width=120,
            command=self.new_garden_wizard,
            **themes.get_button_styles()["primary"]
        )
        new_garden_btn.pack(side="right", padx=5)
        
        # Add Task button
        add_task_btn = ctk.CTkButton(
            button_frame,
            text="+ Add Task",
            width=100,
            command=self.quick_add_task,
            **themes.get_button_styles()["secondary"]
        )
        add_task_btn.pack(side="right", padx=5)
        
        # Generate Tasks button (for automation)
        if self.task_generator:
            gen_tasks_btn = ctk.CTkButton(
                button_frame,
                text="⚡ Generate Tasks",
                width=120,
                command=self.generate_tasks_for_all,
                **themes.get_button_styles()["accent"]
            )
            gen_tasks_btn.pack(side="right", padx=5)    def create_main_interface(self):
        """Create main tabbed interface"""
        # Main container
        self.main_container = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Create tabview
        self.tabview = ctk.CTkTabview(self.main_container, corner_radius=10)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Add tabs
        self.create_tabs()
    
    def create_tabs(self):
        """Create all application tabs"""
        tab_configs = [
            ("Dashboard", DashboardTab, "📊"),
            ("Calendar", MasterCalendarTab, "📅"),
            ("Gardens", GrowPlansTab, "🌱"),
            ("Tasks", TaskManagerTab, "✅"),
            ("Inventory", InventoryTab, "📦"),
            ("Calculator", CostCalculatorTab, "💰"),
            ("Notes", NotesTab, "📝"),
            ("Settings", SettingsTab, "⚙️")
        ]
        
        for tab_name, tab_class, icon in tab_configs:
            # Add tab to tabview
            tab_display_name = f"{icon} {tab_name}"
            self.tabview.add(tab_display_name)
            
            # Create tab content
            try:
                # Special handling for Dashboard tab to provide tab switching capability
                if tab_name == "Dashboard":
                    tab_instance = tab_class(self.tabview.tab(tab_display_name), self.settings, self)
                else:
                    tab_instance = tab_class(self.tabview.tab(tab_display_name), self.settings)
                    
                self.tabs[tab_name.lower()] = tab_instance
                logger.info(f"Created {tab_name} tab successfully")
            except Exception as e:
                logger.error(f"Failed to create {tab_name} tab: {e}")
                # Create placeholder tab
                placeholder = ctk.CTkLabel(
                    self.tabview.tab(tab_display_name),
                    text=f"{tab_name} tab is being developed...\\n{str(e)}",
                    font=ctk.CTkFont(size=14)
                )
                placeholder.pack(expand=True)
        
        # Set default tab
        default_tab = self.settings.get("gui", "default_tab", "dashboard")
        try:
            if default_tab in [t.lower() for t in self.tabs.keys()]:
                # Find the full tab name with icon
                for tab_name, _, icon in tab_configs:
                    if tab_name.lower() == default_tab:
                        self.tabview.set(f"{icon} {tab_name}")
                        break
        except:
            pass  # Use default tab selection
    
    def create_status_bar(self):
        """Create status bar with system information"""
        self.status_frame = ctk.CTkFrame(self.root, height=30, corner_radius=0)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        self.status_frame.grid_columnconfigure(1, weight=1)
        
        # Status labels
        self.status_left = ctk.CTkLabel(
            self.status_frame,
            text=f"Ready - GrowMaster Pro v1.0",
            font=ctk.CTkFont(size=11)
        )
        self.status_left.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Automation status
        automation_status = self.get_automation_status()
        self.status_right = ctk.CTkLabel(
            self.status_frame,
            text=automation_status,
            font=ctk.CTkFont(size=11)
        )
        self.status_right.grid(row=0, column=2, sticky="e", padx=10, pady=5)
    
    def get_automation_status(self):
        """Get current automation system status"""
        status_parts = []
        
        if self.task_generator:
            status_parts.append("🤖 Tasks")
        if self.task_coordinator:
            status_parts.append("🤝 Coordinator") 
        if self.notification_system:
            status_parts.append("🔔 Notifications")
        
        if status_parts:
            return f"Automation: {' | '.join(status_parts)}"
        else:
            return "Automation: Disabled"
            text="Ready",
            font=ctk.CTkFont(size=10)
        )
        self.status_left.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        self.status_right = ctk.CTkLabel(
            self.status_frame,
            text="Active Gardens: 0 | Pending Tasks: 0",
            font=ctk.CTkFont(size=10)
        )
        self.status_right.grid(row=0, column=2, sticky="e", padx=10, pady=5)
        
        # Update status periodically
        self.update_status()
    
    def update_status(self):
        """Update status bar information"""
        try:
            # Get actual garden count from database
            with self.db_manager.get_connection() as conn:
                garden_cursor = conn.execute("SELECT COUNT(*) FROM gardens WHERE is_active = 1")
                active_gardens = garden_cursor.fetchone()[0]
                
                # Get pending tasks count
                task_cursor = conn.execute("""
                    SELECT COUNT(*) FROM tasks 
                    WHERE is_completed = 0 AND due_date >= date('now')
                """)
                pending_tasks = task_cursor.fetchone()[0]
                
            self.status_right.configure(
                text=f"Active Gardens: {active_gardens} | Pending Tasks: {pending_tasks}"
            )
        except Exception as e:
            logger.error(f"Error updating status: {e}")
            self.status_right.configure(
                text="Active Gardens: 0 | Pending Tasks: 0"
            )
            logger.error(f"Error updating status: {e}")
        
        # Schedule next update
        self.root.after(30000, self.update_status)  # Update every 30 seconds
    
    def show_welcome_wizard(self):
        """Show welcome wizard for first-time users"""
        try:
            wizard = NewGrowWizard(self.root, self.settings)
            wizard.show()
        except Exception as e:
            logger.error(f"Failed to show welcome wizard: {e}")
            messagebox.showinfo(
                "Welcome to GrowMaster Pro",
                "Welcome to GrowMaster Pro!\\n\\n"
                "Click 'New Garden' to create your first garden setup."
            )
        
        # Mark first run as complete
        self.settings.mark_first_run_complete()
    
    def new_garden_wizard(self):
        """Show new garden creation wizard"""
        try:
            def on_garden_created():
                """Callback when garden is created successfully"""
                # Refresh gardens tab
                if "gardens" in self.tabs:
                    try:
                        self.tabs["gardens"].refresh_data()
                    except:
                        pass
                
                # Refresh dashboard
                if "dashboard" in self.tabs:
                    try:
                        self.tabs["dashboard"].refresh_data()
                    except:
                        pass
                
                # Show notification
                if self.notification_system:
                    self.notification_system.show_notification(
                        "Garden Created",
                        "Your new automated garden has been set up successfully!"
                    )
            
            wizard = NewGrowWizard(self.root, self.db_manager, callback=on_garden_created)
            wizard.show()
        except Exception as e:
            logger.error(f"Failed to show garden wizard: {e}")
            messagebox.showerror("Error", f"Failed to open garden wizard: {e}")
    
    def switch_to_tab(self, tab_name):
        """Switch to specified tab"""
        try:
            # Map tab names to display names
            tab_mapping = {
                "dashboard": "📊 Dashboard",
                "calendar": "📅 Calendar", 
                "gardens": "🌱 Gardens",
                "tasks": "✅ Tasks",
                "inventory": "📦 Inventory",
                "calculator": "💰 Calculator",
                "notes": "📝 Notes",
                "settings": "⚙️ Settings"
            }
            
            display_name = tab_mapping.get(tab_name.lower())
            if display_name:
                self.tabview.set(display_name)
                logger.info(f"Switched to {tab_name} tab")
            else:
                logger.warning(f"Unknown tab name: {tab_name}")
                
        except Exception as e:
            logger.error(f"Error switching to tab {tab_name}: {e}")
    
    def generate_tasks_for_all(self):
        """Generate tasks for all active gardens"""
        try:
            if not self.task_generator:
                messagebox.showwarning("Not Available", "Task generation system is not available.")
                return
            
            # Get all active gardens
            with self.db_manager.get_connection() as conn:
                gardens = conn.execute("""
                    SELECT id, name FROM gardens 
                    WHERE is_active = 1
                    ORDER BY name
                """).fetchall()
            
            if not gardens:
                messagebox.showinfo("No Gardens", "No active gardens found. Create a garden first!")
                return
            
            total_tasks = 0
            for garden in gardens:
                try:
                    tasks = self.task_generator.generate_tasks_for_garden(garden['id'])
                    total_tasks += len(tasks)
                except Exception as e:
                    logger.error(f"Failed to generate tasks for garden {garden['name']}: {e}")
            
            # Show success message
            if total_tasks > 0:
                messagebox.showinfo(
                    "Tasks Generated",
                    f"Generated {total_tasks} tasks for {len(gardens)} gardens!"
                )
                
                # Refresh task tab
                if "tasks" in self.tabs:
                    try:
                        self.tabs["tasks"].refresh_data()
                    except:
                        pass
                        
                # Show notification
                if self.notification_system:
                    self.notification_system.show_notification(
                        "Tasks Generated",
                        f"Created {total_tasks} new tasks for your gardens"
                    )
            else:
                messagebox.showinfo("No Tasks", "No new tasks were generated.")
                
        except Exception as e:
            logger.error(f"Error generating tasks: {e}")
            messagebox.showerror("Error", f"Failed to generate tasks: {e}")
    
    def quick_add_task(self):
        """Show quick task creation dialog"""
        try:
            # Refresh dashboard callback for task updates
            refresh_callback = None
            if "Dashboard" in self.tabs:
                refresh_callback = lambda: self.tabs["Dashboard"].refresh_data()
            
            dialog = QuickTaskDialog(self.root, self.settings, callback=refresh_callback)
            result = dialog.show()
            
            if result:
                logger.info(f"Quick task created: {result['title']}")
                # Switch to dashboard tab to show the new task
                self.tabview.set("Dashboard")
                
        except Exception as e:
            logger.error(f"Error in quick task dialog: {e}")
            messagebox.showerror("Error", f"Failed to open task dialog: {str(e)}")
    
    def on_closing(self):
        """Handle application closing"""
        # Stop automation services
        try:
            if self.notification_system:
                self.notification_system.stop_worker()
                logger.info("Notification system stopped")
        except Exception as e:
            logger.error(f"Error stopping automation services: {e}")
        
        # Save window state
        if self.root.state() == 'zoomed':
            self.settings.set("gui", "window_maximized", True)
        else:
            self.settings.set("gui", "window_maximized", False)
            self.settings.set("gui", "window_width", self.root.winfo_width())
            self.settings.set("gui", "window_height", self.root.winfo_height())
        
        # Save settings
        self.settings.save()
        
        # Close application
        logger.info("Application closing...")
        self.root.destroy()
    
    def run(self):
        """Start the main application loop"""
        logger.info("Starting GrowMaster Pro GUI...")
        self.root.mainloop()
