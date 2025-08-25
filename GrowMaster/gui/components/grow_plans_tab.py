"""
Grow Plans Tab - Garden management interface
Template system for rapid grow plan creation and replication
"""

import customtkinter as ctk
import logging
from tkinter import messagebox
from datetime import datetime
import json

from config.themes import themes
from core.database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class GrowPlansTab:
    """Garden and grow plan management interface"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        self.db_manager = DatabaseManager()
        self.gardens_data = []
        self.selected_garden = None
        
        # Configure parent frame
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.main_container = ctk.CTkFrame(parent)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        self.create_interface()
        self.load_gardens()
    
    def create_interface(self):
        """Create garden management interface"""
        
        # Header
        header_frame = ctk.CTkFrame(self.main_container, **themes.get_frame_styles()["card"])
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🌱 Garden & Grow Plan Management",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        # Action buttons in header
        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=15, pady=10)
        
        new_garden_btn = ctk.CTkButton(
            button_frame,
            text="➕ New Garden",
            command=self.show_add_garden_form,
            **themes.get_button_styles()["primary"]
        )
        new_garden_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            command=self.load_gardens,
            **themes.get_button_styles()["secondary"]
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Left panel: Garden list
        self.create_left_panel()
        
        # Right panel: Garden details and forms
        self.create_right_panel()
    
    def create_left_panel(self):
        """Create left panel with garden list"""
        left_panel = ctk.CTkFrame(self.main_container, **themes.get_frame_styles()["card"])
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(5, 2), pady=5)
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)
        
        # Garden list header
        list_header = ctk.CTkFrame(left_panel, fg_color="transparent")
        list_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        gardens_title = ctk.CTkLabel(list_header, text="🏡 My Gardens", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        gardens_title.pack(anchor="w")
        
        # Gardens list
        self.gardens_list_frame = ctk.CTkScrollableFrame(left_panel)
        self.gardens_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    def create_right_panel(self):
        """Create right panel with garden details"""
        self.right_panel = ctk.CTkFrame(self.main_container, **themes.get_frame_styles()["card"])
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(2, 5), pady=5)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        # Initially show garden details view
        self.show_garden_details()
    
    def show_garden_details(self):
        """Show garden details view"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        details_frame = ctk.CTkScrollableFrame(self.right_panel, label_text="Garden Details")
        details_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        if self.selected_garden:
            self.display_garden_details(details_frame)
        else:
            # Show placeholder
            placeholder = ctk.CTkLabel(
                details_frame,
                text="🌱 Select a garden to view details\n\nGarden information, settings,\nand management options will appear here.",
                font=ctk.CTkFont(size=14),
                justify="center"
            )
            placeholder.pack(expand=True, pady=50)
    
    def display_garden_details(self, parent):
        """Display selected garden details"""
        garden = self.selected_garden
        
        # Garden header
        header_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        header_frame.pack(fill="x", padx=5, pady=5)
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=f"🌱 {garden['name']}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        name_label.pack(anchor="w", padx=15, pady=10)
        
        # Status indicator
        status_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        status_frame.pack(fill="x", padx=5, pady=5)
        
        status_colors = {
            "active": themes.get_color("success"),
            "dormant": themes.get_color("warning"),
            "completed": themes.get_color("info"),
            "planning": themes.get_color("text_secondary")
        }
        
        status_color = status_colors.get(garden.get('status', 'active'), themes.get_color("info"))
        
        status_label = ctk.CTkLabel(
            status_frame,
            text=f"Status: {garden.get('status', 'Active').title()}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=status_color
        )
        status_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Garden details
        details_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        details_frame.pack(fill="x", padx=5, pady=5)
        
        details_list = [
            ("Type", garden.get('garden_type', 'N/A').title()),
            ("Growing Method", garden.get('growing_method', 'N/A').title()),
            ("Location", garden.get('location', 'N/A')),
            ("Dimensions", f"{garden.get('dimensions_length', 0)} × {garden.get('dimensions_width', 0)} × {garden.get('dimensions_height', 0)}"),
            ("Created", garden.get('created_date', 'N/A')[:10] if garden.get('created_date') else 'N/A')
        ]
        
        for label, value in details_list:
            detail_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            detail_frame.pack(fill="x", padx=15, pady=2)
            
            label_widget = ctk.CTkLabel(detail_frame, text=f"{label}:", width=120)
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(detail_frame, text=str(value))
            value_widget.pack(side="left", padx=(10, 0))
        
        # Environmental settings
        if garden.get('environmental_settings'):
            env_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
            env_frame.pack(fill="x", padx=5, pady=5)
            
            env_label = ctk.CTkLabel(env_frame, text="Environmental Settings:", font=ctk.CTkFont(weight="bold"))
            env_label.pack(anchor="w", padx=15, pady=(15, 5))
            
            try:
                env_settings = json.loads(garden['environmental_settings']) if isinstance(garden['environmental_settings'], str) else garden['environmental_settings']
                if env_settings:
                    for key, value in env_settings.items():
                        env_detail = ctk.CTkLabel(env_frame, text=f"• {key}: {value}")
                        env_detail.pack(anchor="w", padx=25, pady=1)
                else:
                    env_detail = ctk.CTkLabel(env_frame, text="No environmental settings configured")
                    env_detail.pack(anchor="w", padx=25, pady=(0, 15))
            except:
                env_detail = ctk.CTkLabel(env_frame, text="Environmental settings format error")
                env_detail.pack(anchor="w", padx=25, pady=(0, 15))
        
        # Notes
        if garden.get('notes'):
            notes_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
            notes_frame.pack(fill="x", padx=5, pady=5)
            
            notes_label = ctk.CTkLabel(notes_frame, text="Notes:", font=ctk.CTkFont(weight="bold"))
            notes_label.pack(anchor="w", padx=15, pady=(15, 5))
            
            notes_text = ctk.CTkTextbox(notes_frame, height=80)
            notes_text.pack(fill="x", padx=15, pady=(0, 15))
            notes_text.insert("1.0", garden['notes'])
            notes_text.configure(state="disabled")
        
        # Get garden statistics
        with self.db_manager.get_connection() as conn:
            # Count plants in this garden
            cursor = conn.execute("SELECT COUNT(*) FROM plants WHERE garden_id = ?", (garden['id'],))
            plant_count = cursor.fetchone()[0]
            
            # Count tasks for this garden
            cursor = conn.execute("SELECT COUNT(*) FROM tasks WHERE garden_id = ?", (garden['id'],))
            task_count = cursor.fetchone()[0]
        
        # Statistics
        stats_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        stats_frame.pack(fill="x", padx=5, pady=5)
        
        stats_label = ctk.CTkLabel(stats_frame, text="Statistics:", font=ctk.CTkFont(weight="bold"))
        stats_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        stats_info = f"Plants: {plant_count} • Tasks: {task_count}"
        stats_detail = ctk.CTkLabel(stats_frame, text=stats_info)
        stats_detail.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Action buttons
        action_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        action_frame.pack(fill="x", padx=5, pady=5)
        
        button_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        button_container.pack(pady=15)
        
        edit_btn = ctk.CTkButton(
            button_container,
            text="✏️ Edit",
            command=self.show_edit_garden_form,
            **themes.get_button_styles()["primary"]
        )
        edit_btn.pack(side="left", padx=5)
        
        clone_btn = ctk.CTkButton(
            button_container,
            text="🔄 Clone",
            command=self.clone_garden,
            **themes.get_button_styles()["secondary"]
        )
        clone_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            button_container,
            text="🗑️ Delete",
            command=self.delete_garden,
            **themes.get_button_styles()["danger"]
        )
        delete_btn.pack(side="left", padx=5)
    
    def load_gardens(self):
        """Load gardens from database"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM gardens ORDER BY created_date DESC
                """)
                
                gardens = cursor.fetchall()
                self.gardens_data = []
                
                for garden in gardens:
                    self.gardens_data.append({
                        "id": garden[0],
                        "name": garden[1],
                        "garden_type": garden[2],
                        "growing_method": garden[3],
                        "location": garden[4],
                        "dimensions_length": garden[5],
                        "dimensions_width": garden[6], 
                        "dimensions_height": garden[7],
                        "environmental_settings": garden[8],
                        "created_date": garden[9],
                        "status": garden[10],
                        "notes": garden[11],
                        "color_code": garden[12]
                    })
            
            self.display_gardens()
            logger.info(f"Loaded {len(self.gardens_data)} gardens")
            
        except Exception as e:
            logger.error(f"Error loading gardens: {e}")
            messagebox.showerror("Error", f"Failed to load gardens: {str(e)}")
    
    def display_gardens(self):
        """Display gardens in the list"""
        # Clear existing gardens
        for widget in self.gardens_list_frame.winfo_children():
            widget.destroy()
        
        if not self.gardens_data:
            no_gardens_label = ctk.CTkLabel(
                self.gardens_list_frame,
                text="No gardens found\n\nCreate your first garden to get started!",
                font=ctk.CTkFont(size=14),
                justify="center"
            )
            no_gardens_label.pack(expand=True, pady=50)
            return
        
        for garden in self.gardens_data:
            garden_widget = self.create_garden_widget(garden)
            garden_widget.pack(fill="x", pady=2)
    
    def create_garden_widget(self, garden):
        """Create widget for a garden"""
        garden_frame = ctk.CTkFrame(self.gardens_list_frame, **themes.get_frame_styles()["default"])
        
        content_frame = ctk.CTkFrame(garden_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=8)
        
        # Garden header
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=garden["name"],
            font=ctk.CTkFont(weight="bold")
        )
        name_label.pack(side="left")
        
        # Status indicator
        status_colors = {
            "active": "🟢",
            "dormant": "🟡", 
            "completed": "🔵",
            "planning": "⚪"
        }
        
        status_icon = status_colors.get(garden.get('status', 'active'), "🟢")
        status_label = ctk.CTkLabel(header_frame, text=status_icon)
        status_label.pack(side="right")
        
        # Garden details
        details_text = f"{garden['garden_type'].title()} • {garden['growing_method'].title()}"
        if garden['location']:
            details_text += f" • {garden['location']}"
        
        details_label = ctk.CTkLabel(
            content_frame,
            text=details_text,
            font=ctk.CTkFont(size=11),
            text_color=themes.get_color("text_secondary")
        )
        details_label.pack(anchor="w", pady=(5, 0))
        
        # Date
        try:
            date_obj = datetime.fromisoformat(garden["created_date"].replace('Z', '+00:00'))
            date_str = date_obj.strftime("%Y-%m-%d")
        except:
            date_str = garden["created_date"][:10] if garden["created_date"] else "N/A"
        
        date_label = ctk.CTkLabel(
            content_frame,
            text=f"Created: {date_str}",
            font=ctk.CTkFont(size=9),
            text_color=themes.get_color("text_secondary")
        )
        date_label.pack(anchor="w", pady=(2, 0))
        
        # Bind click event
        def on_garden_click(event, garden_data=garden):
            self.select_garden(garden_data)
        
        garden_frame.bind("<Button-1>", on_garden_click)
        content_frame.bind("<Button-1>", on_garden_click)
        
        return garden_frame
    
    def select_garden(self, garden):
        """Select a garden for editing"""
        self.selected_garden = garden
        self.show_garden_details()
        logger.info(f"Selected garden: {garden['name']}")
    
    def show_add_garden_form(self):
        """Show form to add new garden"""
        self.selected_garden = None
        self.show_garden_form("Add New Garden")
    
    def show_edit_garden_form(self):
        """Show form to edit selected garden"""
        if not self.selected_garden:
            messagebox.showwarning("Warning", "Please select a garden to edit")
            return
        self.show_garden_form("Edit Garden")
    
    def show_garden_form(self, title):
        """Show garden form for add/edit"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        form_frame = ctk.CTkScrollableFrame(self.right_panel, label_text=title)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Form fields
        self.form_vars = {}
        
        fields = [
            ("name", "Garden Name*", "entry"),
            ("garden_type", "Garden Type*", "dropdown", ["indoor", "outdoor", "greenhouse"]),
            ("growing_method", "Growing Method*", "dropdown", ["soil", "hydroponic", "aeroponic", "coco", "soilless"]),
            ("location", "Location", "entry"),
            ("dimensions_length", "Length (ft)", "entry"),
            ("dimensions_width", "Width (ft)", "entry"), 
            ("dimensions_height", "Height (ft)", "entry"),
            ("status", "Status", "dropdown", ["active", "dormant", "completed", "planning"]),
            ("notes", "Notes", "textbox")
        ]
        
        for i, field_info in enumerate(fields):
            field_name = field_info[0]
            field_label = field_info[1]
            field_type = field_info[2]
            
            field_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            field_frame.pack(fill="x", padx=5, pady=5)
            
            label = ctk.CTkLabel(field_frame, text=field_label, width=150)
            label.pack(side="left")
            
            if field_type == "entry":
                var = ctk.StringVar()
                entry = ctk.CTkEntry(field_frame, textvariable=var, width=250)
                entry.pack(side="left", padx=(10, 0))
                self.form_vars[field_name] = var
                
            elif field_type == "dropdown":
                values = field_info[3]
                var = ctk.StringVar(value=values[0])
                dropdown = ctk.CTkOptionMenu(field_frame, variable=var, values=values)
                dropdown.pack(side="left", padx=(10, 0))
                self.form_vars[field_name] = var
                
            elif field_type == "textbox":
                textbox = ctk.CTkTextbox(field_frame, width=250, height=80)
                textbox.pack(side="left", padx=(10, 0))
                self.form_vars[field_name] = textbox
        
        # Load existing data if editing
        if self.selected_garden:
            self.load_garden_form_data()
        
        # Submit buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        submit_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Garden",
            command=self.save_garden,
            **themes.get_button_styles()["primary"]
        )
        submit_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            command=self.show_garden_details,
            **themes.get_button_styles()["secondary"]
        )
        cancel_btn.pack(side="left", padx=5)
    
    def load_garden_form_data(self):
        """Load selected garden data into form"""
        if not self.selected_garden:
            return
        
        garden = self.selected_garden
        
        # Load data into form variables
        for field_name, var in self.form_vars.items():
            if field_name == "notes":
                # TextBox widget
                var.delete("1.0", "end")
                var.insert("1.0", garden.get(field_name, ""))
            else:
                # StringVar
                var.set(str(garden.get(field_name, "")))
    
    def save_garden(self):
        """Save garden to database"""
        try:
            # Get form data
            garden_data = {}
            for field_name, var in self.form_vars.items():
                if field_name == "notes":
                    # TextBox widget
                    garden_data[field_name] = var.get("1.0", "end").strip()
                else:
                    # StringVar
                    garden_data[field_name] = var.get().strip()
            
            # Validate required fields
            required_fields = ["name", "garden_type", "growing_method"]
            for field in required_fields:
                if not garden_data.get(field):
                    messagebox.showerror("Error", f"{field.replace('_', ' ').title()} is required")
                    return
            
            # Validate numeric fields
            for dim_field in ["dimensions_length", "dimensions_width", "dimensions_height"]:
                if garden_data.get(dim_field):
                    try:
                        float(garden_data[dim_field])
                    except ValueError:
                        messagebox.showerror("Error", f"{dim_field.replace('_', ' ').title()} must be a valid number")
                        return
            
            # Save to database
            now = datetime.now().isoformat()
            environmental_settings = "{}"  # Default empty JSON
            
            with self.db_manager.get_connection() as conn:
                if self.selected_garden:
                    # Update existing garden
                    conn.execute("""
                        UPDATE gardens
                        SET name = ?, garden_type = ?, growing_method = ?, location = ?,
                            dimensions_length = ?, dimensions_width = ?, dimensions_height = ?,
                            status = ?, notes = ?
                        WHERE id = ?
                    """, (
                        garden_data["name"], garden_data["garden_type"], garden_data["growing_method"],
                        garden_data["location"], 
                        float(garden_data["dimensions_length"]) if garden_data["dimensions_length"] else 0,
                        float(garden_data["dimensions_width"]) if garden_data["dimensions_width"] else 0,
                        float(garden_data["dimensions_height"]) if garden_data["dimensions_height"] else 0,
                        garden_data["status"], garden_data["notes"], self.selected_garden["id"]
                    ))
                    messagebox.showinfo("Success", "Garden updated successfully!")
                else:
                    # Insert new garden
                    conn.execute("""
                        INSERT INTO gardens
                        (name, garden_type, growing_method, location, dimensions_length,
                         dimensions_width, dimensions_height, environmental_settings,
                         created_date, status, notes, color_code)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        garden_data["name"], garden_data["garden_type"], garden_data["growing_method"],
                        garden_data["location"],
                        float(garden_data["dimensions_length"]) if garden_data["dimensions_length"] else 0,
                        float(garden_data["dimensions_width"]) if garden_data["dimensions_width"] else 0,
                        float(garden_data["dimensions_height"]) if garden_data["dimensions_height"] else 0,
                        environmental_settings, now, garden_data["status"], garden_data["notes"],
                        "#4CAF50"  # Default green color
                    ))
                    messagebox.showinfo("Success", "Garden created successfully!")
            
            self.load_gardens()
            self.show_garden_details()
            
        except Exception as e:
            logger.error(f"Error saving garden: {e}")
            messagebox.showerror("Error", f"Failed to save garden: {str(e)}")
    
    def clone_garden(self):
        """Clone selected garden"""
        if not self.selected_garden:
            messagebox.showwarning("Warning", "Please select a garden to clone")
            return
        
        if messagebox.askyesno("Confirm Clone", 
                              f"Clone garden '{self.selected_garden['name']}'?"):
            try:
                garden = self.selected_garden
                now = datetime.now().isoformat()
                
                with self.db_manager.get_connection() as conn:
                    conn.execute("""
                        INSERT INTO gardens
                        (name, garden_type, growing_method, location, dimensions_length,
                         dimensions_width, dimensions_height, environmental_settings,
                         created_date, status, notes, color_code)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f"{garden['name']} (Copy)", garden['garden_type'], garden['growing_method'],
                        garden['location'], garden['dimensions_length'], garden['dimensions_width'],
                        garden['dimensions_height'], garden['environmental_settings'], now,
                        "planning", garden['notes'], garden['color_code']
                    ))
                
                messagebox.showinfo("Success", f"Garden cloned successfully!")
                self.load_gardens()
                
            except Exception as e:
                logger.error(f"Error cloning garden: {e}")
                messagebox.showerror("Error", f"Failed to clone garden: {str(e)}")
    
    def delete_garden(self):
        """Delete selected garden"""
        if not self.selected_garden:
            messagebox.showwarning("Warning", "Please select a garden to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{self.selected_garden['name']}'?\n\nThis will also delete all associated plants and tasks."):
            try:
                with self.db_manager.get_connection() as conn:
                    conn.execute("DELETE FROM gardens WHERE id = ?", 
                               (self.selected_garden["id"],))
                
                messagebox.showinfo("Success", "Garden deleted successfully!")
                self.selected_garden = None
                self.load_gardens()
                self.show_garden_details()
                
            except Exception as e:
                logger.error(f"Error deleting garden: {e}")
                messagebox.showerror("Error", f"Failed to delete garden: {str(e)}")
