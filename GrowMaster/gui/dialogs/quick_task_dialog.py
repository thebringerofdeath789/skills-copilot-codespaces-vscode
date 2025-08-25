"""
Quick Task Dialog - Fast task creation interface
Allows rapid task creation with minimal input
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime, timedelta
from typing import Optional

from config.themes import themes
from core.database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class QuickTaskDialog:
    """Quick task creation dialog for rapid task entry"""
    
    def __init__(self, parent, settings, callback=None):
        self.parent = parent
        self.settings = settings
        self.callback = callback
        self.db_manager = DatabaseManager()
        
        self.dialog = None
        self.result = None
        self.gardens_data = []
        
        self.create_dialog()
        self.load_gardens()
        
    def create_dialog(self):
        """Create the quick task dialog"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("⚡ Quick Add Task")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Configure dialog
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(0, weight=1)
        
        # Main container
        main_frame = ctk.CTkFrame(self.dialog, **themes.get_frame_styles()["card"])
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⚡ Quick Add Task",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Rapidly create tasks with smart defaults",
            font=ctk.CTkFont(size=12),
            text_color=themes.get_color("text_secondary")
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Form container
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Task name (required)
        row = 0
        ctk.CTkLabel(form_frame, text="Task Name*:", width=100).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=5
        )
        self.task_name_var = ctk.StringVar()
        self.task_name_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.task_name_var,
            placeholder_text="e.g., Water plants, Check pH, Harvest lettuce"
        )
        self.task_name_entry.grid(row=row, column=1, sticky="ew", pady=5)
        self.task_name_entry.focus()
        
        # Garden selection
        row += 1
        ctk.CTkLabel(form_frame, text="Garden:", width=100).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=5
        )
        self.garden_var = ctk.StringVar()
        self.garden_dropdown = ctk.CTkOptionMenu(
            form_frame, 
            variable=self.garden_var,
            values=["Loading..."]
        )
        self.garden_dropdown.grid(row=row, column=1, sticky="ew", pady=5)
        
        # Priority
        row += 1
        ctk.CTkLabel(form_frame, text="Priority:", width=100).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=5
        )
        self.priority_var = ctk.StringVar(value="Medium")
        priority_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=self.priority_var,
            values=["Low", "Medium", "High", "Critical"]
        )
        priority_dropdown.grid(row=row, column=1, sticky="ew", pady=5)
        
        # Category
        row += 1
        ctk.CTkLabel(form_frame, text="Category:", width=100).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=5
        )
        self.category_var = ctk.StringVar(value="General")
        category_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=self.category_var,
            values=[
                "General", "Watering", "Feeding", "Monitoring",
                "Pruning", "Harvesting", "Maintenance", "Transplanting"
            ]
        )
        category_dropdown.grid(row=row, column=1, sticky="ew", pady=5)
        
        # Due date
        row += 1
        ctk.CTkLabel(form_frame, text="Due Date:", width=100).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=5
        )
        
        due_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        due_frame.grid(row=row, column=1, sticky="ew", pady=5)
        due_frame.grid_columnconfigure(1, weight=1)
        
        self.due_preset_var = ctk.StringVar(value="Today")
        due_preset = ctk.CTkOptionMenu(
            due_frame,
            variable=self.due_preset_var,
            values=["Today", "Tomorrow", "Next Week", "Custom"],
            command=self.on_due_preset_change,
            width=120
        )
        due_preset.grid(row=0, column=0, sticky="w")
        
        self.due_date_var = ctk.StringVar()
        self.due_date_entry = ctk.CTkEntry(
            due_frame,
            textvariable=self.due_date_var,
            placeholder_text="YYYY-MM-DD",
            state="disabled"
        )
        self.due_date_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        # Set default due date
        self.on_due_preset_change("Today")
        
        # Recurring task option
        row += 1
        self.recurring_var = ctk.BooleanVar()
        recurring_check = ctk.CTkCheckBox(
            form_frame,
            text="Recurring Task",
            variable=self.recurring_var,
            command=self.on_recurring_toggle
        )
        recurring_check.grid(row=row, column=1, sticky="w", pady=5)
        
        # Recurrence pattern (initially hidden)
        row += 1
        self.recurrence_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.recurrence_frame.grid(row=row, column=1, sticky="ew", pady=5)
        self.recurrence_frame.grid_remove()  # Initially hidden
        
        ctk.CTkLabel(self.recurrence_frame, text="Repeat every:").grid(
            row=0, column=0, sticky="w"
        )
        
        self.recurrence_interval_var = ctk.StringVar(value="1")
        interval_entry = ctk.CTkEntry(
            self.recurrence_frame, 
            textvariable=self.recurrence_interval_var,
            width=50
        )
        interval_entry.grid(row=0, column=1, padx=(10, 5))
        
        self.recurrence_unit_var = ctk.StringVar(value="days")
        unit_dropdown = ctk.CTkOptionMenu(
            self.recurrence_frame,
            variable=self.recurrence_unit_var,
            values=["days", "weeks", "months"]
        )
        unit_dropdown.grid(row=0, column=2, padx=(5, 0))
        
        # Notes
        row += 1
        ctk.CTkLabel(form_frame, text="Notes:", width=100).grid(
            row=row, column=0, sticky="nw", padx=(0, 10), pady=(15, 5)
        )
        self.notes_textbox = ctk.CTkTextbox(
            form_frame, 
            height=80,
            placeholder_text="Additional details, instructions, or reminders..."
        )
        self.notes_textbox.grid(row=row, column=1, sticky="ew", pady=(15, 5))
        
        # Smart suggestions
        row += 1
        suggestions_frame = ctk.CTkFrame(form_frame, **themes.get_frame_styles()["default"])
        suggestions_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(20, 10))
        
        ctk.CTkLabel(
            suggestions_frame,
            text="💡 Quick Suggestions:",
            font=ctk.CTkFont(weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        suggestions_container = ctk.CTkFrame(suggestions_frame, fg_color="transparent")
        suggestions_container.pack(fill="x", padx=15, pady=(0, 10))
        
        # Common task buttons
        common_tasks = [
            ("💧 Water Plants", "Water Plants", "Watering", "High"),
            ("🔬 Check pH", "Check pH levels", "Monitoring", "Medium"),
            ("🌱 Feed Plants", "Feed nutrients", "Feeding", "Medium"),
            ("✂️ Prune", "Prune and trim", "Pruning", "Low"),
        ]
        
        for i, (text, name, category, priority) in enumerate(common_tasks):
            btn = ctk.CTkButton(
                suggestions_container,
                text=text,
                command=lambda n=name, c=category, p=priority: self.apply_suggestion(n, c, p),
                **themes.get_button_styles()["secondary"],
                width=120,
                height=28
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=2, sticky="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        
        # Left side buttons
        left_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons.pack(side="left")
        
        save_and_new_btn = ctk.CTkButton(
            left_buttons,
            text="💾 Save & New",
            command=self.save_and_new_task,
            **themes.get_button_styles()["secondary"]
        )
        save_and_new_btn.pack(side="left", padx=(0, 10))
        
        # Right side buttons
        right_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_buttons.pack(side="right")
        
        cancel_btn = ctk.CTkButton(
            right_buttons,
            text="❌ Cancel",
            command=self.cancel,
            **themes.get_button_styles()["secondary"]
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            right_buttons,
            text="💾 Save Task",
            command=self.save_task,
            **themes.get_button_styles()["primary"]
        )
        save_btn.pack(side="left")
        
        # Keyboard shortcuts
        self.dialog.bind('<Return>', lambda e: self.save_task())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
    def load_gardens(self):
        """Load gardens from database"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("SELECT id, name FROM gardens ORDER BY name")
                gardens = cursor.fetchall()
                
                self.gardens_data = []
                garden_names = []
                
                for garden in gardens:
                    self.gardens_data.append({
                        "id": garden[0],
                        "name": garden[1]
                    })
                    garden_names.append(garden[1])
                
                if garden_names:
                    self.garden_dropdown.configure(values=garden_names)
                    self.garden_var.set(garden_names[0])
                else:
                    self.garden_dropdown.configure(values=["No gardens found"])
                    self.garden_var.set("No gardens found")
                    
                logger.info(f"Loaded {len(garden_names)} gardens for task dialog")
                
        except Exception as e:
            logger.error(f"Error loading gardens: {e}")
            self.garden_dropdown.configure(values=["Error loading gardens"])
            self.garden_var.set("Error loading gardens")
    
    def on_due_preset_change(self, value):
        """Handle due date preset selection"""
        today = datetime.now()
        
        if value == "Today":
            due_date = today
            self.due_date_entry.configure(state="disabled")
        elif value == "Tomorrow":
            due_date = today + timedelta(days=1)
            self.due_date_entry.configure(state="disabled")
        elif value == "Next Week":
            due_date = today + timedelta(weeks=1)
            self.due_date_entry.configure(state="disabled")
        elif value == "Custom":
            self.due_date_entry.configure(state="normal")
            self.due_date_var.set("")
            return
        
        self.due_date_var.set(due_date.strftime("%Y-%m-%d"))
    
    def on_recurring_toggle(self):
        """Toggle recurrence options visibility"""
        if self.recurring_var.get():
            self.recurrence_frame.grid()
        else:
            self.recurrence_frame.grid_remove()
    
    def apply_suggestion(self, name, category, priority):
        """Apply a suggestion to the form"""
        self.task_name_var.set(name)
        self.category_var.set(category)
        self.priority_var.set(priority)
    
    def validate_form(self):
        """Validate form data"""
        if not self.task_name_var.get().strip():
            messagebox.showerror("Error", "Task name is required")
            self.task_name_entry.focus()
            return False
        
        # Validate due date format
        if self.due_preset_var.get() == "Custom":
            try:
                datetime.strptime(self.due_date_var.get(), "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid due date format. Use YYYY-MM-DD")
                self.due_date_entry.focus()
                return False
        
        # Validate recurrence interval
        if self.recurring_var.get():
            try:
                interval = int(self.recurrence_interval_var.get())
                if interval <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Recurrence interval must be a positive number")
                return False
        
        return True
    
    def get_selected_garden_id(self):
        """Get the selected garden ID"""
        selected_name = self.garden_var.get()
        for garden in self.gardens_data:
            if garden["name"] == selected_name:
                return garden["id"]
        return None
    
    def save_task(self):
        """Save the task"""
        if not self.validate_form():
            return
        
        try:
            garden_id = self.get_selected_garden_id()
            if not garden_id:
                messagebox.showerror("Error", "Please select a valid garden")
                return
            
            task_data = {
                "title": self.task_name_var.get().strip(),
                "description": self.notes_textbox.get("1.0", "end").strip(),
                "due_date": self.due_date_var.get(),
                "priority": self.priority_var.get().lower(),
                "category": self.category_var.get().lower(),
                "status": "pending",
                "garden_id": garden_id,
                "created_date": datetime.now().isoformat(),
                "is_recurring": self.recurring_var.get()
            }
            
            # Handle recurrence
            recurrence_pattern = None
            if self.recurring_var.get():
                interval = int(self.recurrence_interval_var.get())
                unit = self.recurrence_unit_var.get()
                recurrence_pattern = f"every_{interval}_{unit}"
            
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO tasks 
                    (title, description, due_date, priority, category, status, 
                     garden_id, created_date, recurrence_pattern)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    task_data["title"], task_data["description"], task_data["due_date"],
                    task_data["priority"], task_data["category"], task_data["status"],
                    task_data["garden_id"], task_data["created_date"], recurrence_pattern
                ))
                
                task_id = cursor.lastrowid
            
            logger.info(f"Quick task created: {task_data['title']} (ID: {task_id})")
            messagebox.showinfo("Success", f"Task '{task_data['title']}' created successfully!")
            
            # Call callback if provided
            if self.callback:
                self.callback()
            
            self.result = task_data
            self.dialog.destroy()
            
        except Exception as e:
            logger.error(f"Error saving task: {e}")
            messagebox.showerror("Error", f"Failed to save task: {str(e)}")
    
    def save_and_new_task(self):
        """Save current task and create new one"""
        if not self.validate_form():
            return
        
        # Save current task
        current_task_name = self.task_name_var.get()
        self.save_task()
        
        # If save was successful (dialog wasn't destroyed due to error)
        if hasattr(self, 'dialog') and self.dialog.winfo_exists():
            # Clear form for new task
            self.task_name_var.set("")
            self.notes_textbox.delete("1.0", "end")
            self.priority_var.set("Medium")
            self.category_var.set("General")
            self.due_preset_var.set("Today")
            self.on_due_preset_change("Today")
            self.recurring_var.set(False)
            self.on_recurring_toggle()
            self.task_name_entry.focus()
            
            # Show brief confirmation
            self.dialog.title(f"✅ Saved: {current_task_name[:30]}...")
            self.dialog.after(1500, lambda: self.dialog.title("⚡ Quick Add Task"))
    
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """Show dialog and return result"""
        # Position dialog
        self.dialog.geometry("500x600+{}+{}".format(
            self.parent.winfo_x() + 50,
            self.parent.winfo_y() + 50
        ))
        
        self.dialog.wait_window()
        return self.result
