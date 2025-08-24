"""
GrowMaster Pro - Main Window (Standard Tkinter Version)
Professional multi-garden management interface using standard Tkinter and ttk
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Menu
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MainWindow:
    """Main application window using standard Tkinter"""
    
    def __init__(self):
        """Initialize main window with modern styling"""
        self.root = tk.Tk()
        self.setup_window()
        self.create_menu_bar()
        self.create_main_interface()
        self.setup_styles()
    
    def setup_window(self):
        """Configure main window properties"""
        self.root.title("GrowMaster Pro - Professional Multi-Garden Management")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Configure for modern appearance
        self.root.configure(bg='#f0f0f0')
        
        # Center the window
        self.center_window()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        
        # Configure notebook (tab) style
        style.configure('MainNotebook.TNotebook', background='#f0f0f0')
        style.configure('MainNotebook.TNotebook.Tab', 
                       padding=[20, 10], 
                       font=('Arial', 10, 'bold'))
        
        # Configure frames
        style.configure('Card.TFrame', 
                       background='white', 
                       relief='solid', 
                       borderwidth=1)
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Garden", command=self.new_garden)
        file_menu.add_command(label="Import Data", command=self.import_data)
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Gardens menu
        gardens_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Gardens", menu=gardens_menu)
        gardens_menu.add_command(label="Manage Gardens", command=self.manage_gardens)
        gardens_menu.add_command(label="Garden Settings", command=self.garden_settings)
        
        # Tools menu
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Calculators", command=self.open_calculators)
        tools_menu.add_command(label="Reports", command=self.generate_reports)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_interface(self):
        """Create the main tabbed interface"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Status bar at top
        self.create_status_bar(main_frame)
        
        # Main notebook (tabbed interface)
        self.notebook = ttk.Notebook(main_frame, style='MainNotebook.TNotebook')
        self.notebook.pack(fill='both', expand=True, pady=(10, 0))
        
        # Create tabs
        self.create_tabs()
    
    def create_status_bar(self, parent):
        """Create status bar with system information"""
        status_frame = ttk.Frame(parent, style='Card.TFrame')
        status_frame.pack(fill='x', pady=(0, 5))
        
        # System status indicators
        ttk.Label(status_frame, text="System Status:", 
                 font=('Arial', 9, 'bold')).pack(side='left', padx=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", 
                                     foreground='green')
        self.status_label.pack(side='left', padx=5)
        
        # Garden count
        self.gardens_label = ttk.Label(status_frame, text="Gardens: 0")
        self.gardens_label.pack(side='left', padx=20)
        
        # Active tasks count
        self.tasks_label = ttk.Label(status_frame, text="Active Tasks: 0")
        self.tasks_label.pack(side='left', padx=20)
    
    def create_tabs(self):
        """Create all application tabs"""
        
        # Dashboard Tab
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        self.create_dashboard_content(dashboard_frame)
        
        # Calendar Tab
        calendar_frame = ttk.Frame(self.notebook)
        self.notebook.add(calendar_frame, text="Master Calendar")
        self.create_calendar_content(calendar_frame)
        
        # Task Manager Tab
        tasks_frame = ttk.Frame(self.notebook)
        self.notebook.add(tasks_frame, text="Task Manager")
        self.create_tasks_content(tasks_frame)
        
        # Gardens Tab
        gardens_frame = ttk.Frame(self.notebook)
        self.notebook.add(gardens_frame, text="Gardens")
        self.create_gardens_content(gardens_frame)
        
        # Inventory Tab
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")
        self.create_inventory_content(inventory_frame)
        
        # Calculator Tab
        calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="Calculators")
        self.create_calculator_content(calc_frame)
        
        # Settings Tab
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        self.create_settings_content(settings_frame)
    
    def create_dashboard_content(self, parent):
        """Create dashboard tab content"""
        # Header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(header_frame, text="GrowMaster Pro Dashboard", 
                 font=('Arial', 16, 'bold')).pack(side='left')
        
        # Quick stats cards
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        self.create_stat_card(stats_frame, "Active Gardens", "0", "left")
        self.create_stat_card(stats_frame, "Today's Tasks", "0", "left")
        self.create_stat_card(stats_frame, "Plants Tracked", "0", "left")
        self.create_stat_card(stats_frame, "Days to Harvest", "--", "left")
        
        # Recent activity section
        activity_frame = ttk.LabelFrame(parent, text="Recent Activity", padding=10)
        activity_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Activity listbox with scrollbar
        activity_list_frame = ttk.Frame(activity_frame)
        activity_list_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(activity_list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.activity_listbox = tk.Listbox(activity_list_frame, 
                                          yscrollcommand=scrollbar.set,
                                          font=('Arial', 10))
        self.activity_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.activity_listbox.yview)
        
        # Add sample activities
        sample_activities = [
            "Garden 'Veg Room' created",
            "Task 'Water plants' completed",
            "New plant 'Tomato #1' added",
            "Harvest scheduled for next week"
        ]
        for activity in sample_activities:
            self.activity_listbox.insert('end', activity)
    
    def create_stat_card(self, parent, title, value, side):
        """Create a statistics card"""
        card = ttk.Frame(parent, style='Card.TFrame', padding=15)
        card.pack(side=side, padx=5, pady=5)
        
        ttk.Label(card, text=title, font=('Arial', 9)).pack()
        ttk.Label(card, text=value, font=('Arial', 18, 'bold'), 
                 foreground='#2196F3').pack()
    
    def create_calendar_content(self, parent):
        """Create calendar tab content"""
        ttk.Label(parent, text="Master Calendar View", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Calendar controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls_frame, text="← Previous", 
                  command=self.prev_month).pack(side='left')
        ttk.Label(controls_frame, text="August 2025", 
                 font=('Arial', 12, 'bold')).pack(side='left', padx=20)
        ttk.Button(controls_frame, text="Next →", 
                  command=self.next_month).pack(side='left')
        
        # Calendar grid (simplified)
        calendar_frame = ttk.Frame(parent)
        calendar_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(calendar_frame, text="Calendar view will be implemented here", 
                 font=('Arial', 12)).pack(expand=True)
    
    def create_tasks_content(self, parent):
        """Create task manager content"""
        ttk.Label(parent, text="Task Manager", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Task controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Add Task", 
                  command=self.add_task).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Complete Selected", 
                  command=self.complete_task).pack(side='left', padx=5)
        
        # Task list
        task_frame = ttk.Frame(parent)
        task_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for tasks
        columns = ('Priority', 'Task', 'Garden', 'Due Date', 'Status')
        self.task_tree = ttk.Treeview(task_frame, columns=columns, show='headings')
        
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=100)
        
        self.task_tree.pack(fill='both', expand=True)
        
        # Add sample tasks
        sample_tasks = [
            ('High', 'Water plants', 'Main Garden', '2025-08-25', 'Pending'),
            ('Medium', 'Check pH levels', 'Hydro Setup', '2025-08-26', 'Pending'),
            ('Low', 'Clean grow room', 'Veg Room', '2025-08-27', 'Pending')
        ]
        
        for i, task in enumerate(sample_tasks):
            self.task_tree.insert('', 'end', iid=i, values=task)
    
    def create_gardens_content(self, parent):
        """Create gardens management content"""
        ttk.Label(parent, text="Garden Management", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Garden controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(controls_frame, text="New Garden", 
                  command=self.new_garden).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Edit Garden", 
                  command=self.edit_garden).pack(side='left', padx=5)
        
        # Gardens list
        gardens_frame = ttk.LabelFrame(parent, text="Active Gardens", padding=10)
        gardens_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(gardens_frame, text="No gardens configured yet.", 
                 font=('Arial', 12)).pack(expand=True)
    
    def create_inventory_content(self, parent):
        """Create inventory management content"""
        ttk.Label(parent, text="Inventory Management", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Inventory categories
        categories_frame = ttk.Frame(parent)
        categories_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(categories_frame, text="Nutrients", 
                  command=self.show_nutrients).pack(side='left', padx=5)
        ttk.Button(categories_frame, text="Equipment", 
                  command=self.show_equipment).pack(side='left', padx=5)
        ttk.Button(categories_frame, text="Seeds/Clones", 
                  command=self.show_genetics).pack(side='left', padx=5)
        
        # Inventory display
        inventory_frame = ttk.Frame(parent)
        inventory_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(inventory_frame, text="Inventory tracking will be implemented here", 
                 font=('Arial', 12)).pack(expand=True)
    
    def create_calculator_content(self, parent):
        """Create calculators content"""
        ttk.Label(parent, text="Growing Calculators", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Calculator buttons
        calc_frame = ttk.Frame(parent)
        calc_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        calculators = [
            ("Nutrient Calculator", self.nutrient_calculator),
            ("Lighting Calculator", self.lighting_calculator),
            ("Cost Calculator", self.cost_calculator),
            ("Environmental Calculator", self.environmental_calculator)
        ]
        
        for i, (name, command) in enumerate(calculators):
            row = i // 2
            col = i % 2
            
            calc_button = ttk.Button(calc_frame, text=name, command=command)
            calc_button.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        
        calc_frame.grid_columnconfigure(0, weight=1)
        calc_frame.grid_columnconfigure(1, weight=1)
    
    def create_settings_content(self, parent):
        """Create settings content"""
        ttk.Label(parent, text="Application Settings", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        settings_frame = ttk.Frame(parent)
        settings_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sample settings
        ttk.Label(settings_frame, text="Theme:", font=('Arial', 10, 'bold')).pack(anchor='w')
        theme_var = tk.StringVar(value="Light")
        ttk.Combobox(settings_frame, textvariable=theme_var, 
                    values=["Light", "Dark"], state="readonly").pack(anchor='w', pady=5)
        
        ttk.Label(settings_frame, text="Default Units:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10,0))
        units_var = tk.StringVar(value="Metric")
        ttk.Combobox(settings_frame, textvariable=units_var, 
                    values=["Metric", "Imperial"], state="readonly").pack(anchor='w', pady=5)
    
    # Event handlers
    def new_garden(self):
        messagebox.showinfo("New Garden", "New Garden wizard will be implemented")
    
    def import_data(self):
        messagebox.showinfo("Import", "Data import feature coming soon")
    
    def export_data(self):
        messagebox.showinfo("Export", "Data export feature coming soon")
    
    def manage_gardens(self):
        messagebox.showinfo("Manage Gardens", "Garden management coming soon")
    
    def garden_settings(self):
        messagebox.showinfo("Garden Settings", "Garden settings coming soon")
    
    def open_calculators(self):
        self.notebook.select(5)  # Switch to calculators tab
    
    def generate_reports(self):
        messagebox.showinfo("Reports", "Report generation coming soon")
    
    def show_docs(self):
        messagebox.showinfo("Documentation", "Documentation coming soon")
    
    def show_about(self):
        messagebox.showinfo("About", "GrowMaster Pro v1.0\nProfessional Multi-Garden Management")
    
    def prev_month(self):
        print("Previous month clicked")
    
    def next_month(self):
        print("Next month clicked")
    
    def add_task(self):
        messagebox.showinfo("Add Task", "Add task dialog coming soon")
    
    def complete_task(self):
        selection = self.task_tree.selection()
        if selection:
            messagebox.showinfo("Complete Task", "Task marked as complete")
    
    def edit_garden(self):
        messagebox.showinfo("Edit Garden", "Garden editor coming soon")
    
    def show_nutrients(self):
        messagebox.showinfo("Nutrients", "Nutrient inventory coming soon")
    
    def show_equipment(self):
        messagebox.showinfo("Equipment", "Equipment inventory coming soon")
    
    def show_genetics(self):
        messagebox.showinfo("Genetics", "Genetics inventory coming soon")
    
    def nutrient_calculator(self):
        messagebox.showinfo("Nutrient Calculator", "Nutrient calculator coming soon")
    
    def lighting_calculator(self):
        messagebox.showinfo("Lighting Calculator", "Lighting calculator coming soon")
    
    def cost_calculator(self):
        messagebox.showinfo("Cost Calculator", "Cost calculator coming soon")
    
    def environmental_calculator(self):
        messagebox.showinfo("Environmental Calculator", "Environmental calculator coming soon")
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit GrowMaster Pro?"):
            logger.info("Application closing...")
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        logger.info("Starting main window...")
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
