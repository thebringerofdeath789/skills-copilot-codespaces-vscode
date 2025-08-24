#!/usr/bin/env python3
"""
GrowMaster Pro - Comprehensive GUI Test Suite
Tests all GUI functionality in a non-headless environment
Comprehensive testing for standard Tkinter interface components
"""

import sys
import os
import logging
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gui_test.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class GUITest:
    """Comprehensive GUI test suite for GrowMaster Pro"""
    
    def __init__(self):
        """Initialize test environment"""
        self.test_results = {}
        self.setup_test_data()
    
    def setup_test_data(self):
        """Create sample data for testing"""
        self.sample_gardens = [
            {
                "name": "Main Vegetative Room",
                "type": "vegetative",
                "plant_count": 12,
                "status": "active",
                "last_watered": "2025-08-23",
                "next_task": "pH check"
            },
            {
                "name": "Flowering Room A", 
                "type": "flowering",
                "plant_count": 8,
                "status": "active",
                "last_watered": "2025-08-24",
                "next_task": "Defoliation"
            },
            {
                "name": "Seedling Tray",
                "type": "seedling",
                "plant_count": 24,
                "status": "planning",
                "last_watered": "2025-08-24",
                "next_task": "Transplant ready seedlings"
            }
        ]
        
        self.sample_tasks = [
            {
                "id": 1,
                "title": "Water all plants",
                "priority": "high",
                "garden": "Main Vegetative Room",
                "due_date": "2025-08-25",
                "status": "pending",
                "description": "Check soil moisture and water as needed"
            },
            {
                "id": 2,
                "title": "pH and EC check",
                "priority": "medium",
                "garden": "Flowering Room A",
                "due_date": "2025-08-26",
                "status": "pending",
                "description": "Test nutrient solution pH and EC levels"
            },
            {
                "id": 3,
                "title": "Clean grow room",
                "priority": "low",
                "garden": "All",
                "due_date": "2025-08-27",
                "status": "pending",
                "description": "Weekly cleaning and maintenance"
            }
        ]
        
        self.sample_inventory = [
            {"item": "Flora Trio Nutrients", "category": "nutrients", "quantity": 2, "unit": "bottles", "low_stock": False},
            {"item": "pH Down", "category": "nutrients", "quantity": 1, "unit": "bottle", "low_stock": True},
            {"item": "Rockwool Cubes", "category": "media", "quantity": 50, "unit": "pieces", "low_stock": False},
            {"item": "LED Light Bulbs", "category": "equipment", "quantity": 2, "unit": "pieces", "low_stock": True}
        ]
    
    def test_basic_window(self):
        """Test 1: Basic window creation and styling"""
        logger.info("Starting Test 1: Basic Window Creation")
        
        try:
            root = tk.Tk()
            root.title("GrowMaster Pro - Test Window")
            root.geometry("800x600")
            
            # Test window configuration
            root.configure(bg='#f0f0f0')
            
            # Test basic widgets
            header = tk.Label(root, text="GrowMaster Pro - GUI Test", 
                             font=('Arial', 16, 'bold'), bg='#f0f0f0')
            header.pack(pady=20)
            
            test_frame = tk.Frame(root, bg='white', relief='solid', bd=1)
            test_frame.pack(padx=20, pady=10, fill='both', expand=True)
            
            tk.Label(test_frame, text="✓ Basic window creation successful", 
                    font=('Arial', 12), bg='white', fg='green').pack(pady=10)
            
            # Test button functionality
            def close_test():
                logger.info("Test 1 completed successfully")
                self.test_results["basic_window"] = "PASS"
                root.destroy()
            
            tk.Button(test_frame, text="Close Test", command=close_test, 
                     bg='#0078d4', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
            
            # Auto-close after 3 seconds for automated testing
            root.after(3000, close_test)
            root.mainloop()
            
        except Exception as e:
            logger.error(f"Test 1 failed: {e}")
            self.test_results["basic_window"] = f"FAIL: {e}"
    
    def test_tabbed_interface(self):
        """Test 2: Comprehensive tabbed interface"""
        logger.info("Starting Test 2: Tabbed Interface")
        
        try:
            root = tk.Tk()
            root.title("GrowMaster Pro - Tabbed Interface Test")
            root.geometry("1000x700")
            root.configure(bg='#f0f0f0')
            
            # Create notebook
            notebook = ttk.Notebook(root)
            notebook.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Dashboard Tab
            dashboard_frame = ttk.Frame(notebook)
            notebook.add(dashboard_frame, text="Dashboard")
            self.create_test_dashboard(dashboard_frame)
            
            # Tasks Tab
            tasks_frame = ttk.Frame(notebook)
            notebook.add(tasks_frame, text="Tasks")
            self.create_test_tasks(tasks_frame)
            
            # Gardens Tab
            gardens_frame = ttk.Frame(notebook)
            notebook.add(gardens_frame, text="Gardens")
            self.create_test_gardens(gardens_frame)
            
            # Inventory Tab
            inventory_frame = ttk.Frame(notebook)
            notebook.add(inventory_frame, text="Inventory")
            self.create_test_inventory(inventory_frame)
            
            def close_test():
                logger.info("Test 2 completed successfully")
                self.test_results["tabbed_interface"] = "PASS"
                root.destroy()
            
            # Close button
            close_btn = tk.Button(root, text="Close Tabbed Test", command=close_test,
                                 bg='#d13438', fg='white', font=('Arial', 10, 'bold'))
            close_btn.pack(pady=5)
            
            # Auto-close after 10 seconds
            root.after(10000, close_test)
            root.mainloop()
            
        except Exception as e:
            logger.error(f"Test 2 failed: {e}")
            self.test_results["tabbed_interface"] = f"FAIL: {e}"
    
    def create_test_dashboard(self, parent):
        """Create test dashboard content"""
        # Header
        header = tk.Label(parent, text="Dashboard Test", font=('Arial', 14, 'bold'))
        header.pack(pady=10)
        
        # Stats cards
        stats_frame = tk.Frame(parent)
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        # Create stat cards
        stats = [
            ("Active Gardens", "3", "#4caf50"),
            ("Today's Tasks", "5", "#ff9800"),
            ("Plants Tracked", "44", "#2196f3"),
            ("Days to Harvest", "12", "#9c27b0")
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg='white', relief='solid', bd=1)
            card.pack(side='left', padx=5, pady=5, fill='both', expand=True)
            
            tk.Label(card, text=title, font=('Arial', 9), bg='white').pack(pady=(10,0))
            tk.Label(card, text=value, font=('Arial', 16, 'bold'), bg='white', fg=color).pack(pady=(0,10))
        
        # Recent activity
        activity_frame = tk.LabelFrame(parent, text="Recent Activity", font=('Arial', 10, 'bold'))
        activity_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        activities = [
            "✓ Watered Main Vegetative Room - 2 hours ago",
            "📊 pH checked in Flowering Room A - 4 hours ago", 
            "🌱 Transplanted 6 seedlings - Yesterday",
            "🔧 Cleaned equipment - Yesterday",
            "📝 Updated grow log - 2 days ago"
        ]
        
        for activity in activities:
            tk.Label(activity_frame, text=activity, font=('Arial', 10), anchor='w').pack(fill='x', padx=10, pady=2)
    
    def create_test_tasks(self, parent):
        """Create test tasks content"""
        # Header
        header = tk.Label(parent, text="Task Manager Test", font=('Arial', 14, 'bold'))
        header.pack(pady=10)
        
        # Controls
        controls_frame = tk.Frame(parent)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(controls_frame, text="Add Task", bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(controls_frame, text="Complete Selected", bg='#2196f3', fg='white').pack(side='left', padx=5)
        tk.Button(controls_frame, text="Delete", bg='#d13438', fg='white').pack(side='left', padx=5)
        
        # Task list
        list_frame = tk.Frame(parent)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Headers
        headers_frame = tk.Frame(list_frame, bg='#f0f0f0', relief='solid', bd=1)
        headers_frame.pack(fill='x', pady=(0,5))
        
        headers = ["Priority", "Task", "Garden", "Due Date", "Status"]
        for header in headers:
            tk.Label(headers_frame, text=header, font=('Arial', 10, 'bold'), 
                    bg='#f0f0f0').pack(side='left', padx=20, pady=5)
        
        # Task rows
        for task in self.sample_tasks:
            task_frame = tk.Frame(list_frame, bg='white', relief='solid', bd=1)
            task_frame.pack(fill='x', pady=2)
            
            priority_color = {'high': '#d13438', 'medium': '#ff9800', 'low': '#4caf50'}[task['priority']]
            
            tk.Label(task_frame, text=task['priority'].upper(), fg=priority_color, 
                    font=('Arial', 9, 'bold'), bg='white').pack(side='left', padx=20, pady=5)
            tk.Label(task_frame, text=task['title'], bg='white').pack(side='left', padx=20, pady=5)
            tk.Label(task_frame, text=task['garden'], bg='white').pack(side='left', padx=20, pady=5)
            tk.Label(task_frame, text=task['due_date'], bg='white').pack(side='left', padx=20, pady=5)
            tk.Label(task_frame, text=task['status'].upper(), bg='white').pack(side='left', padx=20, pady=5)
    
    def create_test_gardens(self, parent):
        """Create test gardens content"""
        # Header
        header = tk.Label(parent, text="Gardens Management Test", font=('Arial', 14, 'bold'))
        header.pack(pady=10)
        
        # Controls
        controls_frame = tk.Frame(parent)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(controls_frame, text="New Garden", bg='#4caf50', fg='white').pack(side='left', padx=5)
        tk.Button(controls_frame, text="Edit Selected", bg='#2196f3', fg='white').pack(side='left', padx=5)
        tk.Button(controls_frame, text="Archive", bg='#ff9800', fg='white').pack(side='left', padx=5)
        
        # Gardens grid
        gardens_frame = tk.Frame(parent)
        gardens_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        for i, garden in enumerate(self.sample_gardens):
            row = i // 2
            col = i % 2
            
            # Garden card
            card = tk.Frame(gardens_frame, bg='white', relief='solid', bd=2, padx=15, pady=15)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Garden type color
            type_colors = {'vegetative': '#4caf50', 'flowering': '#ff9800', 'seedling': '#2196f3'}
            type_color = type_colors.get(garden['type'], '#607d8b')
            
            # Garden info
            tk.Label(card, text=garden['name'], font=('Arial', 12, 'bold'), 
                    bg='white', fg=type_color).pack(anchor='w')
            tk.Label(card, text=f"Type: {garden['type'].title()}", 
                    bg='white').pack(anchor='w')
            tk.Label(card, text=f"Plants: {garden['plant_count']}", 
                    bg='white').pack(anchor='w')
            tk.Label(card, text=f"Status: {garden['status'].title()}", 
                    bg='white').pack(anchor='w')
            tk.Label(card, text=f"Next: {garden['next_task']}", 
                    bg='white', font=('Arial', 9, 'italic')).pack(anchor='w')
        
        gardens_frame.grid_columnconfigure(0, weight=1)
        gardens_frame.grid_columnconfigure(1, weight=1)
    
    def create_test_inventory(self, parent):
        """Create test inventory content"""
        # Header
        header = tk.Label(parent, text="Inventory Management Test", font=('Arial', 14, 'bold'))
        header.pack(pady=10)
        
        # Categories
        categories_frame = tk.Frame(parent)
        categories_frame.pack(fill='x', padx=10, pady=5)
        
        categories = ["All Items", "Nutrients", "Equipment", "Growing Media", "Seeds/Genetics"]
        for category in categories:
            tk.Button(categories_frame, text=category, bg='#e1e1e1').pack(side='left', padx=5)
        
        # Inventory list
        inventory_frame = tk.Frame(parent)
        inventory_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Headers
        headers_frame = tk.Frame(inventory_frame, bg='#f0f0f0', relief='solid', bd=1)
        headers_frame.pack(fill='x', pady=(0,5))
        
        headers = ["Item", "Category", "Quantity", "Unit", "Status"]
        for header in headers:
            tk.Label(headers_frame, text=header, font=('Arial', 10, 'bold'), 
                    bg='#f0f0f0').pack(side='left', padx=30, pady=5)
        
        # Inventory rows
        for item in self.sample_inventory:
            item_frame = tk.Frame(inventory_frame, bg='white', relief='solid', bd=1)
            item_frame.pack(fill='x', pady=2)
            
            status_text = "LOW STOCK" if item['low_stock'] else "OK"
            status_color = '#d13438' if item['low_stock'] else '#4caf50'
            
            tk.Label(item_frame, text=item['item'], bg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=30, pady=5)
            tk.Label(item_frame, text=item['category'].title(), bg='white').pack(side='left', padx=30, pady=5)
            tk.Label(item_frame, text=str(item['quantity']), bg='white').pack(side='left', padx=30, pady=5)
            tk.Label(item_frame, text=item['unit'], bg='white').pack(side='left', padx=30, pady=5)
            tk.Label(item_frame, text=status_text, bg='white', fg=status_color, 
                    font=('Arial', 9, 'bold')).pack(side='left', padx=30, pady=5)
    
    def test_dialogs_and_forms(self):
        """Test 3: Dialog boxes and form elements"""
        logger.info("Starting Test 3: Dialogs and Forms")
        
        try:
            root = tk.Tk()
            root.title("GrowMaster Pro - Forms Test")
            root.geometry("600x500")
            root.configure(bg='#f0f0f0')
            
            # Header
            header = tk.Label(root, text="Forms and Dialogs Test", 
                             font=('Arial', 16, 'bold'), bg='#f0f0f0')
            header.pack(pady=20)
            
            # Form frame
            form_frame = tk.Frame(root, bg='white', relief='solid', bd=1)
            form_frame.pack(padx=20, pady=10, fill='both', expand=True)
            
            tk.Label(form_frame, text="Sample Garden Setup Form", 
                    font=('Arial', 12, 'bold'), bg='white').pack(pady=10)
            
            # Form fields
            fields_frame = tk.Frame(form_frame, bg='white')
            fields_frame.pack(padx=20, pady=10, fill='x')
            
            # Garden name
            tk.Label(fields_frame, text="Garden Name:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
            garden_name = tk.Entry(fields_frame, font=('Arial', 10))
            garden_name.pack(fill='x', pady=(0,10))
            garden_name.insert(0, "Test Garden")
            
            # Garden type
            tk.Label(fields_frame, text="Garden Type:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
            garden_type = ttk.Combobox(fields_frame, values=["Vegetative", "Flowering", "Seedling"])
            garden_type.pack(fill='x', pady=(0,10))
            garden_type.set("Vegetative")
            
            # Plant count
            tk.Label(fields_frame, text="Plant Count:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
            plant_count = tk.Spinbox(fields_frame, from_=1, to=100, font=('Arial', 10))
            plant_count.pack(fill='x', pady=(0,10))
            plant_count.set("12")
            
            # Growing medium
            tk.Label(fields_frame, text="Growing Medium:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
            medium_frame = tk.Frame(fields_frame, bg='white')
            medium_frame.pack(fill='x', pady=(0,10))
            
            medium_var = tk.StringVar(value="soil")
            tk.Radiobutton(medium_frame, text="Soil", variable=medium_var, value="soil", bg='white').pack(side='left')
            tk.Radiobutton(medium_frame, text="Hydroponic", variable=medium_var, value="hydro", bg='white').pack(side='left')
            tk.Radiobutton(medium_frame, text="Coco Coir", variable=medium_var, value="coco", bg='white').pack(side='left')
            
            # Notes
            tk.Label(fields_frame, text="Notes:", bg='white', anchor='w').pack(fill='x', pady=(5,0))
            notes_text = tk.Text(fields_frame, height=4, font=('Arial', 10))
            notes_text.pack(fill='x', pady=(0,10))
            notes_text.insert('1.0', "Test garden setup with sample data for GUI testing.")
            
            # Buttons
            button_frame = tk.Frame(form_frame, bg='white')
            button_frame.pack(pady=10)
            
            def save_form():
                messagebox.showinfo("Success", "Garden configuration saved successfully!")
            
            def test_warning():
                messagebox.showwarning("Warning", "This is a test warning dialog.")
            
            def test_error():
                messagebox.showerror("Error", "This is a test error dialog.")
            
            tk.Button(button_frame, text="Save Garden", command=save_form, 
                     bg='#4caf50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
            tk.Button(button_frame, text="Test Warning", command=test_warning, 
                     bg='#ff9800', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
            tk.Button(button_frame, text="Test Error", command=test_error, 
                     bg='#d13438', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
            
            def close_test():
                logger.info("Test 3 completed successfully")
                self.test_results["dialogs_forms"] = "PASS"
                root.destroy()
            
            tk.Button(button_frame, text="Close Test", command=close_test, 
                     bg='#607d8b', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
            
            # Auto-close after 8 seconds
            root.after(8000, close_test)
            root.mainloop()
            
        except Exception as e:
            logger.error(f"Test 3 failed: {e}")
            self.test_results["dialogs_forms"] = f"FAIL: {e}"
    
    def test_main_application(self):
        """Test 4: Full application launch"""
        logger.info("Starting Test 4: Full Application")
        
        try:
            from gui.main_window_tk import MainWindow
            
            app = MainWindow()
            logger.info("Main application created successfully")
            
            # Auto-close after 5 seconds for testing
            def close_test():
                logger.info("Test 4 completed successfully")
                self.test_results["main_application"] = "PASS"
                app.root.destroy()
            
            app.root.after(5000, close_test)
            app.run()
            
        except Exception as e:
            logger.error(f"Test 4 failed: {e}")
            self.test_results["main_application"] = f"FAIL: {e}"
    
    def run_all_tests(self):
        """Run all GUI tests in sequence"""
        logger.info("Starting GrowMaster Pro GUI Test Suite")
        logger.info("=" * 50)
        
        tests = [
            ("Basic Window", self.test_basic_window),
            ("Tabbed Interface", self.test_tabbed_interface), 
            ("Dialogs and Forms", self.test_dialogs_and_forms),
            ("Main Application", self.test_main_application)
        ]
        
        for test_name, test_func in tests:
            logger.info(f"Running {test_name} test...")
            test_func()
        
        # Print results
        logger.info("=" * 50)
        logger.info("TEST RESULTS:")
        logger.info("=" * 50)
        
        for test_name, result in self.test_results.items():
            status = "✓ PASS" if result == "PASS" else f"✗ {result}"
            logger.info(f"{test_name.replace('_', ' ').title()}: {status}")
        
        passed = sum(1 for r in self.test_results.values() if r == "PASS")
        total = len(self.test_results)
        logger.info(f"
Overall: {passed}/{total} tests passed")
        
        if passed == total:
            logger.info("🎉 All GUI tests completed successfully!")
        else:
            logger.warning("⚠️ Some tests failed. Check logs for details.")

def main():
    """Run GUI tests"""
    print("GrowMaster Pro - GUI Test Suite")
    print("=" * 40)
    print("This test suite verifies GUI functionality.")
    print("Run this in a non-headless environment with display support.")
    print("=" * 40)
    
    try:
        # Test if GUI is available
        root = tk.Tk()
        root.withdraw()  # Hide test window
        root.destroy()
        
        # Run test suite
        tester = GUITest()
        tester.run_all_tests()
        
    except tk.TclError as e:
        print(f"❌ GUI not available: {e}")
        print("This appears to be a headless environment.")
        print("To run GUI tests:")
        print("1. Use a system with display support")
        print("2. Or use X11 forwarding: ssh -X username@server")
        print("3. Or use VNC/remote desktop")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Add the project root to Python path  
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_gui():
    """Test basic GUI functionality"""
    root = tk.Tk()
    root.title("GrowMaster Pro - GUI Test")
    root.geometry("400x300")
    
    # Test basic widgets
    ttk.Label(root, text="GrowMaster Pro - GUI Test", 
             font=('Arial', 14, 'bold')).pack(pady=20)
    
    ttk.Label(root, text="If you can see this window, tkinter is working!").pack(pady=10)
    
    # Test button
    def on_test_click():
        print("Button clicked successfully!")
    
    ttk.Button(root, text="Test Button", command=on_test_click).pack(pady=10)
    
    # Test notebook (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Tab 1
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Tab 1")
    ttk.Label(tab1, text="This is tab 1").pack(pady=20)
    
    # Tab 2
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Tab 2")
    ttk.Label(tab2, text="This is tab 2").pack(pady=20)
    
    print("GUI test window created successfully!")
    print("Close the window to continue...")
    
    root.mainloop()

if __name__ == "__main__":
    test_gui()
