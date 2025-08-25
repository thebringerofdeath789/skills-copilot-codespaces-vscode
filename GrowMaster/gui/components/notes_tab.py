"""Notes Tab - Documentation and photo management"""

import customtkinter as ctk
import logging
from tkinter import messagebox, filedialog
from datetime import datetime, date
import os
from pathlib import Path

from config.themes import themes
from core.database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class NotesTab:
    """Comprehensive notes and documentation management interface"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        self.db_manager = DatabaseManager()
        self.notes_data = []
        self.photos_data = []
        self.selected_note = None
        self.selected_photo = None
        
        # Configure parent frame
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.main_container = ctk.CTkFrame(parent)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        self.create_interface()
        self.load_data()
    
    def create_interface(self):
        """Create the notes interface"""
        
        # Header with tabs
        header_frame = ctk.CTkFrame(self.main_container, **themes.get_frame_styles()["card"])
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📝 Notes & Documentation",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        # Tab buttons
        tab_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        tab_frame.pack(side="right", padx=15, pady=10)
        
        self.current_tab = "notes"  # Default tab
        
        notes_btn = ctk.CTkButton(
            tab_frame,
            text="📝 Notes",
            command=lambda: self.switch_tab("notes"),
            **themes.get_button_styles()["primary"]
        )
        notes_btn.pack(side="left", padx=5)
        
        photos_btn = ctk.CTkButton(
            tab_frame,
            text="📷 Photos",
            command=lambda: self.switch_tab("photos"),
            **themes.get_button_styles()["secondary"]
        )
        photos_btn.pack(side="left", padx=5)
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Initially show notes tab
        self.show_notes_tab()
    
    def switch_tab(self, tab_name):
        """Switch between notes and photos tabs"""
        self.current_tab = tab_name
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if tab_name == "notes":
            self.show_notes_tab()
        else:
            self.show_photos_tab()
        
        logger.info(f"Switched to {tab_name} tab")
    
    def show_notes_tab(self):
        """Show notes management interface"""
        notes_container = ctk.CTkFrame(self.content_frame)
        notes_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        notes_container.grid_columnconfigure(1, weight=1)
        notes_container.grid_rowconfigure(0, weight=1)
        
        # Left: Notes list
        left_panel = ctk.CTkFrame(notes_container, **themes.get_frame_styles()["card"])
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=0)
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)
        
        # Notes list header
        list_header = ctk.CTkFrame(left_panel, fg_color="transparent")
        list_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        list_header.grid_columnconfigure(0, weight=1)
        
        notes_title = ctk.CTkLabel(list_header, text="📋 Garden Notes", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        notes_title.grid(row=0, column=0, sticky="w")
        
        add_note_btn = ctk.CTkButton(
            list_header,
            text="➕ Add Note",
            width=100,
            command=self.add_new_note,
            **themes.get_button_styles()["primary"]
        )
        add_note_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Notes list
        self.notes_list_frame = ctk.CTkScrollableFrame(left_panel)
        self.notes_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Right: Note details/editor
        self.right_panel = ctk.CTkFrame(notes_container, **themes.get_frame_styles()["card"])
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(2, 0), pady=0)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        self.show_note_editor()
    
    def show_photos_tab(self):
        """Show photos management interface"""
        photos_container = ctk.CTkFrame(self.content_frame)
        photos_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        photos_container.grid_columnconfigure(0, weight=1)
        photos_container.grid_rowconfigure(1, weight=1)
        
        # Header with actions
        photos_header = ctk.CTkFrame(photos_container, fg_color="transparent")
        photos_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        photos_header.grid_columnconfigure(0, weight=1)
        
        photos_title = ctk.CTkLabel(photos_header, text="📷 Photo Gallery", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        photos_title.grid(row=0, column=0, sticky="w")
        
        add_photo_btn = ctk.CTkButton(
            photos_header,
            text="📸 Add Photos",
            command=self.add_photos,
            **themes.get_button_styles()["primary"]
        )
        add_photo_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Photos grid
        self.photos_grid_frame = ctk.CTkScrollableFrame(photos_container)
        self.photos_grid_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.load_photos()
    
    def show_note_editor(self):
        """Show note editor interface"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        editor_frame = ctk.CTkScrollableFrame(self.right_panel, label_text="Note Editor")
        editor_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Note title
        title_frame = ctk.CTkFrame(editor_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(title_frame, text="Title:", width=80).pack(side="left")
        self.note_title_var = ctk.StringVar()
        title_entry = ctk.CTkEntry(title_frame, textvariable=self.note_title_var, width=300)
        title_entry.pack(side="left", padx=(10, 0), expand=True, fill="x")
        
        # Associated garden/plant
        association_frame = ctk.CTkFrame(editor_frame, fg_color="transparent")
        association_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(association_frame, text="Garden:", width=80).pack(side="left")
        self.garden_var = ctk.StringVar(value="General Notes")
        garden_dropdown = ctk.CTkOptionMenu(
            association_frame,
            variable=self.garden_var,
            values=["General Notes", "Indoor Garden", "Outdoor Garden", "Greenhouse"]
        )
        garden_dropdown.pack(side="left", padx=(10, 0))
        
        # Note content
        content_label = ctk.CTkLabel(editor_frame, text="Content:", font=ctk.CTkFont(weight="bold"))
        content_label.pack(anchor="w", padx=5, pady=(10, 5))
        
        self.note_content = ctk.CTkTextbox(editor_frame, height=300)
        self.note_content.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Action buttons
        button_frame = ctk.CTkFrame(editor_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=5, pady=10)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Note",
            command=self.save_note,
            **themes.get_button_styles()["primary"]
        )
        save_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_note_editor,
            **themes.get_button_styles()["secondary"]
        )
        clear_btn.pack(side="left", padx=5)
        
        if self.selected_note:
            delete_btn = ctk.CTkButton(
                button_frame,
                text="❌ Delete",
                command=self.delete_note,
                **themes.get_button_styles()["danger"]
            )
            delete_btn.pack(side="left", padx=5)
        
        # Load selected note if any
        if self.selected_note:
            self.load_note_into_editor()
    
    def load_data(self):
        """Load notes and photos data"""
        self.load_notes()
        self.load_photos()
    
    def load_notes(self):
        """Load notes from various database tables"""
        try:
            self.notes_data = []
            
            with self.db_manager.get_connection() as conn:
                # Get standalone notes from notes table
                cursor = conn.execute("""
                    SELECT id, title, content, category, created_date, modified_date, is_pinned
                    FROM notes 
                    WHERE is_archived = FALSE
                    ORDER BY is_pinned DESC, modified_date DESC
                """)
                for row in cursor.fetchall():
                    self.notes_data.append({
                        "id": row[0],
                        "type": "Standalone",
                        "title": row[1],
                        "content": row[2],
                        "category": row[3],
                        "date": row[5] or row[4],  # Use modified_date or created_date
                        "is_pinned": bool(row[6])
                    })
                
                # Get garden notes (existing functionality)
                cursor = conn.execute("""
                    SELECT 'garden' as type, id, name as title, notes, created_date
                    FROM gardens 
                    WHERE notes IS NOT NULL AND notes != ''
                """)
                for row in cursor.fetchall():
                    self.notes_data.append({
                        "id": f"garden_{row[1]}",
                        "type": "Garden",
                        "title": f"Garden: {row[2]}",
                        "content": row[3],
                        "date": row[4] or datetime.now().isoformat(),
                        "source_id": row[1],
                        "is_pinned": False
                    })
                
                # Get plant notes (existing functionality)
                cursor = conn.execute("""
                    SELECT 'plant' as type, id, plant_name as title, notes, created_date
                    FROM plants 
                    WHERE notes IS NOT NULL AND notes != ''
                """)
                for row in cursor.fetchall():
                    self.notes_data.append({
                        "id": f"plant_{row[1]}",
                        "type": "Plant",
                        "title": f"Plant: {row[2]}",
                        "content": row[3],
                        "date": row[4] or datetime.now().isoformat(),
                        "source_id": row[1],
                        "is_pinned": False
                    })
                
                # Get task notes (existing functionality)
                cursor = conn.execute("""
                    SELECT 'task' as type, id, title, notes, created_date
                    FROM tasks 
                    WHERE notes IS NOT NULL AND notes != ''
                """)
                for row in cursor.fetchall():
                    self.notes_data.append({
                        "id": f"task_{row[1]}",
                        "type": "Task",
                        "title": f"Task: {row[2]}",
                        "content": row[3],
                        "date": row[4] or datetime.now().isoformat(),
                        "source_id": row[1],
                        "is_pinned": False
                    })
            
            # Sort by pinned status first, then by date (newest first)
            self.notes_data.sort(key=lambda x: (not x.get("is_pinned", False), x["date"]), reverse=True)
            
            self.display_notes()
            logger.info(f"Loaded {len(self.notes_data)} notes")
            
        except Exception as e:
            logger.error(f"Error loading notes: {e}")
            messagebox.showerror("Error", f"Failed to load notes: {str(e)}")
    
    def display_notes(self):
        """Display notes in the list"""
        # Clear existing notes
        for widget in self.notes_list_frame.winfo_children():
            widget.destroy()
        
        if not self.notes_data:
            no_notes_label = ctk.CTkLabel(
                self.notes_list_frame,
                text="No notes found\n\nAdd a note to get started!",
                font=ctk.CTkFont(size=14),
                justify="center"
            )
            no_notes_label.pack(expand=True, pady=50)
            return
        
        for note in self.notes_data:
            note_widget = self.create_note_widget(note)
            note_widget.pack(fill="x", pady=2)
    
    def create_note_widget(self, note):
        """Create widget for a note"""
        note_frame = ctk.CTkFrame(self.notes_list_frame, **themes.get_frame_styles()["default"])
        
        content_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Note header
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=note["title"][:40] + ("..." if len(note["title"]) > 40 else ""),
            font=ctk.CTkFont(weight="bold")
        )
        title_label.pack(side="left")
        
        type_label = ctk.CTkLabel(
            header_frame,
            text=f"[{note['type']}]",
            font=ctk.CTkFont(size=10),
            text_color=themes.get_color("text_secondary")
        )
        type_label.pack(side="right")
        
        # Note preview
        preview_text = note["content"][:100] + ("..." if len(note["content"]) > 100 else "")
        preview_label = ctk.CTkLabel(
            content_frame,
            text=preview_text,
            font=ctk.CTkFont(size=11),
            justify="left",
            wraplength=300
        )
        preview_label.pack(anchor="w", pady=(5, 0))
        
        # Date
        try:
            date_obj = datetime.fromisoformat(note["date"].replace('Z', '+00:00'))
            date_str = date_obj.strftime("%Y-%m-%d %H:%M")
        except:
            date_str = note["date"][:16]
        
        date_label = ctk.CTkLabel(
            content_frame,
            text=date_str,
            font=ctk.CTkFont(size=9),
            text_color=themes.get_color("text_secondary")
        )
        date_label.pack(anchor="w", pady=(2, 0))
        
        # Bind click event
        def on_note_click(event, note_data=note):
            self.select_note(note_data)
        
        note_frame.bind("<Button-1>", on_note_click)
        content_frame.bind("<Button-1>", on_note_click)
        
        return note_frame
    
    def select_note(self, note):
        """Select a note for editing"""
        self.selected_note = note
        self.show_note_editor()
        logger.info(f"Selected note: {note['title']}")
    
    def load_note_into_editor(self):
        """Load selected note into editor"""
        if not self.selected_note:
            return
        
        note = self.selected_note
        self.note_title_var.set(note["title"])
        self.note_content.delete("1.0", "end")
        self.note_content.insert("1.0", note["content"])
    
    def save_note(self):
        """Save current note"""
        title = self.note_title_var.get().strip()
        content = self.note_content.get("1.0", "end").strip()
        
        if not title or not content:
            messagebox.showerror("Error", "Both title and content are required")
            return
        
        try:
            now = datetime.now().isoformat()
            
            with self.db_manager.get_connection() as conn:
                if self.selected_note:
                    # Update existing note
                    conn.execute("""
                        UPDATE notes 
                        SET title = ?, content = ?, modified_date = ?
                        WHERE id = ?
                    """, (title, content, now, self.selected_note['id']))
                    
                    messagebox.showinfo("Success", "Note updated successfully!")
                    logger.info(f"Note updated: {title} (ID: {self.selected_note['id']})")
                else:
                    # Create new note
                    cursor = conn.execute("""
                        INSERT INTO notes (title, content, category, created_date, modified_date)
                        VALUES (?, ?, ?, ?, ?)
                    """, (title, content, "general", now, now))
                    
                    note_id = cursor.lastrowid
                    messagebox.showinfo("Success", "Note saved successfully!")
                    logger.info(f"New note created: {title} (ID: {note_id})")
            
            # Refresh the notes list
            self.load_notes()
            
        except Exception as e:
            logger.error(f"Error saving note: {e}")
            messagebox.showerror("Error", f"Failed to save note: {str(e)}")
    
    def add_new_note(self):
        """Add a new note"""
        self.selected_note = None
        self.note_title_var.set("")
        self.note_content.delete("1.0", "end")
        logger.info("New note started")
    
    def clear_note_editor(self):
        """Clear the note editor"""
        self.note_title_var.set("")
        self.note_content.delete("1.0", "end")
        self.selected_note = None
    
    def delete_note(self):
        """Delete selected note"""
        if not self.selected_note:
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Delete note '{self.selected_note['title']}'?"):
            try:
                with self.db_manager.get_connection() as conn:
                    conn.execute("DELETE FROM notes WHERE id = ?", 
                               (self.selected_note['id'],))
                
                messagebox.showinfo("Success", "Note deleted successfully!")
                logger.info(f"Note deleted: {self.selected_note['title']} (ID: {self.selected_note['id']})")
                
                # Clear editor and refresh list
                self.clear_note_editor()
                self.load_notes()
                
            except Exception as e:
                logger.error(f"Error deleting note: {e}")
                messagebox.showerror("Error", f"Failed to delete note: {str(e)}")
    
    def load_photos(self):
        """Load photos from database"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT p.id, p.file_path, p.caption, p.photo_date, p.growth_stage,
                           g.name as garden_name, pl.plant_name
                    FROM photos p
                    LEFT JOIN gardens g ON p.garden_id = g.id
                    LEFT JOIN plants pl ON p.plant_id = pl.id
                    ORDER BY p.photo_date DESC
                """)
                
                self.photos_data = []
                for row in cursor.fetchall():
                    self.photos_data.append({
                        "id": row[0],
                        "file_path": row[1],
                        "caption": row[2] or "No caption",
                        "photo_date": row[3],
                        "growth_stage": row[4] or "General",
                        "garden_name": row[5] or "Unknown Garden",
                        "plant_name": row[6] or "No specific plant"
                    })
            
            self.display_photos()
            logger.info(f"Loaded {len(self.photos_data)} photos")
            
        except Exception as e:
            logger.error(f"Error loading photos: {e}")
            self.photos_data = []
    
    def display_photos(self):
        """Display photos in grid"""
        # Clear existing photos
        for widget in self.photos_grid_frame.winfo_children():
            widget.destroy()
        
        if not self.photos_data:
            no_photos_label = ctk.CTkLabel(
                self.photos_grid_frame,
                text="📷 No photos yet\n\nAdd some photos to document your garden progress!",
                font=ctk.CTkFont(size=14),
                justify="center"
            )
            no_photos_label.pack(expand=True, pady=50)
            return
        
        # Create photo grid
        for i, photo in enumerate(self.photos_data):
            photo_widget = self.create_photo_widget(photo)
            photo_widget.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
    
    def create_photo_widget(self, photo):
        """Create widget for a photo"""
        photo_frame = ctk.CTkFrame(self.photos_grid_frame, **themes.get_frame_styles()["default"])
        
        # Photo placeholder (since we don't have actual images to display)
        placeholder_frame = ctk.CTkFrame(photo_frame, width=200, height=150, 
                                       **themes.get_frame_styles()["card"])
        placeholder_frame.pack(padx=10, pady=10)
        placeholder_frame.pack_propagate(False)
        
        # Photo icon
        photo_icon = ctk.CTkLabel(
            placeholder_frame,
            text="📷",
            font=ctk.CTkFont(size=40)
        )
        photo_icon.pack(expand=True)
        
        # Photo info
        info_frame = ctk.CTkFrame(photo_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        caption_label = ctk.CTkLabel(
            info_frame,
            text=photo["caption"][:30] + ("..." if len(photo["caption"]) > 30 else ""),
            font=ctk.CTkFont(weight="bold", size=12)
        )
        caption_label.pack(anchor="w")
        
        details_text = f"{photo['garden_name']} • {photo['growth_stage']}"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=ctk.CTkFont(size=10),
            text_color=themes.get_color("text_secondary")
        )
        details_label.pack(anchor="w")
        
        try:
            date_obj = datetime.fromisoformat(photo["photo_date"])
            date_str = date_obj.strftime("%Y-%m-%d")
        except:
            date_str = photo["photo_date"][:10]
        
        date_label = ctk.CTkLabel(
            info_frame,
            text=date_str,
            font=ctk.CTkFont(size=9),
            text_color=themes.get_color("text_secondary")
        )
        date_label.pack(anchor="w")
        
        return photo_frame
    
    def add_photos(self):
        """Add new photos"""
        messagebox.showinfo("Coming Soon", 
                           "Photo upload and management will be fully implemented in Phase 3.\n" +
                           "This will include:\n" +
                           "• Photo upload and organization\n" +
                           "• Thumbnail generation\n" +
                           "• Growth stage tracking\n" +
                           "• Photo galleries by garden/plant")
        
        logger.info("Photo upload requested")
