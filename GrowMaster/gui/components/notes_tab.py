"""Notes Tab - Documentation and photo management"""

import customtkinter as ctk
import logging
from config.themes import themes

class NotesTab:
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        label = ctk.CTkLabel(
            parent,
            text="📝 Notes & Documentation\n\nPhoto galleries and rich text documentation\nComing soon...",
            font=ctk.CTkFont(size=16)
        )
        label.grid(row=0, column=0, padx=20, pady=20)
