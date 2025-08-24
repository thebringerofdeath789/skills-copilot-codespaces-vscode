"""
Grow Plans Tab - Garden management interface
Template system for rapid grow plan creation and replication
"""

import customtkinter as ctk
import logging
from config.themes import themes

logger = logging.getLogger(__name__)

class GrowPlansTab:
    """Garden and grow plan management interface"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        self.create_interface()
    
    def create_interface(self):
        """Create grow plans interface"""
        # Main content area
        main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Title and description
        title_label = ctk.CTkLabel(
            main_frame,
            text="🌱 Garden & Grow Plan Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=20)
        
        description_label = ctk.CTkLabel(
            main_frame,
            text="Create, manage, and clone your garden setups and grow plans",
            font=ctk.CTkFont(size=14),
            text_color=themes.get_color("text_secondary")
        )
        description_label.grid(row=1, column=0, pady=(0, 30))
        
        # Development status
        status_frame = ctk.CTkFrame(main_frame, **themes.get_frame_styles()["card"])
        status_frame.grid(row=2, column=0, sticky="ew", pady=20, padx=50)
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="🚧 Under Development",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=themes.get_color("warning")
        )
        status_label.pack(pady=20)
        
        features_text = """
        Coming Soon:
        • Garden creation wizard with guided setup
        • Template library with pre-made grow plans
        • One-click grow plan cloning and modification
        • Garden comparison and performance analytics
        • Multi-garden resource coordination
        • Template sharing and import/export
        """
        
        features_label = ctk.CTkLabel(
            status_frame,
            text=features_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        features_label.pack(pady=(0, 20))
