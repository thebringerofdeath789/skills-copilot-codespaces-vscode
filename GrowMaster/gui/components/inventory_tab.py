"""Inventory Tab - Resource and supply management"""

import customtkinter as ctk
import logging
from tkinter import messagebox, ttk
from datetime import datetime, date
import json

from config.themes import themes
from core.database.database_manager import DatabaseManager
from gui.dialogs.inventory_transaction_dialog import InventoryTransactionDialog

logger = logging.getLogger(__name__)

class InventoryTab:
    """Comprehensive inventory management interface"""
    
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        self.db_manager = DatabaseManager()
        self.inventory_data = []
        self.selected_item = None
        
        # Configure parent frame
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.main_container = ctk.CTkFrame(parent)
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        self.create_interface()
        self.load_inventory()
    
    def create_interface(self):
        """Create the inventory interface"""
        
        # Header
        header_frame = ctk.CTkFrame(self.main_container, **themes.get_frame_styles()["card"])
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📦 Inventory Management",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=15, pady=10)
        
        # Action buttons in header
        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=15, pady=10)
        
        new_item_btn = ctk.CTkButton(
            button_frame,
            text="➕ New Item",
            command=self.show_add_item_form,
            **themes.get_button_styles()["primary"]
        )
        new_item_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            command=self.load_inventory,
            **themes.get_button_styles()["secondary"]
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Left panel: Inventory list and filters
        self.create_left_panel()
        
        # Right panel: Item details and forms
        self.create_right_panel()
    
    def create_left_panel(self):
        """Create left panel with inventory list"""
        left_panel = ctk.CTkFrame(self.main_container, **themes.get_frame_styles()["card"])
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(5, 2), pady=5)
        left_panel.grid_columnconfigure(0, weight=1)
        left_panel.grid_rowconfigure(2, weight=1)
        
        # Filters
        filter_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        filter_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        filter_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(filter_frame, text="Category:").grid(row=0, column=0, sticky="w")
        
        self.category_filter = ctk.StringVar(value="all")
        category_dropdown = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.category_filter,
            values=["all", "nutrients", "tools", "containers", "lighting", "growing_medium", "seeds", "other"],
            command=self.filter_inventory
        )
        category_dropdown.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        # Search
        search_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        search_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(search_frame, text="Search:").grid(row=0, column=0, sticky="w")
        
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        search_entry.bind("<KeyRelease>", lambda e: self.filter_inventory())
        
        # Inventory list
        list_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        self.inventory_listbox = ctk.CTkScrollableFrame(list_frame)
        self.inventory_listbox.grid(row=0, column=0, sticky="nsew")
    
    def create_right_panel(self):
        """Create right panel with item details"""
        self.right_panel = ctk.CTkFrame(self.main_container, **themes.get_frame_styles()["card"])
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(2, 5), pady=5)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        # Initially show item details view
        self.show_item_details()
    
    def show_item_details(self):
        """Show item details view"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        details_frame = ctk.CTkScrollableFrame(self.right_panel, label_text="Item Details")
        details_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        if self.selected_item:
            self.display_item_details(details_frame)
        else:
            # Show placeholder
            placeholder = ctk.CTkLabel(
                details_frame,
                text="📦 Select an item to view details\n\nItem information, stock levels,\nand transaction history will appear here.",
                font=ctk.CTkFont(size=14),
                justify="center"
            )
            placeholder.pack(expand=True, pady=50)
    
    def display_item_details(self, parent):
        """Display selected item details"""
        item = self.selected_item
        
        # Item header
        header_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        header_frame.pack(fill="x", padx=5, pady=5)
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=f"📦 {item['item_name']}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        name_label.pack(anchor="w", padx=15, pady=10)
        
        # Stock status
        stock_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        stock_frame.pack(fill="x", padx=5, pady=5)
        
        current_qty = float(item['current_quantity'])
        min_threshold = float(item['minimum_threshold'] or 0)
        
        # Stock level indicator
        if current_qty <= 0:
            status_color = themes.get_color("error")
            status_text = "🔴 OUT OF STOCK"
        elif current_qty <= min_threshold:
            status_color = themes.get_color("warning")
            status_text = "🟡 LOW STOCK"
        else:
            status_color = themes.get_color("success")
            status_text = "🟢 IN STOCK"
        
        status_label = ctk.CTkLabel(
            stock_frame,
            text=status_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=status_color
        )
        status_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Quantity info
        qty_text = f"Current: {current_qty} {item['unit_of_measure']}"
        if min_threshold > 0:
            qty_text += f" (Min: {min_threshold})"
        
        qty_label = ctk.CTkLabel(stock_frame, text=qty_text, font=ctk.CTkFont(size=12))
        qty_label.pack(anchor="w", padx=15, pady=(0, 15))
        
        # Item details
        details_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        details_frame.pack(fill="x", padx=5, pady=5)
        
        details_list = [
            ("Category", item['category'].title()),
            ("Brand", item['brand'] or "N/A"),
            ("Type", item['item_type'] or "N/A"),
            ("Cost per Unit", f"${float(item['cost_per_unit'] or 0):.2f}"),
            ("Supplier", item['supplier'] or "N/A"),
            ("Storage Location", item['storage_location'] or "N/A"),
            ("Expiration Date", item['expiration_date'] or "N/A")
        ]
        
        for label, value in details_list:
            detail_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            detail_frame.pack(fill="x", padx=15, pady=2)
            
            label_widget = ctk.CTkLabel(detail_frame, text=f"{label}:", width=120)
            label_widget.pack(side="left")
            
            value_widget = ctk.CTkLabel(detail_frame, text=str(value))
            value_widget.pack(side="left", padx=(10, 0))
        
        # Notes
        if item['notes']:
            notes_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
            notes_frame.pack(fill="x", padx=5, pady=5)
            
            notes_label = ctk.CTkLabel(notes_frame, text="Notes:", font=ctk.CTkFont(weight="bold"))
            notes_label.pack(anchor="w", padx=15, pady=(15, 5))
            
            notes_text = ctk.CTkTextbox(notes_frame, height=60)
            notes_text.pack(fill="x", padx=15, pady=(0, 15))
            notes_text.insert("1.0", item['notes'])
            notes_text.configure(state="disabled")
        
        # Action buttons
        action_frame = ctk.CTkFrame(parent, **themes.get_frame_styles()["default"])
        action_frame.pack(fill="x", padx=5, pady=5)
        
        button_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        button_container.pack(pady=15)
        
        edit_btn = ctk.CTkButton(
            button_container,
            text="✏️ Edit",
            command=self.show_edit_item_form,
            **themes.get_button_styles()["primary"]
        )
        edit_btn.pack(side="left", padx=5)
        
        transaction_btn = ctk.CTkButton(
            button_container,
            text="📊 Transactions",
            command=self.show_transaction_form,
            **themes.get_button_styles()["secondary"]
        )
        transaction_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            button_container,
            text="🗑️ Delete",
            command=self.delete_item,
            **themes.get_button_styles()["danger"]
        )
        delete_btn.pack(side="left", padx=5)
    
    def show_add_item_form(self):
        """Show form to add new inventory item"""
        self.selected_item = None
        self.show_item_form("Add New Item")
    
    def show_edit_item_form(self):
        """Show form to edit selected item"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return
        self.show_item_form("Edit Item")
    
    def show_item_form(self, title):
        """Show item form for add/edit"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        form_frame = ctk.CTkScrollableFrame(self.right_panel, label_text=title)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Form fields
        self.form_vars = {}
        
        fields = [
            ("item_name", "Item Name*", "entry"),
            ("category", "Category*", "dropdown", ["nutrients", "tools", "containers", "lighting", "growing_medium", "seeds", "other"]),
            ("brand", "Brand", "entry"),
            ("item_type", "Type", "entry"),
            ("current_quantity", "Current Quantity*", "entry"),
            ("unit_of_measure", "Unit of Measure*", "entry"),
            ("minimum_threshold", "Minimum Threshold", "entry"),
            ("cost_per_unit", "Cost per Unit ($)", "entry"),
            ("supplier", "Supplier", "entry"),
            ("storage_location", "Storage Location", "entry"),
            ("expiration_date", "Expiration Date (YYYY-MM-DD)", "entry"),
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
        if self.selected_item:
            self.load_form_data()
        
        # Submit buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        submit_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Item",
            command=self.save_item,
            **themes.get_button_styles()["primary"]
        )
        submit_btn.pack(side="left", padx=5)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Cancel",
            command=self.show_item_details,
            **themes.get_button_styles()["secondary"]
        )
        cancel_btn.pack(side="left", padx=5)
    
    def load_form_data(self):
        """Load selected item data into form"""
        if not self.selected_item:
            return
        
        item = self.selected_item
        
        # Load data into form variables
        for field_name, var in self.form_vars.items():
            if field_name == "notes":
                # TextBox widget
                var.delete("1.0", "end")
                var.insert("1.0", item.get(field_name, ""))
            else:
                # StringVar
                var.set(str(item.get(field_name, "")))
    
    def save_item(self):
        """Save inventory item to database"""
        try:
            # Get form data
            item_data = {}
            for field_name, var in self.form_vars.items():
                if field_name == "notes":
                    # TextBox widget
                    item_data[field_name] = var.get("1.0", "end").strip()
                else:
                    # StringVar
                    item_data[field_name] = var.get().strip()
            
            # Validate required fields
            required_fields = ["item_name", "category", "current_quantity", "unit_of_measure"]
            for field in required_fields:
                if not item_data.get(field):
                    messagebox.showerror("Error", f"{field.replace('_', ' ').title()} is required")
                    return
            
            # Validate numeric fields
            try:
                float(item_data["current_quantity"])
                if item_data["minimum_threshold"]:
                    float(item_data["minimum_threshold"])
                if item_data["cost_per_unit"]:
                    float(item_data["cost_per_unit"])
            except ValueError:
                messagebox.showerror("Error", "Quantity, threshold, and cost must be valid numbers")
                return
            
            # Validate date
            if item_data["expiration_date"]:
                try:
                    datetime.strptime(item_data["expiration_date"], "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Expiration date must be in YYYY-MM-DD format")
                    return
            
            # Save to database
            now = datetime.now().isoformat()
            
            with self.db_manager.get_connection() as conn:
                if self.selected_item:
                    # Update existing item
                    conn.execute("""
                        UPDATE inventory_items
                        SET item_name = ?, category = ?, brand = ?, item_type = ?,
                            current_quantity = ?, unit_of_measure = ?, minimum_threshold = ?,
                            cost_per_unit = ?, supplier = ?, storage_location = ?,
                            expiration_date = ?, notes = ?, last_updated = ?
                        WHERE id = ?
                    """, (
                        item_data["item_name"], item_data["category"], item_data["brand"],
                        item_data["item_type"], float(item_data["current_quantity"]),
                        item_data["unit_of_measure"], 
                        float(item_data["minimum_threshold"]) if item_data["minimum_threshold"] else 0,
                        float(item_data["cost_per_unit"]) if item_data["cost_per_unit"] else 0,
                        item_data["supplier"], item_data["storage_location"],
                        item_data["expiration_date"] if item_data["expiration_date"] else None,
                        item_data["notes"], now, self.selected_item["id"]
                    ))
                    messagebox.showinfo("Success", "Item updated successfully!")
                else:
                    # Insert new item
                    conn.execute("""
                        INSERT INTO inventory_items
                        (item_name, category, brand, item_type, current_quantity,
                         unit_of_measure, minimum_threshold, cost_per_unit, supplier,
                         storage_location, expiration_date, notes, created_date, last_updated)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        item_data["item_name"], item_data["category"], item_data["brand"],
                        item_data["item_type"], float(item_data["current_quantity"]),
                        item_data["unit_of_measure"],
                        float(item_data["minimum_threshold"]) if item_data["minimum_threshold"] else 0,
                        float(item_data["cost_per_unit"]) if item_data["cost_per_unit"] else 0,
                        item_data["supplier"], item_data["storage_location"],
                        item_data["expiration_date"] if item_data["expiration_date"] else None,
                        item_data["notes"], now, now
                    ))
                    messagebox.showinfo("Success", "Item added successfully!")
            
            self.load_inventory()
            self.show_item_details()
            
        except Exception as e:
            logger.error(f"Error saving inventory item: {e}")
            messagebox.showerror("Error", f"Failed to save item: {str(e)}")
    
    def load_inventory(self):
        """Load inventory from database"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM inventory_items
                    ORDER BY item_name
                """)
                
                items = cursor.fetchall()
                self.inventory_data = []
                
                for item in items:
                    self.inventory_data.append({
                        "id": item[0],
                        "item_name": item[1],
                        "category": item[2],
                        "brand": item[3],
                        "item_type": item[4],
                        "current_quantity": item[5],
                        "unit_of_measure": item[6],
                        "minimum_threshold": item[7],
                        "cost_per_unit": item[8],
                        "supplier": item[9],
                        "storage_location": item[10],
                        "expiration_date": item[11],
                        "notes": item[12],
                        "created_date": item[13],
                        "last_updated": item[14]
                    })
            
            self.display_inventory()
            logger.info(f"Loaded {len(self.inventory_data)} inventory items")
            
        except Exception as e:
            logger.error(f"Error loading inventory: {e}")
            messagebox.showerror("Error", f"Failed to load inventory: {str(e)}")
    
    def display_inventory(self):
        """Display inventory in the list"""
        # Clear existing items
        for widget in self.inventory_listbox.winfo_children():
            widget.destroy()
        
        filtered_data = self.get_filtered_inventory()
        
        if not filtered_data:
            no_items_label = ctk.CTkLabel(
                self.inventory_listbox,
                text="No items found",
                font=ctk.CTkFont(size=14)
            )
            no_items_label.pack(pady=20)
            return
        
        for item in filtered_data:
            item_widget = self.create_inventory_item_widget(item)
            item_widget.pack(fill="x", pady=2)
    
    def get_filtered_inventory(self):
        """Get filtered inventory based on search and category"""
        filtered = self.inventory_data
        
        # Filter by category
        if self.category_filter.get() != "all":
            filtered = [item for item in filtered if item["category"] == self.category_filter.get()]
        
        # Filter by search term
        search_term = self.search_var.get().lower()
        if search_term:
            filtered = [item for item in filtered if 
                       search_term in item["item_name"].lower() or
                       search_term in (item["brand"] or "").lower() or
                       search_term in (item["supplier"] or "").lower()]
        
        return filtered
    
    def create_inventory_item_widget(self, item):
        """Create widget for inventory item"""
        # Determine stock status color
        current_qty = float(item['current_quantity'])
        min_threshold = float(item['minimum_threshold'] or 0)
        
        if current_qty <= 0:
            status_color = "#5a2d2d"  # Red
        elif current_qty <= min_threshold:
            status_color = "#5a4a2d"  # Orange
        else:
            status_color = "#2d4a4a"  # Default
        
        item_frame = ctk.CTkFrame(self.inventory_listbox, fg_color=status_color)
        
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Item name and category
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=item["item_name"],
            font=ctk.CTkFont(weight="bold")
        )
        name_label.pack(side="left")
        
        category_label = ctk.CTkLabel(
            header_frame,
            text=f"[{item['category'].title()}]",
            font=ctk.CTkFont(size=10)
        )
        category_label.pack(side="right")
        
        # Quantity info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(fill="x", pady=(2, 0))
        
        qty_text = f"Stock: {current_qty} {item['unit_of_measure']}"
        qty_label = ctk.CTkLabel(info_frame, text=qty_text, font=ctk.CTkFont(size=10))
        qty_label.pack(side="left")
        
        if item['brand']:
            brand_label = ctk.CTkLabel(
                info_frame,
                text=item['brand'],
                font=ctk.CTkFont(size=10)
            )
            brand_label.pack(side="right")
        
        # Bind click event
        def on_item_click(event, item_data=item):
            self.select_item(item_data)
        
        item_frame.bind("<Button-1>", on_item_click)
        content_frame.bind("<Button-1>", on_item_click)
        
        return item_frame
    
    def select_item(self, item):
        """Select an inventory item"""
        self.selected_item = item
        self.show_item_details()
        logger.info(f"Selected inventory item: {item['item_name']}")
    
    def filter_inventory(self, *args):
        """Filter inventory based on current filters"""
        self.display_inventory()
    
    def delete_item(self):
        """Delete selected inventory item"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{self.selected_item['item_name']}'?"):
            try:
                with self.db_manager.get_connection() as conn:
                    conn.execute("DELETE FROM inventory_items WHERE id = ?", 
                               (self.selected_item["id"],))
                
                messagebox.showinfo("Success", "Item deleted successfully!")
                self.selected_item = None
                self.load_inventory()
                self.show_item_details()
                
            except Exception as e:
                logger.error(f"Error deleting inventory item: {e}")
                messagebox.showerror("Error", f"Failed to delete item: {str(e)}")
    
    def show_transaction_form(self):
        """Show transaction form for selected item"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item first")
            return
        
        try:
            # Refresh callback to update inventory display
            refresh_callback = lambda: self.load_inventory()
            
            dialog = InventoryTransactionDialog(
                self.parent, 
                self.settings, 
                self.selected_item,
                callback=refresh_callback
            )
            result = dialog.show()
            
            if result:
                logger.info(f"Transaction completed for {self.selected_item['item_name']}: {result['transaction_type']} {result['quantity']}")
                
                # Update the selected item's quantity display
                self.selected_item['current_quantity'] = result['new_quantity']
                self.show_item_details()
                
        except Exception as e:
            logger.error(f"Error in transaction dialog: {e}")
            messagebox.showerror("Error", f"Failed to open transaction dialog: {str(e)}")
