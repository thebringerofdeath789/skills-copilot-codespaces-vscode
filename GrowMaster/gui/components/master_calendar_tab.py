"""
Master Calendar Tab - Unified calendar view with advanced filtering
Shows all tasks across all gardens in one comprehensive view
"""

import customtkinter as ctk
from datetime import datetime, date, timedelta
import calendar
import logging

from config.themes import themes

logger = logging.getLogger(__name__)

class MasterCalendarTab:
    """Master calendar with multi-garden task visualization"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        self.current_date = date.today()
        
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
                
                # Sample tasks for demonstration
                if day % 3 == 0:  # Add some sample tasks
                    task_label = ctk.CTkLabel(
                        day_frame,
                        text="💧 Water plants",
                        font=ctk.CTkFont(size=9),
                        text_color=themes.get_color("info")
                    )
                    task_label.pack(anchor="w", padx=5)
                
                if day % 7 == 0:
                    task_label = ctk.CTkLabel(
                        day_frame,
                        text="🧪 Check nutrients",
                        font=ctk.CTkFont(size=9),
                        text_color=themes.get_color("warning")
                    )
                    task_label.pack(anchor="w", padx=5)
    
    def load_calendar_data(self):
        """Load tasks and events for calendar display"""
        # TODO: Load real data from database
        logger.info("Loading calendar data...")
    
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
