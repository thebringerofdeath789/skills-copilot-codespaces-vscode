"""
GrowMaster Pro - Application Themes
Modern GUI themes using standard Tkinter with ttk styling
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class Themes:
    """Theme manager for consistent styling across the application"""
    
    def __init__(self):
        self.current_theme = "dark"
        self.style = None
        
        # Color palettes for different themes
        self.themes = {
            "dark": {
                "primary": "#1f538d",
                "secondary": "#14375e", 
                "accent": "#36719f",
                "background": "#212121",
                "surface": "#2b2b2b",
                "text_primary": "#ffffff",
                "text_secondary": "#b0b0b0",
                "success": "#4caf50",
                "warning": "#ff9800",
                "error": "#f44336",
                "info": "#2196f3"
            },
            "light": {
                "primary": "#1976d2",
                "secondary": "#1565c0",
                "accent": "#42a5f5",
                "background": "#f5f5f5",
                "surface": "#ffffff",
                "text_primary": "#212121",
                "text_secondary": "#757575",
                "success": "#4caf50",
                "warning": "#ff9800", 
                "error": "#f44336",
                "info": "#2196f3"
"""
GrowMaster Pro - Application Themes
Modern GUI themes using standard Tkinter with ttk styling
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class Themes:
    """Theme manager for consistent styling across the application"""
    
    def __init__(self):
        self.current_theme = "dark"
        self.style = None
        
        # Color palettes for different themes
        self.themes = {
            "dark": {
                "primary": "#1f538d",
                "secondary": "#14375e", 
                "accent": "#36719f",
                "background": "#212121",
                "surface": "#2b2b2b",
                "text_primary": "#ffffff",
                "text_secondary": "#b0b0b0",
                "success": "#4caf50",
                "warning": "#ff9800",
                "error": "#f44336",
                "info": "#2196f3"
            },
            "light": {
                "primary": "#1976d2",
                "secondary": "#1565c0",
                "accent": "#42a5f5",
                "background": "#f5f5f5",
                "surface": "#ffffff",
                "text_primary": "#212121",
                "text_secondary": "#757575",
                "success": "#4caf50",
                "warning": "#ff9800", 
                "error": "#f44336",
                "info": "#2196f3"
            }
        }
        
        # Garden-specific colors for multi-garden visualization
        self.garden_colors = [
            "#4caf50",  # Green
            "#2196f3",  # Blue
            "#ff9800",  # Orange
            "#9c27b0",  # Purple
            "#f44336",  # Red
            "#00bcd4",  # Cyan
            "#795548",  # Brown
            "#607d8b",  # Blue Grey
            "#e91e63",  # Pink
            "#ffeb3b"   # Yellow
        ]
        
        # Task priority colors
        self.priority_colors = {
            "critical": "#d32f2f",
            "high": "#f57c00",
            "medium": "#1976d2",
            "low": "#388e3c"
        }
        
        # Growth stage colors
        self.stage_colors = {
            "germination": "#8bc34a",
            "seedling": "#4caf50",
            "vegetative": "#009688",
            "flowering": "#ff9800",
            "harvest": "#795548",
            "curing": "#9e9e9e"
        }
        
    def setup_ttk_style(self, root):
        """Initialize ttk styling for consistent appearance"""
        self.style = ttk.Style(root)
        
        # Configure ttk styles based on current theme
        colors = self.themes[self.current_theme]
        
        # Configure the main theme
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Button styles
        self.style.configure('TButton',
                           background=colors["primary"],
                           foreground=colors["text_primary"],
                           borderwidth=1,
                           relief='flat',
                           padding=(10, 5))
        self.style.map('TButton',
                      background=[('active', colors["secondary"]),
                                ('pressed', colors["accent"])])
        
        # Frame styles
        self.style.configure('TFrame',
                           background=colors["surface"],
                           borderwidth=1,
                           relief='flat')
        
        # Label styles
        self.style.configure('TLabel',
                           background=colors["surface"],
                           foreground=colors["text_primary"])
        
        # Entry styles
        self.style.configure('TEntry',
                           fieldbackground=colors["background"],
                           borderwidth=1,
                           insertcolor=colors["text_primary"],
                           foreground=colors["text_primary"])
        
        # Notebook (Tab) styles
        self.style.configure('TNotebook',
                           background=colors["surface"],
                           borderwidth=0)
        self.style.configure('TNotebook.Tab',
                           background=colors["background"],
                           foreground=colors["text_primary"],
                           padding=[10, 5])
        self.style.map('TNotebook.Tab',
                      background=[('selected', colors["primary"]),
                                ('active', colors["accent"])])
    
    def get_color(self, color_name: str, theme: str = None) -> str:
        """Get a color value from the current theme"""
        theme = theme or self.current_theme
        return self.themes[theme].get(color_name, "#000000")
    
    def get_garden_color(self, garden_index: int) -> str:
        """Get a color for a specific garden based on index"""
        return self.garden_colors[garden_index % len(self.garden_colors)]
    
    def get_priority_color(self, priority: str) -> str:
        """Get color for task priority"""
        return self.priority_colors.get(priority.lower(), self.priority_colors["medium"])
    
    def get_stage_color(self, stage: str) -> str:
        """Get color for growth stage"""
        return self.stage_colors.get(stage.lower(), self.stage_colors["vegetative"])
    
    def set_theme(self, theme_name: str):
        """Switch between themes"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            if self.style:
                self.setup_ttk_style(self.style.master)
    
    def get_font_family(self) -> str:
        """Get default font family"""
        return "Segoe UI"
    
    def get_fonts(self) -> Dict[str, Tuple[str, int, str]]:
        """Get font specifications for different UI elements"""
        family = self.get_font_family()
        return {
            "title": (family, 24, "bold"),
            "heading": (family, 18, "bold"),
            "subheading": (family, 14, "bold"),
            "body": (family, 12, "normal"),
            "small": (family, 10, "normal"),
            "button": (family, 12, "bold"),
            "label": (family, 11, "normal")
        }
    
    def get_button_styles(self) -> Dict[str, Dict]:
        """Get button styling configurations for tkinter buttons"""
        colors = self.themes[self.current_theme]
        return {
            "primary": {
                "bg": colors["primary"],
                "fg": colors["text_primary"],
                "relief": "flat",
                "borderwidth": 0,
                "activebackground": colors["secondary"],
                "activeforeground": colors["text_primary"]
            },
            "secondary": {
                "bg": colors["surface"],
                "fg": colors["primary"],
                "relief": "solid",
                "borderwidth": 1,
                "highlightbackground": colors["primary"],
                "activebackground": colors["accent"],
                "activeforeground": colors["text_primary"]
            },
            "success": {
                "bg": colors["success"],
                "fg": "white",
                "relief": "flat",
                "borderwidth": 0,
                "activebackground": "#45a049",
                "activeforeground": "white"
            },
            "warning": {
                "bg": colors["warning"],
                "fg": "white",
                "relief": "flat",
                "borderwidth": 0,
                "activebackground": "#e68900",
                "activeforeground": "white"
            },
            "error": {
                "bg": colors["error"],
                "fg": "white",
                "relief": "flat",
                "borderwidth": 0,
                "activebackground": "#d32f2f",
                "activeforeground": "white"
            }
        }
    
    def get_frame_styles(self) -> Dict[str, Dict]:
        """Get frame styling configurations for tkinter frames"""
        colors = self.themes[self.current_theme]
        return {
            "default": {
                "bg": colors["surface"],
                "relief": "flat",
                "borderwidth": 0
            },
            "card": {
                "bg": colors["surface"],
                "relief": "solid",
                "borderwidth": 1,
                "highlightbackground": colors["accent"]
            },
            "panel": {
                "bg": colors["background"],
                "relief": "flat",
                "borderwidth": 0
            }
        }

# Global theme instance
themes = Themes()
