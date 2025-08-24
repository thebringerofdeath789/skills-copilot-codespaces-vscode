"""New Grow Wizard - Guided garden setup for new users"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import logging
from config.themes import themes

logger = logging.getLogger(__name__)

class NewGrowWizard:
    """Guided wizard for creating new garden setups"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        self.wizard_window = None
    
    def show(self):
        """Display the wizard dialog"""
        try:
            self.create_wizard_window()
            self.show_welcome_page()
        except Exception as e:
            logger.error(f"Failed to show wizard: {e}")
            messagebox.showerror("Error", f"Failed to open wizard: {e}")
    
    def create_wizard_window(self):
        """Create the wizard dialog window"""
        self.wizard_window = ctk.CTkToplevel(self.parent)
        self.wizard_window.title("New Garden Wizard")
        self.wizard_window.geometry("600x500")
        self.wizard_window.resizable(False, False)
        
        # Center the window
        self.wizard_window.transient(self.parent)
        self.wizard_window.grab_set()
        
        # Configure grid
        self.wizard_window.grid_columnconfigure(0, weight=1)
        self.wizard_window.grid_rowconfigure(0, weight=1)
        
        # Main content frame
        self.content_frame = ctk.CTkFrame(self.wizard_window)
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def show_welcome_page(self):
        """Show welcome page of wizard"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Welcome content
        welcome_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        welcome_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        welcome_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            welcome_frame,
            text="🌱 Welcome to GrowMaster Pro!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=themes.get_color("primary")
        )
        title_label.grid(row=0, column=0, pady=20)
        
        # Description
        desc_text = """
        Let's get you started with your first garden setup.
        
        This wizard will guide you through:
        • Selecting your growing method
        • Configuring your garden space
        • Setting up initial growing parameters
        • Creating your first grow plan
        
        The entire process takes just a few minutes!
        """
        
        desc_label = ctk.CTkLabel(
            welcome_frame,
            text=desc_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        desc_label.grid(row=1, column=0, pady=20, sticky="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        
        get_started_btn = ctk.CTkButton(
            button_frame,
            text="Get Started",
            width=200,
            height=40,
            command=self.show_method_selection,
            **themes.get_button_styles()["primary"]
        )
        get_started_btn.grid(row=0, column=0, pady=10)
        
        skip_btn = ctk.CTkButton(
            button_frame,
            text="Skip for Now",
            width=150,
            height=30,
            command=self.close_wizard,
            **themes.get_button_styles()["secondary"]
        )
        skip_btn.grid(row=1, column=0, pady=5)
    
    def show_method_selection(self):
        """Show growing method selection page"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Method selection content
        method_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        method_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        method_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            method_frame,
            text="Choose Your Growing Method",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=20)
        
        # Method options
        methods = [
            ("🏠 Indoor Soil", "Perfect for beginners, controlled environment"),
            ("🌊 Hydroponic DWC", "Fast growth, precise nutrient control"),
            ("🏡 Greenhouse", "Year-round growing, climate control"),
            ("🌞 Outdoor Soil", "Natural growing, seasonal cycles")
        ]
        
        self.selected_method = tk.StringVar(value="indoor_soil")
        
        for i, (name, description) in enumerate(methods):
            method_btn = ctk.CTkRadioButton(
                method_frame,
                text=f"{name}\\n{description}",
                variable=self.selected_method,
                value=name.lower().replace(" ", "_"),
                font=ctk.CTkFont(size=12)
            )
            method_btn.grid(row=i+1, column=0, sticky="w", pady=10, padx=20)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(method_frame, fg_color="transparent")
        nav_frame.grid(row=len(methods)+2, column=0, sticky="ew", pady=20)
        nav_frame.grid_columnconfigure(1, weight=1)
        
        back_btn = ctk.CTkButton(
            nav_frame,
            text="← Back",
            width=100,
            command=self.show_welcome_page,
            **themes.get_button_styles()["secondary"]
        )
        back_btn.grid(row=0, column=0, padx=5)
        
        next_btn = ctk.CTkButton(
            nav_frame,
            text="Next →",
            width=100,
            command=self.show_completion,
            **themes.get_button_styles()["primary"]
        )
        next_btn.grid(row=0, column=2, padx=5)
    
    def show_completion(self):
        """Show completion page"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Completion content
        completion_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        completion_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        completion_frame.grid_columnconfigure(0, weight=1)
        
        # Success message
        success_label = ctk.CTkLabel(
            completion_frame,
            text="🎉 Setup Complete!",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=themes.get_color("success")
        )
        success_label.grid(row=0, column=0, pady=20)
        
        # Summary
        method = getattr(self, 'selected_method', tk.StringVar(value="indoor_soil"))
        summary_text = f"""
        Great! Your garden setup is ready:
        
        Growing Method: {method.get().replace('_', ' ').title()}
        
        You can now:
        • View your dashboard for an overview
        • Start adding tasks to your calendar
        • Begin tracking costs and inventory
        • Document your growing progress
        
        Happy growing! 🌱
        """
        
        summary_label = ctk.CTkLabel(
            completion_frame,
            text=summary_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        summary_label.grid(row=1, column=0, pady=20)
        
        # Finish button
        finish_btn = ctk.CTkButton(
            completion_frame,
            text="Finish",
            width=200,
            height=40,
            command=self.close_wizard,
            **themes.get_button_styles()["success"]
        )
        finish_btn.grid(row=2, column=0, pady=20)
    
    def close_wizard(self):
        """Close the wizard dialog"""
        if self.wizard_window:
            self.wizard_window.destroy()
            logger.info("Garden wizard closed")
