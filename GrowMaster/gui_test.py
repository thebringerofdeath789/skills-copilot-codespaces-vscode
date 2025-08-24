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
