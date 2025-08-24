"""
GrowMaster Pro - Application Themes
Modern GUI themes using standard Tkinter and ttk
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class Themes:
    """Theme manager for consistent styling across the application"""
    
    def __init__(self):
        """Initialize theme system with default styles"""
        self.current_theme = "light"
        self.setup_themes()
        self.setup_ttk_styles()
    
    def setup_themes(self):
        """Define color schemes for different themes"""
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "select_bg": "#0078d4",
                "select_fg": "#ffffff",
                "border": "#cccccc",
                "accent": "#0078d4",
                "success": "#107c10",
                "warning": "#ff8c00",
                "error": "#d13438",
                "info": "#0078d4",
                "card_bg": "#f9f9f9",
                "header_bg": "#f0f0f0",
                "button_bg": "#e1e1e1",
                "button_hover": "#d0d0d0",
                "input_bg": "#ffffff",
                "tab_bg": "#f0f0f0",
                "tab_active": "#ffffff"
            },
            "dark": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "select_bg": "#0078d4",
                "select_fg": "#ffffff",
                "border": "#404040",
                "accent": "#4cc2ff",
                "success": "#6ccb5f",
                "warning": "#ffaa44",
                "error": "#ff6b6b",
                "info": "#4cc2ff",
                "card_bg": "#3c3c3c",
                "header_bg": "#404040",
                "button_bg": "#404040",
                "button_hover": "#505050",
                "input_bg": "#3c3c3c",
                "tab_bg": "#404040",
                "tab_active": "#2d2d2d"
            }
        }
        
        # Garden-specific color coding
        self.garden_colors = {
            "vegetative": "#4caf50",  # Green
            "flowering": "#ff9800",   # Orange
            "seedling": "#2196f3",    # Blue
            "harvest": "#9c27b0",     # Purple
            "maintenance": "#607d8b", # Blue Grey
            "planning": "#795548"     # Brown
        }
    
    def setup_ttk_styles(self):
        """Configure ttk widget styles"""
        style = ttk.Style()
        
        # Get current theme colors
        theme = self.get_current_theme()
        
        # Configure general styles
        style.configure('Card.TFrame', 
                       background=theme['card_bg'], 
                       borderwidth=1, 
                       relief='solid')
        
        style.configure('Header.TLabel', 
                       background=theme['header_bg'],
                       font=('Arial', 12, 'bold'))
        
        style.configure('Accent.TButton',
                       background=theme['accent'],
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background=theme['success'],
                       foreground='white')
        
        style.configure('Warning.TButton',
                       background=theme['warning'],
                       foreground='white')
        
        style.configure('Error.TButton',
                       background=theme['error'],
                       foreground='white')
    
    def get_current_theme(self) -> Dict[str, str]:
        """Get the current theme color dictionary"""
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_name: str):
        """Change the current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.setup_ttk_styles()
            logger.info(f"Theme changed to: {theme_name}")
        else:
            logger.warning(f"Theme not found: {theme_name}")
    
    def get_garden_color(self, garden_type: str) -> str:
        """Get color for specific garden type"""
        return self.garden_colors.get(garden_type, self.themes[self.current_theme]['accent'])
    
    def apply_card_style(self, frame: tk.Frame):
        """Apply card styling to a frame"""
        theme = self.get_current_theme()
        frame.configure(
            bg=theme['card_bg'],
            relief='solid',
            bd=1
        )
    
    def apply_button_style(self, button: tk.Button, style_type: str = 'default'):
        """Apply button styling"""
        theme = self.get_current_theme()
        
        style_configs = {
            'default': {
                'bg': theme['button_bg'],
                'fg': theme['fg'],
                'activebackground': theme['button_hover'],
                'activeforeground': theme['fg']
            },
            'accent': {
                'bg': theme['accent'],
                'fg': 'white',
                'activebackground': theme['accent'],
                'activeforeground': 'white'
            },
            'success': {
                'bg': theme['success'],
                'fg': 'white',
                'activebackground': theme['success'],
                'activeforeground': 'white'
            },
            'warning': {
                'bg': theme['warning'],
                'fg': 'white',
                'activebackground': theme['warning'],
                'activeforeground': 'white'
            },
            'error': {
                'bg': theme['error'],
                'fg': 'white',
                'activebackground': theme['error'],
                'activeforeground': 'white'
            }
        }
        
        if style_type in style_configs:
            config = style_configs[style_type]
            button.configure(**config)
    
    def get_status_color(self, status: str) -> str:
        """Get color based on status"""
        theme = self.get_current_theme()
        
        status_colors = {
            'active': theme['success'],
            'pending': theme['warning'],
            'completed': theme['success'],
            'overdue': theme['error'],
            'cancelled': theme['border'],
            'planning': theme['info']
        }
        
        return status_colors.get(status.lower(), theme['fg'])
    
    def get_priority_color(self, priority: str) -> str:
        """Get color based on priority level"""
        theme = self.get_current_theme()
        
        priority_colors = {
            'critical': theme['error'],
            'high': theme['warning'],
            'medium': theme['info'],
            'low': theme['success']
        }
        
        return priority_colors.get(priority.lower(), theme['fg'])

# Global theme manager instance
themes = Themes()
