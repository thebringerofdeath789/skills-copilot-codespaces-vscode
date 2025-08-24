"""
GrowMaster Pro - Application Themes
Modern GUI themes using standard Tkinter
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

import customtkinter as ctk
from typing import Dict, Tuple

class Themes:
    """Theme manager for consistent styling across the application"""
    
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
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
        
        self.current_theme = "dark"
    
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
            ctk.set_appearance_mode(theme_name)
    
    def get_font_family(self) -> str:
        """Get default font family"""
        return "Segoe UI"
    
    def get_fonts(self) -> Dict[str, Tuple[str, int]]:
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
        """Get button styling configurations"""
        return {
            "primary": {
                "fg_color": self.get_color("primary"),
                "hover_color": self.get_color("secondary"),
                "text_color": self.get_color("text_primary"),
                "border_width": 0,
                "corner_radius": 6
            },
            "secondary": {
                "fg_color": "transparent",
                "hover_color": self.get_color("surface"),
                "text_color": self.get_color("primary"),
                "border_width": 1,
                "border_color": self.get_color("primary"),
                "corner_radius": 6
            },
            "success": {
                "fg_color": self.get_color("success"),
                "hover_color": "#45a049",
                "text_color": "white",
                "border_width": 0,
                "corner_radius": 6
            },
            "warning": {
                "fg_color": self.get_color("warning"),
                "hover_color": "#e68900",
                "text_color": "white",
                "border_width": 0,
                "corner_radius": 6
            },
            "error": {
                "fg_color": self.get_color("error"),
                "hover_color": "#d32f2f",
                "text_color": "white",
                "border_width": 0,
                "corner_radius": 6
            }
        }
    
    def get_frame_styles(self) -> Dict[str, Dict]:
        """Get frame styling configurations"""
        return {
            "default": {
                "fg_color": self.get_color("surface"),
                "corner_radius": 10,
                "border_width": 0
            },
            "card": {
                "fg_color": self.get_color("surface"),
                "corner_radius": 12,
                "border_width": 1,
                "border_color": self.get_color("accent")
            },
            "panel": {
                "fg_color": self.get_color("background"),
                "corner_radius": 8,
                "border_width": 0
            }
        }

# Global theme instance
themes = Themes()
