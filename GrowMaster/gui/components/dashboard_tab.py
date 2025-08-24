"""
Dashboard Tab - Central command center for GrowMaster Pro
Real-time overview of all active grows with status tracking
"""

import customtkinter as ctk
import tkinter as tk
from datetime import datetime, date, timedelta
import logging
from typing import Dict, List, Any

from config.themes import themes

logger = logging.getLogger(__name__)

class DashboardTab:
    """Main dashboard with grow overview and quick actions"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        
        # Configure parent frame
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        # Create dashboard sections
        self.create_header()
        self.create_main_content()
        self.create_quick_actions()
        
        # Load initial data
        self.refresh_dashboard()
        
        # Auto-refresh every 5 minutes
        self.schedule_refresh()
    
    def create_header(self):
        """Create dashboard header with summary stats"""
        header_frame = ctk.CTkFrame(self.parent, **themes.get_frame_styles()["card"])
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            header_frame,
            text=f"Good {self.get_time_greeting()}! Welcome to GrowMaster Pro",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        welcome_label.grid(row=0, column=0, columnspan=4, pady=20)
        
        # Summary statistics
        self.create_stat_card(header_frame, "Active Gardens", "0", "🌱", 0)
        self.create_stat_card(header_frame, "Pending Tasks", "0", "✅", 1)
        self.create_stat_card(header_frame, "Days to Harvest", "--", "🌾", 2)
        self.create_stat_card(header_frame, "Total Plants", "0", "🪴", 3)
    
    def create_stat_card(self, parent, title: str, value: str, icon: str, column: int):
        """Create individual statistics card"""
        card_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        card_frame.grid(row=1, column=column, padx=10, pady=10, sticky="nsew")
        
        # Icon
        icon_label = ctk.CTkLabel(
            card_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(pady=(10, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card_frame,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=themes.get_color("primary")
        )
        value_label.pack()
        
        # Title
        title_label = ctk.CTkLabel(
            card_frame,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color=themes.get_color("text_secondary")
        )
        title_label.pack(pady=(0, 15))
        
        # Store reference for updates
        setattr(self, f"stat_{title.lower().replace(' ', '_')}_value", value_label)
    
    def create_main_content(self):
        """Create main dashboard content area"""
        content_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left column - Recent activity and upcoming tasks
        left_column = ctk.CTkFrame(content_frame, **themes.get_frame_styles()["card"])
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_column.grid_rowconfigure(1, weight=1)
        
        # Upcoming tasks section
        tasks_title = ctk.CTkLabel(
            left_column,
            text="🔔 Upcoming Tasks",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        tasks_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        # Tasks list
        self.tasks_list = self.create_tasks_list(left_column)
        self.tasks_list.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Right column - Garden status and alerts
        right_column = ctk.CTkFrame(content_frame, **themes.get_frame_styles()["card"])
        right_column.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_column.grid_rowconfigure(1, weight=1)
        
        # Garden status section
        gardens_title = ctk.CTkLabel(
            right_column,
            text="🌱 Garden Status",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        gardens_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        # Gardens list
        self.gardens_list = self.create_gardens_list(right_column)
        self.gardens_list.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    
    def create_tasks_list(self, parent):
        """Create scrollable tasks list"""
        tasks_frame = ctk.CTkScrollableFrame(parent, label_text="")
        
        # Sample tasks (would be loaded from database)
        sample_tasks = [
            {"title": "Water Plants - Garden 1", "due": "Today", "priority": "high"},
            {"title": "Check pH levels", "due": "Tomorrow", "priority": "medium"},
            {"title": "Nutrient feeding - All Gardens", "due": "In 2 days", "priority": "high"},
            {"title": "Trim lower fan leaves", "due": "In 3 days", "priority": "low"},
            {"title": "Check for pests", "due": "Weekly", "priority": "medium"},
        ]
        
        for i, task in enumerate(sample_tasks):
            self.create_task_item(tasks_frame, task, i)
        
        return tasks_frame
    
    def create_task_item(self, parent, task: Dict, row: int):
        """Create individual task item"""
        task_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        task_frame.grid(row=row, column=0, sticky="ew", pady=5, padx=5)
        task_frame.grid_columnconfigure(1, weight=1)
        
        # Priority indicator
        priority_color = themes.get_priority_color(task["priority"])
        priority_frame = ctk.CTkFrame(task_frame, width=4, fg_color=priority_color)
        priority_frame.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(5, 0))
        
        # Task title
        title_label = ctk.CTkLabel(
            task_frame,
            text=task["title"],
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="w", padx=10, pady=(8, 2))
        
        # Due date
        due_label = ctk.CTkLabel(
            task_frame,
            text=f"Due: {task['due']}",
            font=ctk.CTkFont(size=10),
            text_color=themes.get_color("text_secondary"),
            anchor="w"
        )
        due_label.grid(row=1, column=1, sticky="w", padx=10, pady=(0, 8))
        
        # Complete button
        complete_btn = ctk.CTkButton(
            task_frame,
            text="✓",
            width=30,
            height=30,
            command=lambda: self.complete_task(task),
            **themes.get_button_styles()["success"]
        )
        complete_btn.grid(row=0, column=2, rowspan=2, padx=10, pady=5)
    
    def create_gardens_list(self, parent):
        """Create scrollable gardens list"""
        gardens_frame = ctk.CTkScrollableFrame(parent, label_text="")
        
        # Sample gardens (would be loaded from database)
        sample_gardens = [
            {"name": "Indoor Tent #1", "status": "Flowering Week 6", "health": "Excellent", "plants": 4},
            {"name": "Outdoor Plot", "status": "Vegetative", "health": "Good", "plants": 8},
            {"name": "Hydro System", "status": "Seedling", "health": "Monitoring", "plants": 12},
        ]
        
        for i, garden in enumerate(sample_gardens):
            self.create_garden_item(gardens_frame, garden, i)
        
        return gardens_frame
    
    def create_garden_item(self, parent, garden: Dict, row: int):
        """Create individual garden item"""
        garden_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        garden_frame.grid(row=row, column=0, sticky="ew", pady=5, padx=5)
        garden_frame.grid_columnconfigure(1, weight=1)
        
        # Garden icon
        icon_label = ctk.CTkLabel(
            garden_frame,
            text="🌿",
            font=ctk.CTkFont(size=20)
        )
        icon_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
        
        # Garden name
        name_label = ctk.CTkLabel(
            garden_frame,
            text=garden["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=5, pady=(10, 2))
        
        # Status
        status_label = ctk.CTkLabel(
            garden_frame,
            text=f"Status: {garden['status']}",
            font=ctk.CTkFont(size=11),
            text_color=themes.get_color("text_secondary"),
            anchor="w"
        )
        status_label.grid(row=1, column=1, sticky="w", padx=5, pady=1)
        
        # Health and plant count
        info_label = ctk.CTkLabel(
            garden_frame,
            text=f"Health: {garden['health']} • Plants: {garden['plants']}",
            font=ctk.CTkFont(size=10),
            text_color=themes.get_color("text_secondary"),
            anchor="w"
        )
        info_label.grid(row=2, column=1, sticky="w", padx=5, pady=(1, 10))
        
        # View button
        view_btn = ctk.CTkButton(
            garden_frame,
            text="View",
            width=60,
            height=25,
            command=lambda: self.view_garden(garden),
            **themes.get_button_styles()["secondary"]
        )
        view_btn.grid(row=0, column=2, rowspan=3, padx=10, pady=5)
    
    def create_quick_actions(self):
        """Create quick action buttons at bottom"""
        actions_frame = ctk.CTkFrame(self.parent, **themes.get_frame_styles()["default"])
        actions_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        actions_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Quick action buttons
        actions = [
            ("🌱 New Garden", self.new_garden),
            ("✅ Add Task", self.add_task),
            ("💰 Log Expense", self.log_expense),
            ("📊 View Reports", self.view_reports)
        ]
        
        for i, (text, command) in enumerate(actions):
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                height=40,
                command=command,
                **themes.get_button_styles()["secondary"]
            )
            btn.grid(row=0, column=i, padx=10, pady=15, sticky="ew")
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        try:
            # TODO: Load real data from database
            # For now, update with sample data
            self.update_statistics()
            logger.info("Dashboard refreshed")
        except Exception as e:
            logger.error(f"Error refreshing dashboard: {e}")
    
    def update_statistics(self):
        """Update dashboard statistics"""
        # TODO: Query database for real statistics
        # For now, use sample data
        stats = {
            "active_gardens": 3,
            "pending_tasks": 8,
            "days_to_harvest": 21,
            "total_plants": 24
        }
        
        try:
            self.stat_active_gardens_value.configure(text=str(stats["active_gardens"]))
            self.stat_pending_tasks_value.configure(text=str(stats["pending_tasks"]))
            self.stat_days_to_harvest_value.configure(text=str(stats["days_to_harvest"]))
            self.stat_total_plants_value.configure(text=str(stats["total_plants"]))
        except AttributeError:
            # Stats widgets not yet created
            pass
    
    def schedule_refresh(self):
        """Schedule automatic dashboard refresh"""
        self.parent.after(300000, self.refresh_dashboard)  # 5 minutes
        self.parent.after(300000, self.schedule_refresh)
    
    def get_time_greeting(self) -> str:
        """Get appropriate greeting based on time of day"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"
    
    # Event handlers
    def complete_task(self, task: Dict):
        """Mark task as completed"""
        logger.info(f"Completing task: {task['title']}")
        # TODO: Update task in database
    
    def view_garden(self, garden: Dict):
        """View garden details"""
        logger.info(f"Viewing garden: {garden['name']}")
        # TODO: Switch to garden tab or open garden details
    
    def new_garden(self):
        """Open new garden wizard"""
        logger.info("Opening new garden wizard")
        # TODO: Open new garden wizard
    
    def add_task(self):
        """Open add task dialog"""
        logger.info("Opening add task dialog")
        # TODO: Open add task dialog
    
    def log_expense(self):
        """Open expense logging dialog"""
        logger.info("Opening expense logging dialog")
        # TODO: Open expense dialog
    
    def view_reports(self):
        """Switch to reports view"""
        logger.info("Viewing reports")
        # TODO: Switch to analytics tab
