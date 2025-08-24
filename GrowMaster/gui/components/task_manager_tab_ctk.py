"""
Task Manager Tab
Comprehensive task scheduling and management interface
"""

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional

from ...core.schedulers.task_scheduler import TaskScheduler
from ...core.models.task import TaskType, Priority, TaskStatus

class TaskManagerTab(ctk.CTkFrame):
    """Advanced task management interface"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.task_scheduler = TaskScheduler()
        self.selected_task = None
        self.tasks_data = []
        
        self.setup_ui()
        self.load_tasks()
    
    def setup_ui(self):
        """Setup the task management interface"""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(header_frame, text="Task Manager", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(side="left", padx=10, pady=10)
        
        # Control buttons
        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=10)
        
        new_task_btn = ctk.CTkButton(button_frame, text="New Task", 
                                    command=self.create_new_task)
        new_task_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(button_frame, text="Refresh", 
                                   command=self.load_tasks)
        refresh_btn.pack(side="left", padx=5)
        
        # Filter and search frame
        filter_frame = ctk.CTkFrame(main_frame)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Date filter
        ctk.CTkLabel(filter_frame, text="Filter by date:").pack(side="left", padx=(10, 5), pady=10)
        
        self.date_filter = ctk.CTkOptionMenu(filter_frame, 
                                            values=["Today", "This Week", "This Month", "All"],
                                            command=self.filter_tasks)
        self.date_filter.pack(side="left", padx=5, pady=10)
        
        # Status filter
        ctk.CTkLabel(filter_frame, text="Status:").pack(side="left", padx=(20, 5), pady=10)
        
        self.status_filter = ctk.CTkOptionMenu(filter_frame,
                                              values=["All", "Pending", "In Progress", "Completed", "Overdue"],
                                              command=self.filter_tasks)
        self.status_filter.pack(side="left", padx=5, pady=10)
        
        # Search
        ctk.CTkLabel(filter_frame, text="Search:").pack(side="left", padx=(20, 5), pady=10)
        
        self.search_entry = ctk.CTkEntry(filter_frame, width=200)
        self.search_entry.pack(side="left", padx=5, pady=10)
        self.search_entry.bind("<KeyRelease>", self.on_search_changed)
        
        # Main content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Task list (left side)
        task_list_frame = ctk.CTkFrame(content_frame)
        task_list_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        task_list_label = ctk.CTkLabel(task_list_frame, text="Tasks", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        task_list_label.pack(pady=(10, 5))
        
        # Task list with scrollbar
        self.task_list_frame = ctk.CTkScrollableFrame(task_list_frame)
        self.task_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Task details (right side)
        self.details_frame = ctk.CTkFrame(content_frame, width=300)
        self.details_frame.pack(side="right", fill="y", padx=(5, 0))
        self.details_frame.pack_propagate(False)
        
        self.setup_task_details()
    
    def setup_task_details(self):
        """Setup task details panel"""
        
        details_label = ctk.CTkLabel(self.details_frame, text="Task Details", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        details_label.pack(pady=(10, 20))
        
        # Task details form
        self.details_content = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        self.details_content.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Task title
        self.title_var = tk.StringVar()
        ctk.CTkLabel(self.details_content, text="Title:").pack(anchor="w", pady=(0, 5))
        self.title_entry = ctk.CTkEntry(self.details_content, textvariable=self.title_var)
        self.title_entry.pack(fill="x", pady=(0, 10))
        
        # Description
        ctk.CTkLabel(self.details_content, text="Description:").pack(anchor="w", pady=(0, 5))
        self.description_text = ctk.CTkTextbox(self.details_content, height=80)
        self.description_text.pack(fill="x", pady=(0, 10))
        
        # Priority
        ctk.CTkLabel(self.details_content, text="Priority:").pack(anchor="w", pady=(0, 5))
        self.priority_var = ctk.CTkOptionMenu(self.details_content,
                                             values=["Low", "Medium", "High", "Critical"])
        self.priority_var.pack(fill="x", pady=(0, 10))
        
        # Due date
        ctk.CTkLabel(self.details_content, text="Due Date:").pack(anchor="w", pady=(0, 5))
        self.due_date_entry = ctk.CTkEntry(self.details_content, 
                                          placeholder_text="YYYY-MM-DD")
        self.due_date_entry.pack(fill="x", pady=(0, 10))
        
        # Status
        ctk.CTkLabel(self.details_content, text="Status:").pack(anchor="w", pady=(0, 5))
        self.status_var = ctk.CTkOptionMenu(self.details_content,
                                           values=["Pending", "In Progress", "Completed", "Cancelled"])
        self.status_var.pack(fill="x", pady=(0, 20))
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.details_content, fg_color="transparent")
        button_frame.pack(fill="x")
        
        save_btn = ctk.CTkButton(button_frame, text="Save", 
                               command=self.save_task)
        save_btn.pack(side="left", padx=(0, 5))
        
        delete_btn = ctk.CTkButton(button_frame, text="Delete", 
                                 fg_color="red", hover_color="darkred",
                                 command=self.delete_task)
        delete_btn.pack(side="right")
        
        # Initially disable details (no task selected)
        self.toggle_details(False)
    
    def load_tasks(self):
        """Load tasks from database"""
        try:
            # Clear existing task widgets
            for widget in self.task_list_frame.winfo_children():
                widget.destroy()
            
            # Sample tasks (in production, load from database)
            self.tasks_data = [
                {
                    "id": 1,
                    "title": "Water Plants",
                    "description": "Check soil moisture and water as needed",
                    "priority": "High",
                    "status": "Pending",
                    "due_date": "2025-08-24",
                    "garden_name": "Indoor Tent 1"
                },
                {
                    "id": 2,
                    "title": "Nutrient Feeding",
                    "description": "Apply weekly nutrient solution",
                    "priority": "Critical",
                    "status": "Overdue",
                    "due_date": "2025-08-23",
                    "garden_name": "Indoor Tent 1"
                },
                {
                    "id": 3,
                    "title": "Environmental Check",
                    "description": "Record temperature and humidity",
                    "priority": "Medium",
                    "status": "Completed",
                    "due_date": "2025-08-24",
                    "garden_name": "Indoor Tent 2"
                },
                {
                    "id": 4,
                    "title": "Pest Inspection",
                    "description": "Check plants for pests and diseases",
                    "priority": "High",
                    "status": "In Progress",
                    "due_date": "2025-08-25",
                    "garden_name": "Indoor Tent 1"
                }
            ]
            
            self.display_tasks(self.tasks_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
    
    def display_tasks(self, tasks):
        """Display tasks in the list"""
        
        # Clear existing widgets
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        if not tasks:
            no_tasks_label = ctk.CTkLabel(self.task_list_frame, 
                                         text="No tasks found",
                                         font=ctk.CTkFont(size=14))
            no_tasks_label.pack(pady=20)
            return
        
        for task in tasks:
            task_widget = self.create_task_widget(task)
            task_widget.pack(fill="x", pady=2)
    
    def create_task_widget(self, task):
        """Create a widget for a single task"""
        
        # Task frame with status-based color
        color_map = {
            "Completed": "#2d5a2d",
            "Overdue": "#5a2d2d", 
            "In Progress": "#2d4a5a",
            "Pending": "#4a4a4a"
        }
        
        task_frame = ctk.CTkFrame(self.task_list_frame, 
                                 fg_color=color_map.get(task["status"], "#4a4a4a"))
        
        # Task content
        content_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Title and priority
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        title_label = ctk.CTkLabel(header_frame, text=task["title"],
                                  font=ctk.CTkFont(weight="bold"))
        title_label.pack(side="left")
        
        priority_label = ctk.CTkLabel(header_frame, text=f"[{task['priority']}]",
                                     font=ctk.CTkFont(size=10))
        priority_label.pack(side="right")
        
        # Due date and status
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=(2, 0))
        
        due_label = ctk.CTkLabel(info_frame, text=f"Due: {task['due_date']}",
                                font=ctk.CTkFont(size=10))
        due_label.pack(side="left")
        
        status_label = ctk.CTkLabel(info_frame, text=task["status"],
                                   font=ctk.CTkFont(size=10))
        status_label.pack(side="right")
        
        # Garden info
        if "garden_name" in task:
            garden_label = ctk.CTkLabel(content_frame, text=f"Garden: {task['garden_name']}",
                                       font=ctk.CTkFont(size=9))
            garden_label.pack(anchor="w", pady=(2, 0))
        
        # Bind click event
        def on_task_click(event, task_data=task):
            self.select_task(task_data)
        
        task_frame.bind("<Button-1>", on_task_click)
        content_frame.bind("<Button-1>", on_task_click)
        
        return task_frame
    
    def select_task(self, task):
        """Select a task and display its details"""
        self.selected_task = task
        self.populate_task_details(task)
        self.toggle_details(True)
    
    def populate_task_details(self, task):
        """Populate task details form with selected task data"""
        
        self.title_var.set(task.get("title", ""))
        
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", task.get("description", ""))
        
        self.priority_var.set(task.get("priority", "Medium"))
        self.status_var.set(task.get("status", "Pending"))
        
        self.due_date_entry.delete(0, "end")
        self.due_date_entry.insert(0, task.get("due_date", ""))
    
    def toggle_details(self, enabled):
        """Enable/disable task details form"""
        
        state = "normal" if enabled else "disabled"
        
        self.title_entry.configure(state=state)
        self.description_text.configure(state=state)
        self.due_date_entry.configure(state=state)
        
        # Enable/disable buttons
        for widget in self.details_content.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for button in widget.winfo_children():
                    if isinstance(button, ctk.CTkButton):
                        button.configure(state=state)
    
    def create_new_task(self):
        """Create a new task"""
        
        # Clear form
        self.title_var.set("")
        self.description_text.delete("1.0", "end")
        self.priority_var.set("Medium")
        self.status_var.set("Pending")
        self.due_date_entry.delete(0, "end")
        
        # Tomorrow's date as default
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.due_date_entry.insert(0, tomorrow)
        
        self.selected_task = None
        self.toggle_details(True)
    
    def save_task(self):
        """Save the current task"""
        
        try:
            title = self.title_var.get().strip()
            if not title:
                messagebox.showerror("Error", "Task title is required")
                return
            
            task_data = {
                "title": title,
                "description": self.description_text.get("1.0", "end").strip(),
                "priority": self.priority_var.get(),
                "status": self.status_var.get(),
                "due_date": self.due_date_entry.get().strip()
            }
            
            # Validate date format
            if task_data["due_date"]:
                try:
                    datetime.strptime(task_data["due_date"], "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                    return
            
            if self.selected_task:
                # Update existing task
                task_data["id"] = self.selected_task["id"]
                messagebox.showinfo("Success", "Task updated successfully")
            else:
                # Create new task
                task_data["id"] = len(self.tasks_data) + 1
                messagebox.showinfo("Success", "Task created successfully")
            
            # In production, save to database
            self.load_tasks()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save task: {str(e)}")
    
    def delete_task(self):
        """Delete the selected task"""
        
        if not self.selected_task:
            return
        
        result = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete '{self.selected_task['title']}'?")
        
        if result:
            try:
                # In production, delete from database
                messagebox.showinfo("Success", "Task deleted successfully")
                self.load_tasks()
                self.toggle_details(False)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete task: {str(e)}")
    
    def filter_tasks(self, value=None):
        """Filter tasks based on selected criteria"""
        
        filtered_tasks = self.tasks_data.copy()
        
        # Date filter
        date_filter = self.date_filter.get()
        if date_filter != "All":
            today = datetime.now().date()
            
            if date_filter == "Today":
                filtered_tasks = [t for t in filtered_tasks if t["due_date"] == str(today)]
            elif date_filter == "This Week":
                week_end = today + timedelta(days=7)
                filtered_tasks = [t for t in filtered_tasks 
                                if today <= datetime.strptime(t["due_date"], "%Y-%m-%d").date() <= week_end]
            elif date_filter == "This Month":
                month_end = today.replace(day=28) + timedelta(days=4)
                month_end = month_end - timedelta(days=month_end.day)
                filtered_tasks = [t for t in filtered_tasks 
                                if today.month == datetime.strptime(t["due_date"], "%Y-%m-%d").date().month]
        
        # Status filter
        status_filter = self.status_filter.get()
        if status_filter != "All":
            if status_filter == "Overdue":
                today = datetime.now().date()
                filtered_tasks = [t for t in filtered_tasks 
                                if datetime.strptime(t["due_date"], "%Y-%m-%d").date() < today 
                                and t["status"] != "Completed"]
            else:
                filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]
        
        # Search filter
        search_term = self.search_entry.get().lower().strip()
        if search_term:
            filtered_tasks = [t for t in filtered_tasks 
                            if search_term in t["title"].lower() 
                            or search_term in t.get("description", "").lower()]
        
        self.display_tasks(filtered_tasks)
    
    def on_search_changed(self, event):
        """Handle search entry changes"""
        self.filter_tasks()

import customtkinter as ctk
import logging
from config.themes import themes

logger = logging.getLogger(__name__)

class TaskManagerTab:
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Placeholder content
        label = ctk.CTkLabel(
            parent,
            text="✅ Task Manager\n\nAdvanced task scheduling and dependency management\nComing soon...",
            font=ctk.CTkFont(size=16)
        )
        label.grid(row=0, column=0, padx=20, pady=20)
