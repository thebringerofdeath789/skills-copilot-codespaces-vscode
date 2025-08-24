"""Settings Tab - Application configuration and preferences"""

import customtkinter as ctk
import logging
from config.themes import themes

class SettingsTab:
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            parent,
            text="⚙️ Application Settings\n\nUser preferences and system configuration\nComing soon...",
            font=ctk.CTkFont(size=16)
        )
        label.grid(row=0, column=0, padx=20, pady=20)
