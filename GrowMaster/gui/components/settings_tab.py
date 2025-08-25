"""Settings Tab - Application configuration and preferences"""

import customtkinter as ctk
import logging
from tkinter import messagebox
from config.themes import themes

logger = logging.getLogger(__name__)

class SettingsTab:
    """Comprehensive settings interface for GrowMaster configuration"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        
        # Configure parent frame
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Create main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(
            parent,
            label_text="⚙️ Application Settings"
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.create_interface()
        self.load_settings()
    
    def create_interface(self):
        """Create the settings interface"""
        
        # Application Settings Section
        self.create_app_settings_section()
        
        # GUI Settings Section
        self.create_gui_settings_section()
        
        # Notification Settings Section
        self.create_notification_settings_section()
        
        # Database Settings Section
        self.create_database_settings_section()
        
        # Calendar Settings Section
        self.create_calendar_settings_section()
        
        # Action buttons
        self.create_action_buttons()
    
    def create_app_settings_section(self):
        """Create application settings section"""
        # Section header
        app_frame = ctk.CTkFrame(self.main_frame, **themes.get_frame_styles()["card"])
        app_frame.pack(fill="x", padx=10, pady=10)
        
        app_label = ctk.CTkLabel(
            app_frame,
            text="🔧 Application Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        app_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Theme selection
        theme_frame = ctk.CTkFrame(app_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(theme_frame, text="Theme:", width=150).pack(side="left")
        self.theme_var = ctk.StringVar(value="dark")
        theme_dropdown = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.theme_var,
            values=["dark", "light"],
            command=self.on_theme_changed
        )
        theme_dropdown.pack(side="left", padx=(10, 0))
        
        # Auto backup
        backup_frame = ctk.CTkFrame(app_frame, fg_color="transparent")
        backup_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(backup_frame, text="Auto Backup:", width=150).pack(side="left")
        self.auto_backup_var = ctk.BooleanVar(value=True)
        backup_checkbox = ctk.CTkCheckBox(
            backup_frame,
            text="Enable automatic backups",
            variable=self.auto_backup_var
        )
        backup_checkbox.pack(side="left", padx=(10, 0))
        
        # Backup interval
        interval_frame = ctk.CTkFrame(app_frame, fg_color="transparent")
        interval_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(interval_frame, text="Backup Interval:", width=150).pack(side="left")
        self.backup_interval_var = ctk.StringVar(value="7")
        interval_entry = ctk.CTkEntry(
            interval_frame,
            textvariable=self.backup_interval_var,
            width=60
        )
        interval_entry.pack(side="left", padx=(10, 5))
        ctk.CTkLabel(interval_frame, text="days").pack(side="left")
    
    def create_gui_settings_section(self):
        """Create GUI settings section"""
        gui_frame = ctk.CTkFrame(self.main_frame, **themes.get_frame_styles()["card"])
        gui_frame.pack(fill="x", padx=10, pady=10)
        
        gui_label = ctk.CTkLabel(
            gui_frame,
            text="🖥️ Interface Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        gui_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Window size
        size_frame = ctk.CTkFrame(gui_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(size_frame, text="Window Size:", width=150).pack(side="left")
        
        self.window_width_var = ctk.StringVar(value="1200")
        width_entry = ctk.CTkEntry(size_frame, textvariable=self.window_width_var, width=80)
        width_entry.pack(side="left", padx=(10, 5))
        
        ctk.CTkLabel(size_frame, text="×").pack(side="left", padx=2)
        
        self.window_height_var = ctk.StringVar(value="800")
        height_entry = ctk.CTkEntry(size_frame, textvariable=self.window_height_var, width=80)
        height_entry.pack(side="left", padx=5)
        
        # Default tab
        tab_frame = ctk.CTkFrame(gui_frame, fg_color="transparent")
        tab_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(tab_frame, text="Default Tab:", width=150).pack(side="left")
        self.default_tab_var = ctk.StringVar(value="dashboard")
        tab_dropdown = ctk.CTkOptionMenu(
            tab_frame,
            variable=self.default_tab_var,
            values=["dashboard", "task_manager", "calendar", "cost_calculator", "inventory", "notes"]
        )
        tab_dropdown.pack(side="left", padx=(10, 0))
    
    def create_notification_settings_section(self):
        """Create notification settings section"""
        notif_frame = ctk.CTkFrame(self.main_frame, **themes.get_frame_styles()["card"])
        notif_frame.pack(fill="x", padx=10, pady=10)
        
        notif_label = ctk.CTkLabel(
            notif_frame,
            text="🔔 Notification Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        notif_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Notifications enabled
        self.notifications_enabled_var = ctk.BooleanVar(value=True)
        enabled_checkbox = ctk.CTkCheckBox(
            notif_frame,
            text="Enable notifications",
            variable=self.notifications_enabled_var
        )
        enabled_checkbox.pack(anchor="w", padx=15, pady=5)
        
        # Task reminders
        self.task_reminders_var = ctk.BooleanVar(value=True)
        task_checkbox = ctk.CTkCheckBox(
            notif_frame,
            text="Task reminders",
            variable=self.task_reminders_var
        )
        task_checkbox.pack(anchor="w", padx=15, pady=5)
        
        # Low stock alerts
        self.low_stock_var = ctk.BooleanVar(value=True)
        stock_checkbox = ctk.CTkCheckBox(
            notif_frame,
            text="Low stock alerts",
            variable=self.low_stock_var
        )
        stock_checkbox.pack(anchor="w", padx=15, pady=5)
        
        # Desktop notifications
        self.desktop_notif_var = ctk.BooleanVar(value=True)
        desktop_checkbox = ctk.CTkCheckBox(
            notif_frame,
            text="Desktop notifications",
            variable=self.desktop_notif_var
        )
        desktop_checkbox.pack(anchor="w", padx=15, pady=(5, 15))
    
    def create_database_settings_section(self):
        """Create database settings section"""
        db_frame = ctk.CTkFrame(self.main_frame, **themes.get_frame_styles()["card"])
        db_frame.pack(fill="x", padx=10, pady=10)
        
        db_label = ctk.CTkLabel(
            db_frame,
            text="🗄️ Database Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        db_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Auto backup
        self.db_auto_backup_var = ctk.BooleanVar(value=True)
        db_backup_checkbox = ctk.CTkCheckBox(
            db_frame,
            text="Auto backup database",
            variable=self.db_auto_backup_var
        )
        db_backup_checkbox.pack(anchor="w", padx=15, pady=5)
        
        # Max backups
        max_backup_frame = ctk.CTkFrame(db_frame, fg_color="transparent")
        max_backup_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(max_backup_frame, text="Max Backups:", width=150).pack(side="left")
        self.max_backups_var = ctk.StringVar(value="10")
        max_entry = ctk.CTkEntry(
            max_backup_frame,
            textvariable=self.max_backups_var,
            width=60
        )
        max_entry.pack(side="left", padx=(10, 0))
        
        # Compress backups
        self.compress_backups_var = ctk.BooleanVar(value=True)
        compress_checkbox = ctk.CTkCheckBox(
            db_frame,
            text="Compress backups",
            variable=self.compress_backups_var
        )
        compress_checkbox.pack(anchor="w", padx=15, pady=(5, 15))
    
    def create_calendar_settings_section(self):
        """Create calendar settings section"""
        cal_frame = ctk.CTkFrame(self.main_frame, **themes.get_frame_styles()["card"])
        cal_frame.pack(fill="x", padx=10, pady=10)
        
        cal_label = ctk.CTkLabel(
            cal_frame,
            text="📅 Calendar Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cal_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Default view
        view_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
        view_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(view_frame, text="Default View:", width=150).pack(side="left")
        self.calendar_view_var = ctk.StringVar(value="monthly")
        view_dropdown = ctk.CTkOptionMenu(
            view_frame,
            variable=self.calendar_view_var,
            values=["monthly", "weekly", "daily"]
        )
        view_dropdown.pack(side="left", padx=(10, 0))
        
        # Week start
        week_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
        week_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        ctk.CTkLabel(week_frame, text="Week Starts:", width=150).pack(side="left")
        self.week_start_var = ctk.StringVar(value="monday")
        week_dropdown = ctk.CTkOptionMenu(
            week_frame,
            variable=self.week_start_var,
            values=["monday", "sunday"]
        )
        week_dropdown.pack(side="left", padx=(10, 0))
    
    def create_action_buttons(self):
        """Create action buttons for settings"""
        button_frame = ctk.CTkFrame(self.main_frame, **themes.get_frame_styles()["card"])
        button_frame.pack(fill="x", padx=10, pady=10)
        
        button_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_container.pack(pady=15)
        
        # Save button
        save_btn = ctk.CTkButton(
            button_container,
            text="💾 Save Settings",
            command=self.save_settings,
            **themes.get_button_styles()["primary"]
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        # Reset button
        reset_btn = ctk.CTkButton(
            button_container,
            text="🔄 Reset to Defaults",
            command=self.reset_settings,
            **themes.get_button_styles()["secondary"]
        )
        reset_btn.pack(side="left", padx=(10, 0))
    
    def load_settings(self):
        """Load current settings into the interface"""
        try:
            # App settings
            self.theme_var.set(self.settings.get("app", "theme", "dark"))
            self.auto_backup_var.set(self.settings.get("app", "auto_backup", True))
            self.backup_interval_var.set(str(self.settings.get("app", "backup_interval_days", 7)))
            
            # GUI settings
            self.window_width_var.set(str(self.settings.get("gui", "window_width", 1200)))
            self.window_height_var.set(str(self.settings.get("gui", "window_height", 800)))
            self.default_tab_var.set(self.settings.get("gui", "default_tab", "dashboard"))
            
            # Notification settings
            self.notifications_enabled_var.set(self.settings.get("notifications", "enabled", True))
            self.task_reminders_var.set(self.settings.get("notifications", "task_reminders", True))
            self.low_stock_var.set(self.settings.get("notifications", "low_stock_alerts", True))
            self.desktop_notif_var.set(self.settings.get("notifications", "desktop_notifications", True))
            
            # Database settings
            self.db_auto_backup_var.set(self.settings.get("database", "auto_backup", True))
            self.max_backups_var.set(str(self.settings.get("database", "max_backups", 10)))
            self.compress_backups_var.set(self.settings.get("database", "compress_backups", True))
            
            # Calendar settings
            self.calendar_view_var.set(self.settings.get("calendar", "default_view", "monthly"))
            self.week_start_var.set(self.settings.get("calendar", "week_start", "monday"))
            
            logger.info("Settings loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
    
    def save_settings(self):
        """Save current settings"""
        try:
            # App settings
            self.settings.set("app", "theme", self.theme_var.get())
            self.settings.set("app", "auto_backup", self.auto_backup_var.get())
            
            try:
                backup_interval = int(self.backup_interval_var.get())
                self.settings.set("app", "backup_interval_days", backup_interval)
            except ValueError:
                messagebox.showerror("Error", "Backup interval must be a number")
                return
            
            # GUI settings
            try:
                width = int(self.window_width_var.get())
                height = int(self.window_height_var.get())
                self.settings.set("gui", "window_width", width)
                self.settings.set("gui", "window_height", height)
            except ValueError:
                messagebox.showerror("Error", "Window dimensions must be numbers")
                return
            
            self.settings.set("gui", "default_tab", self.default_tab_var.get())
            
            # Notification settings
            self.settings.set("notifications", "enabled", self.notifications_enabled_var.get())
            self.settings.set("notifications", "task_reminders", self.task_reminders_var.get())
            self.settings.set("notifications", "low_stock_alerts", self.low_stock_var.get())
            self.settings.set("notifications", "desktop_notifications", self.desktop_notif_var.get())
            
            # Database settings
            self.settings.set("database", "auto_backup", self.db_auto_backup_var.get())
            self.settings.set("database", "compress_backups", self.compress_backups_var.get())
            
            try:
                max_backups = int(self.max_backups_var.get())
                self.settings.set("database", "max_backups", max_backups)
            except ValueError:
                messagebox.showerror("Error", "Max backups must be a number")
                return
            
            # Calendar settings
            self.settings.set("calendar", "default_view", self.calendar_view_var.get())
            self.settings.set("calendar", "week_start", self.week_start_var.get())
            
            # Save to file
            self.settings.save()
            messagebox.showinfo("Success", "Settings saved successfully!")
            logger.info("Settings saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Confirm Reset", 
                              "Are you sure you want to reset all settings to defaults?"):
            try:
                self.settings.reset_to_defaults()
                self.load_settings()
                messagebox.showinfo("Success", "Settings reset to defaults!")
                logger.info("Settings reset to defaults")
            except Exception as e:
                logger.error(f"Error resetting settings: {e}")
                messagebox.showerror("Error", f"Failed to reset settings: {str(e)}")
    
    def on_theme_changed(self, selected_theme):
        """Handle theme change"""
        logger.info(f"Theme changed to: {selected_theme}")
        # Note: Actual theme application would require app restart or theme reload
