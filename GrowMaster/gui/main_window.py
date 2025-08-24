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
from .components.dashboard_tab import DashboardTab
from .components.master_calendar_tab import MasterCalendarTab
from .components.grow_plans_tab import GrowPlansTab
from .components.task_manager_tab import TaskManagerTab
from .components.cost_calculator_tab import CostCalculatorTab
from .components.inventory_tab import InventoryTab
from .components.notes_tab import NotesTab
from .components.settings_tab import SettingsTab
from .dialogs.new_grow_wizard import NewGrowWizard

logger = logging.getLogger(__name__)

class MainWindow:
    """Main application window with tabbed interface"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.root = ctk.CTk()
        self.tabs = {}
        
        # Configure main window
        self.setup_window()
        
        # Initialize main components
        self.create_menu_bar()
        self.create_main_interface()
        self.create_status_bar()
        
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
    
    def create_main_interface(self):
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
            # This would typically query the database for real numbers
            active_gardens = 0  # TODO: Get from database
            pending_tasks = 0   # TODO: Get from database
            
            self.status_right.configure(
                text=f"Active Gardens: {active_gardens} | Pending Tasks: {pending_tasks}"
            )
        except Exception as e:
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
            wizard = NewGrowWizard(self.root, self.settings)
            wizard.show()
        except Exception as e:
            logger.error(f"Failed to show garden wizard: {e}")
            messagebox.showerror("Error", f"Failed to open garden wizard: {e}")
    
    def quick_add_task(self):
        """Show quick task creation dialog"""
        # TODO: Implement quick task dialog
        messagebox.showinfo("Coming Soon", "Quick task creation is being developed!")
    
    def on_closing(self):
        """Handle application closing"""
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
