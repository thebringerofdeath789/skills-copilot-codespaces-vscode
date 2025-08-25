"""
GrowMaster Pro - New Garden Wizard
Complete guided setup for creating new hydroponic gardens
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Callable

logger = logging.getLogger(__name__)

class NewGrowWizard:
    """Complete guided wizard for creating new gardens with automation setup"""
    
    def __init__(self, parent, db_manager, callback: Optional[Callable] = None):
        self.parent = parent
        self.db_manager = db_manager
        self.callback = callback
        self.wizard_window = None
        self.current_step = 0
        self.garden_data = {}
        
        # Define wizard steps
        self.steps = [
            self.show_welcome_step,
            self.show_basic_info_step,
            self.show_growing_method_step,
            self.show_plant_selection_step,
            self.show_automation_setup_step,
            self.show_summary_step
        ]
        
        self.step_titles = [
            "Welcome",
            "Basic Information", 
            "Growing Method",
            "Plant Selection",
            "Automation Setup",
            "Summary"
        ]
    
    def show(self):
        """Display the wizard"""
        try:
            self.create_wizard_window()
            self.show_current_step()
        except Exception as e:
            logger.error(f"Error showing wizard: {e}")
            messagebox.showerror("Error", f"Failed to open wizard: {e}")
    
    def create_wizard_window(self):
        """Create the main wizard window"""
        self.wizard_window = ctk.CTkToplevel(self.parent)
        self.wizard_window.title("New Garden Wizard - GrowMaster Pro")
        self.wizard_window.geometry("800x650")
        self.wizard_window.resizable(False, False)
        
        # Center and configure window
        self.wizard_window.transient(self.parent)
        self.wizard_window.grab_set()
        
        # Main layout
        main_frame = ctk.CTkFrame(self.wizard_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Progress bar
        self.create_progress_bar(main_frame)
        
        # Content area
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Navigation buttons
        self.create_navigation_buttons(main_frame)
    
    def create_progress_bar(self, parent):
        """Create progress indicator"""
        progress_frame = ctk.CTkFrame(parent)
        progress_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        
        # Step indicator
        self.step_label = ctk.CTkLabel(
            progress_frame,
            text="Step 1 of 6: Welcome",
            font=("Arial", 12, "bold")
        )
        self.step_label.pack(pady=(0, 10))
        
        self.update_progress()
    
    def create_navigation_buttons(self, parent):
        """Create navigation button frame"""
        nav_frame = ctk.CTkFrame(parent)
        nav_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        # Buttons
        self.back_button = ctk.CTkButton(
            nav_frame,
            text="← Back",
            command=self.go_back,
            state="disabled",
            width=100
        )
        self.back_button.pack(side="left", padx=10, pady=10)
        
        self.cancel_button = ctk.CTkButton(
            nav_frame,
            text="Cancel",
            command=self.cancel_wizard,
            width=100
        )
        self.cancel_button.pack(side="right", padx=10, pady=10)
        
        self.next_button = ctk.CTkButton(
            nav_frame,
            text="Next →",
            command=self.go_next,
            width=100
        )
        self.next_button.pack(side="right", padx=(0, 10), pady=10)
    
    def update_progress(self):
        """Update progress bar and step indicator"""
        progress = (self.current_step + 1) / len(self.steps)
        self.progress_bar.set(progress)
        
        step_text = f"Step {self.current_step + 1} of {len(self.steps)}: {self.step_titles[self.current_step]}"
        self.step_label.configure(text=step_text)
        
        # Update navigation buttons
        self.back_button.configure(state="normal" if self.current_step > 0 else "disabled")
        
        if self.current_step == len(self.steps) - 1:
            self.next_button.configure(text="Create Garden")
        else:
            self.next_button.configure(text="Next →")
    
    def show_current_step(self):
        """Display the current step"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Update progress
        self.update_progress()
        
        # Show current step
        self.steps[self.current_step]()
    
    def cancel_wizard(self):
        """Cancel the wizard"""
        if messagebox.askyesno("Cancel Wizard", "Are you sure you want to cancel?\nYour progress will be lost."):
            self.wizard_window.destroy()
    
    def show_welcome_step(self):
        """Welcome screen"""
        welcome_frame = ctk.CTkFrame(self.content_frame)
        welcome_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            welcome_frame,
            text="🌱 Welcome to GrowMaster Pro!",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(40, 20))
        
        subtitle = ctk.CTkLabel(
            welcome_frame,
            text="Let's set up your automated hydroponic garden",
            font=("Arial", 14)
        )
        subtitle.pack(pady=10)
        
        features_text = """This wizard will help you:

• Choose the perfect growing method for your setup
• Select plants optimized for your experience level  
• Configure intelligent task automation
• Set up notifications and reminders
• Create a complete growing plan

The whole process takes just 5 minutes and sets up everything
you need for successful automated growing!"""
        
        features_label = ctk.CTkLabel(
            welcome_frame,
            text=features_text,
            font=("Arial", 12),
            justify="left"
        )
        features_label.pack(pady=30, padx=40)
        
        start_note = ctk.CTkLabel(
            welcome_frame,
            text="Click 'Next' to begin creating your automated garden",
            font=("Arial", 11, "italic")
        )
        start_note.pack(pady=20)
    
    def show_basic_info_step(self):
        """Basic garden information"""
        info_frame = ctk.CTkFrame(self.content_frame)
        info_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            info_frame,
            text="Basic Garden Information",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(30, 20))
        
        form_frame = ctk.CTkFrame(info_frame)
        form_frame.pack(fill="x", padx=40, pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Garden name
        name_label = ctk.CTkLabel(form_frame, text="Garden Name*:", font=("Arial", 12, "bold"))
        name_label.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        self.name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="e.g., Kitchen Herbs, Basement Greens",
            font=("Arial", 12)
        )
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=15, pady=15)
        if 'name' in self.garden_data:
            self.name_entry.insert(0, self.garden_data['name'])
        
        # Location
        location_label = ctk.CTkLabel(form_frame, text="Location:", font=("Arial", 12, "bold"))
        location_label.grid(row=1, column=0, sticky="w", padx=15, pady=15)
        
        self.location_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="e.g., Kitchen Counter, Grow Tent",
            font=("Arial", 12)
        )
        self.location_entry.grid(row=1, column=1, sticky="ew", padx=15, pady=15)
        if 'location' in self.garden_data:
            self.location_entry.insert(0, self.garden_data['location'])
        
        # Description
        desc_label = ctk.CTkLabel(form_frame, text="Description:", font=("Arial", 12, "bold"))
        desc_label.grid(row=2, column=0, sticky="nw", padx=15, pady=15)
        
        self.desc_text = ctk.CTkTextbox(form_frame, height=100, font=("Arial", 12))
        self.desc_text.grid(row=2, column=1, sticky="ew", padx=15, pady=15)
        if 'description' in self.garden_data:
            self.desc_text.insert("1.0", self.garden_data['description'])
    
    def show_growing_method_step(self):
        """Growing method selection"""
        method_frame = ctk.CTkFrame(self.content_frame)
        method_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            method_frame,
            text="Choose Your Growing Method",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(30, 10))
        
        subtitle = ctk.CTkLabel(
            method_frame,
            text="Select the hydroponic system that matches your space and experience",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 20))
        
        self.method_var = tk.StringVar(value=self.garden_data.get('growing_method', 'dwc'))
        
        methods = [
            ("dwc", "Deep Water Culture (DWC)", "🌊 Beginner-friendly, roots in nutrient solution"),
            ("nft", "Nutrient Film Technique (NFT)", "🌊 Continuous flow, perfect for leafy greens"), 
            ("ebb_flow", "Ebb & Flow", "🌊 Flood and drain system, very versatile"),
            ("drip", "Drip System", "💧 Precise delivery, great for larger plants"),
            ("aeroponics", "Aeroponics", "💨 Advanced misting system, fastest growth")
        ]
        
        for value, name, description in methods:
            method_radio = ctk.CTkRadioButton(
                method_frame,
                text=f"{name}\n{description}",
                variable=self.method_var,
                value=value,
                font=("Arial", 11)
            )
            method_radio.pack(pady=8, padx=50, anchor="w")
    
    def show_plant_selection_step(self):
        """Plant selection and configuration"""
        plant_frame = ctk.CTkFrame(self.content_frame)
        plant_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            plant_frame,
            text="What Would You Like to Grow?",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(30, 20))
        
        form_frame = ctk.CTkFrame(plant_frame)
        form_frame.pack(fill="x", padx=40, pady=20)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Plant type
        type_label = ctk.CTkLabel(form_frame, text="Plant Type*:", font=("Arial", 12, "bold"))
        type_label.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        self.plant_type_var = tk.StringVar(value=self.garden_data.get('plant_type', 'leafy_greens'))
        
        plant_options = [
            "Leafy Greens (Lettuce, Spinach, Kale)",
            "Herbs (Basil, Cilantro, Parsley)", 
            "Tomatoes & Peppers",
            "Strawberries",
            "Microgreens",
            "Other/Mixed"
        ]
        
        self.plant_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=self.plant_type_var,
            values=plant_options,
            font=("Arial", 12)
        )
        self.plant_dropdown.grid(row=0, column=1, sticky="ew", padx=15, pady=15)
        
        # Plant count
        count_label = ctk.CTkLabel(form_frame, text="Number of Plants*:", font=("Arial", 12, "bold"))
        count_label.grid(row=1, column=0, sticky="w", padx=15, pady=15)
        
        self.plant_count_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="e.g., 6, 12, 24",
            font=("Arial", 12),
            width=200
        )
        self.plant_count_entry.grid(row=1, column=1, sticky="w", padx=15, pady=15)
        if 'plant_count' in self.garden_data:
            self.plant_count_entry.insert(0, str(self.garden_data['plant_count']))
        
        # Experience level
        exp_label = ctk.CTkLabel(form_frame, text="Experience Level:", font=("Arial", 12, "bold"))
        exp_label.grid(row=2, column=0, sticky="w", padx=15, pady=15)
        
        self.experience_var = tk.StringVar(value=self.garden_data.get('experience_level', 'beginner'))
        
        exp_options = [
            "🌱 Beginner - New to hydroponics",
            "🌿 Intermediate - Some growing experience", 
            "🌳 Advanced - Experienced grower"
        ]
        
        for i, option in enumerate(exp_options):
            value = ['beginner', 'intermediate', 'advanced'][i]
            exp_radio = ctk.CTkRadioButton(
                form_frame,
                text=option,
                variable=self.experience_var,
                value=value,
                font=("Arial", 11)
            )
            exp_radio.grid(row=3+i, column=0, columnspan=2, sticky="w", padx=15, pady=5)
    
    def show_automation_setup_step(self):
        """Automation and scheduling setup"""
        auto_frame = ctk.CTkFrame(self.content_frame)
        auto_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            auto_frame,
            text="🤖 Automation Setup",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(30, 10))
        
        subtitle = ctk.CTkLabel(
            auto_frame,
            text="Configure intelligent automation features",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 20))
        
        options_frame = ctk.CTkFrame(auto_frame)
        options_frame.pack(fill="x", padx=40, pady=20)
        
        # Auto task generation
        self.auto_tasks_var = tk.BooleanVar(value=self.garden_data.get('auto_generate_tasks', True))
        auto_tasks_check = ctk.CTkCheckBox(
            options_frame,
            text="🎯 Auto-generate tasks based on plant growth stages",
            variable=self.auto_tasks_var,
            font=("Arial", 12, "bold")
        )
        auto_tasks_check.pack(pady=10, padx=20, anchor="w")
        
        auto_tasks_desc = ctk.CTkLabel(
            options_frame,
            text="   Automatically creates watering, feeding, and maintenance tasks",
            font=("Arial", 10),
            text_color=("gray", "lightgray")
        )
        auto_tasks_desc.pack(padx=20, anchor="w")
        
        # Notifications
        self.notifications_var = tk.BooleanVar(value=self.garden_data.get('notifications', True))
        notifications_check = ctk.CTkCheckBox(
            options_frame,
            text="🔔 Enable desktop notifications and reminders",
            variable=self.notifications_var,
            font=("Arial", 12, "bold")
        )
        notifications_check.pack(pady=10, padx=20, anchor="w")
        
        notifications_desc = ctk.CTkLabel(
            options_frame,
            text="   Get reminders for tasks, alerts for issues, and growth milestones",
            font=("Arial", 10),
            text_color=("gray", "lightgray")
        )
        notifications_desc.pack(padx=20, anchor="w")
    
    def show_summary_step(self):
        """Final summary and confirmation"""
        summary_frame = ctk.CTkFrame(self.content_frame)
        summary_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            summary_frame,
            text="🎉 Garden Setup Summary",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(30, 20))
        
        subtitle = ctk.CTkLabel(
            summary_frame,
            text="Please review your garden configuration",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 20))
        
        # Collect all data
        self.collect_current_data()
        
        # Summary display
        summary_text = f"""Garden Name: {self.garden_data.get('name', 'Not specified')}
Location: {self.garden_data.get('location', 'Not specified')}
Growing Method: {self.garden_data.get('growing_method', 'DWC').upper()}
Plant Type: {self.garden_data.get('plant_type', 'Not specified')}
Number of Plants: {self.garden_data.get('plant_count', 'Not specified')}
Experience Level: {self.garden_data.get('experience_level', 'Beginner').title()}

Automation Features:
• Auto-generate tasks: {'✅ Enabled' if self.garden_data.get('auto_generate_tasks', True) else '❌ Disabled'}
• Notifications: {'✅ Enabled' if self.garden_data.get('notifications', True) else '❌ Disabled'}"""
        
        summary_display = ctk.CTkTextbox(summary_frame, height=250, font=("Arial", 11))
        summary_display.pack(fill="both", expand=True, padx=40, pady=20)
        summary_display.insert("1.0", summary_text)
        summary_display.configure(state="disabled")
        
        # Final confirmation
        confirm_label = ctk.CTkLabel(
            summary_frame,
            text="✨ Ready to create your automated hydroponic garden!",
            font=("Arial", 12, "bold"),
            text_color=("green", "lightgreen")
        )
        confirm_label.pack(pady=15)
    
    def collect_current_data(self):
        """Collect data from current step"""
        try:
            if self.current_step == 1:  # Basic info
                self.garden_data['name'] = self.name_entry.get().strip()
                self.garden_data['location'] = self.location_entry.get().strip()
                self.garden_data['description'] = self.desc_text.get("1.0", "end-1c").strip()
            
            elif self.current_step == 2:  # Growing method
                self.garden_data['growing_method'] = self.method_var.get()
            
            elif self.current_step == 3:  # Plant selection
                self.garden_data['plant_type'] = self.plant_type_var.get()
                try:
                    self.garden_data['plant_count'] = int(self.plant_count_entry.get() or "6")
                except ValueError:
                    self.garden_data['plant_count'] = 6
                self.garden_data['experience_level'] = self.experience_var.get()
            
            elif self.current_step == 4:  # Automation setup
                self.garden_data['auto_generate_tasks'] = self.auto_tasks_var.get()
                self.garden_data['notifications'] = self.notifications_var.get()
                
        except Exception as e:
            logger.error(f"Error collecting data: {e}")
    
    def validate_current_step(self) -> bool:
        """Validate current step data"""
        if self.current_step == 1:  # Basic info validation
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("Required Field", "Please enter a garden name.")
                self.name_entry.focus()
                return False
        
        elif self.current_step == 3:  # Plant selection validation
            try:
                count = int(self.plant_count_entry.get() or "0")
                if count <= 0 or count > 200:
                    messagebox.showwarning("Invalid Number", "Please enter a valid number of plants (1-200).")
                    self.plant_count_entry.focus()
                    return False
            except ValueError:
                messagebox.showwarning("Invalid Number", "Please enter a valid number for plant count.")
                self.plant_count_entry.focus()
                return False
        
        return True
    
    def go_next(self):
        """Go to next step or create garden"""
        self.collect_current_data()
        
        if not self.validate_current_step():
            return
        
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            self.create_garden()
    
    def go_back(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.collect_current_data()
            self.current_step -= 1
            self.show_current_step()
    
    def create_garden(self):
        """Create the garden with full automation setup"""
        try:
            # Prepare complete garden data
            garden_data = {
                'name': self.garden_data.get('name', 'New Garden'),
                'description': self.garden_data.get('description', ''),
                'location': self.garden_data.get('location', ''),
                'growing_method': self.garden_data.get('growing_method', 'dwc'),
                'plant_type': self.garden_data.get('plant_type', 'leafy_greens'),
                'plant_count': self.garden_data.get('plant_count', 6),
                'experience_level': self.garden_data.get('experience_level', 'beginner'),
                'planted_date': datetime.now().isoformat(),
                'current_stage': 'germination',
                'stage_start_date': datetime.now().isoformat(),
                'is_active': True,
                'created_date': datetime.now().isoformat()
            }
            
            # Save to database
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO gardens (
                        name, description, location, growing_method, plant_type,
                        plant_count, planted_date, current_stage, stage_start_date,
                        is_active, created_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    garden_data['name'], garden_data['description'], garden_data['location'],
                    garden_data['growing_method'], garden_data['plant_type'],
                    garden_data['plant_count'], garden_data['planted_date'],
                    garden_data['current_stage'], garden_data['stage_start_date'],
                    garden_data['is_active'], garden_data['created_date']
                ))
                
                garden_id = cursor.lastrowid
                conn.commit()
            
            # Setup automation features
            self.setup_automation(garden_id)
            
            # Success message
            features_enabled = []
            if self.garden_data.get('auto_generate_tasks', True):
                features_enabled.append("• Automatic task generation")
            if self.garden_data.get('notifications', True):
                features_enabled.append("• Desktop notifications")
            
            features_text = "\n".join(features_enabled) if features_enabled else "• Manual management mode"
            
            messagebox.showinfo(
                "🎉 Garden Created Successfully!",
                f"Garden '{garden_data['name']}' has been created!\n\n"
                f"Automation features enabled:\n{features_text}\n\n"
                f"Your intelligent hydroponic garden is ready to go!"
            )
            
            # Close wizard and notify parent
            self.wizard_window.destroy()
            if self.callback:
                self.callback()
            
            logger.info(f"Successfully created automated garden: {garden_data['name']}")
            
        except Exception as e:
            logger.error(f"Error creating garden: {e}")
            messagebox.showerror("Error", f"Failed to create garden: {e}")
    
    def setup_automation(self, garden_id: int):
        """Setup automation features for the new garden"""
        try:
            # Generate initial tasks if enabled
            if self.garden_data.get('auto_generate_tasks', True):
                self.generate_initial_tasks(garden_id)
            
            # Setup notifications if enabled
            if self.garden_data.get('notifications', True):
                self.setup_notifications()
                
            logger.info(f"Automation setup completed for garden {garden_id}")
            
        except Exception as e:
            logger.error(f"Error setting up automation: {e}")
    
    def generate_initial_tasks(self, garden_id: int):
        """Generate initial automated tasks"""
        try:
            from core.schedulers.intelligent_task_generator import IntelligentTaskGenerator
            
            generator = IntelligentTaskGenerator(self.db_manager)
            tasks = generator.generate_tasks_for_garden(garden_id)
            
            logger.info(f"Generated {len(tasks)} initial tasks for garden {garden_id}")
            
        except ImportError:
            logger.warning("Intelligent task generator not available")
        except Exception as e:
            logger.error(f"Error generating initial tasks: {e}")
    
    def setup_notifications(self):
        """Setup notification system"""
        try:
            from core.schedulers.notification_system import BasicNotificationSystem
            
            notification_system = BasicNotificationSystem(self.db_manager)
            notification_system.create_notification_tables()
            
            logger.info("Notification system initialized")
            
        except ImportError:
            logger.warning("Notification system not available")
        except Exception as e:
            logger.error(f"Error setting up notifications: {e}")
