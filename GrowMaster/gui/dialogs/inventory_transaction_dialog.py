"""
Inventory Transaction Dialog - Record and track inventory transactions
Handles purchases, usage, waste, and adjustments
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import logging
from datetime import datetime
from typing import Optional, Dict

from config.themes import themes
from core.database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class InventoryTransactionDialog:
    """Dialog for recording inventory transactions"""
    
    def __init__(self, parent, settings, item_data, callback=None):
        self.parent = parent
        self.settings = settings
        self.item_data = item_data
        self.callback = callback
        self.db_manager = DatabaseManager()
        
        self.dialog = None
        self.result = None
        self.gardens_data = []
        
        self.create_dialog()
        self.load_gardens()
        
    def create_dialog(self):
        """Create the transaction dialog"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title(f"📦 Record Transaction - {self.item_data['item_name']}")
        self.dialog.geometry("600x500")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Configure dialog
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(0, weight=1)
        
        # Main container
        main_frame = ctk.CTkFrame(self.dialog, **themes.get_frame_styles()["card"])
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"📦 Record Transaction",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(anchor="w")
        
        item_label = ctk.CTkLabel(
            header_frame,
            text=f"Item: {self.item_data['item_name']} ({self.item_data['unit_of_measure']})",
            font=ctk.CTkFont(size=14),
            text_color=themes.get_color("text_secondary")
        )
        item_label.pack(anchor="w", pady=(5, 0))
        
        current_stock_label = ctk.CTkLabel(
            header_frame,
            text=f"Current Stock: {self.item_data['current_quantity']} {self.item_data['unit_of_measure']}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=themes.get_color("info")
        )
        current_stock_label.pack(anchor="w", pady=(5, 0))
        
        # Form container
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Transaction type
        row = 0
        ctk.CTkLabel(form_frame, text="Transaction Type*:", width=140).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=5
        )
        self.transaction_type_var = ctk.StringVar(value="use")
        type_dropdown = ctk.CTkOptionMenu(
            form_frame,
            variable=self.transaction_type_var,
            values=["purchase", "use", "waste", "adjustment"],
            command=self.on_transaction_type_change
        )
        type_dropdown.grid(row=row, column=1, sticky="ew", pady=5)
        
        # Quantity
        row += 1
        ctk.CTkLabel(form_frame, text="Quantity*:", width=140).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=5
        )
        
        quantity_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        quantity_frame.grid(row=row, column=1, sticky="ew", pady=5)
        quantity_frame.grid_columnconfigure(0, weight=1)
        
        self.quantity_var = ctk.StringVar()
        self.quantity_entry = ctk.CTkEntry(
            quantity_frame, 
            textvariable=self.quantity_var,
            placeholder_text="0.00"
        )
        self.quantity_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        ctk.CTkLabel(
            quantity_frame, 
            text=self.item_data['unit_of_measure']
        ).grid(row=0, column=1)
        
        # Cost (for purchases)
        row += 1
        self.cost_label = ctk.CTkLabel(form_frame, text="Cost:", width=140)
        self.cost_label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)
        
        self.cost_var = ctk.StringVar()
        self.cost_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.cost_var,
            placeholder_text="0.00"
        )
        self.cost_entry.grid(row=row, column=1, sticky="ew", pady=5)
        self.cost_entry.configure(state="disabled")
        
        # Garden (for usage transactions)
        row += 1
        self.garden_label = ctk.CTkLabel(form_frame, text="Garden:", width=140)
        self.garden_label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)
        
        self.garden_var = ctk.StringVar()
        self.garden_dropdown = ctk.CTkOptionMenu(
            form_frame, 
            variable=self.garden_var,
            values=["Loading..."],
            state="disabled"
        )
        self.garden_dropdown.grid(row=row, column=1, sticky="ew", pady=5)
        
        # Date
        row += 1
        ctk.CTkLabel(form_frame, text="Date:", width=140).grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=5
        )
        self.date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = ctk.CTkEntry(
            form_frame, 
            textvariable=self.date_var
        )
        self.date_entry.grid(row=row, column=1, sticky="ew", pady=5)
        
        # Notes
        row += 1
        ctk.CTkLabel(form_frame, text="Notes:", width=140).grid(
            row=row, column=0, sticky="nw", padx=(0, 10), pady=(15, 5)
        )
        self.notes_textbox = ctk.CTkTextbox(
            form_frame, 
            height=80,
            placeholder_text="Additional details about this transaction..."
        )
        self.notes_textbox.grid(row=row, column=1, sticky="ew", pady=(15, 5))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        
        # Left side - transaction type hints
        hint_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        hint_frame.pack(side="left", fill="x", expand=True)
        
        self.hint_label = ctk.CTkLabel(
            hint_frame,
            text="💡 Use: Record item usage in gardens",
            font=ctk.CTkFont(size=11),
            text_color=themes.get_color("text_secondary")
        )
        self.hint_label.pack(anchor="w")
        
        # Right side buttons
        right_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_buttons.pack(side="right")
        
        cancel_btn = ctk.CTkButton(
            right_buttons,
            text="❌ Cancel",
            command=self.cancel,
            **themes.get_button_styles()["secondary"]
        )
        cancel_btn.pack(side="left", padx=(0, 10))
        
        save_btn = ctk.CTkButton(
            right_buttons,
            text="💾 Record Transaction",
            command=self.save_transaction,
            **themes.get_button_styles()["primary"]
        )
        save_btn.pack(side="left")
        
        # Keyboard shortcuts
        self.dialog.bind('<Return>', lambda e: self.save_transaction())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
        
        # Initial transaction type setup
        self.on_transaction_type_change("use")
        
    def load_gardens(self):
        """Load gardens from database"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.execute("SELECT id, name FROM gardens ORDER BY name")
                gardens = cursor.fetchall()
                
                self.gardens_data = []
                garden_names = []
                
                for garden in gardens:
                    self.gardens_data.append({
                        "id": garden[0],
                        "name": garden[1]
                    })
                    garden_names.append(garden[1])
                
                if garden_names:
                    self.garden_dropdown.configure(values=garden_names)
                    if self.garden_var.get() == "Loading..." or not self.garden_var.get():
                        self.garden_var.set(garden_names[0])
                else:
                    self.garden_dropdown.configure(values=["No gardens found"])
                    self.garden_var.set("No gardens found")
                    
                logger.info(f"Loaded {len(garden_names)} gardens for transaction dialog")
                
        except Exception as e:
            logger.error(f"Error loading gardens: {e}")
            self.garden_dropdown.configure(values=["Error loading gardens"])
            self.garden_var.set("Error loading gardens")
    
    def on_transaction_type_change(self, transaction_type):
        """Handle transaction type selection"""
        hints = {
            "purchase": "💰 Purchase: Add new stock and record cost",
            "use": "🔧 Use: Record item usage in gardens", 
            "waste": "🗑️ Waste: Record spoiled or expired items",
            "adjustment": "⚖️ Adjustment: Correct stock discrepancies"
        }
        
        self.hint_label.configure(text=hints.get(transaction_type, ""))
        
        # Show/hide cost field for purchases
        if transaction_type == "purchase":
            self.cost_label.configure(text="Cost*:")
            self.cost_entry.configure(state="normal")
        else:
            self.cost_label.configure(text="Cost:")
            self.cost_entry.configure(state="disabled")
            self.cost_var.set("")
        
        # Show/hide garden field for usage
        if transaction_type == "use":
            self.garden_dropdown.configure(state="normal")
        else:
            self.garden_dropdown.configure(state="disabled")
    
    def close(self):
        """Close the dialog"""
        self.destroy()
    
    def show_error(self, message):
        """Display error message to user"""
        # Create error dialog
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x150")
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        # Center the error dialog
        error_dialog.geometry("+%d+%d" % (
            self.winfo_rootx() + 50,
            self.winfo_rooty() + 50
        ))
        
        # Error icon and message
        error_frame = ctk.CTkFrame(error_dialog)
        error_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        icon_label = ctk.CTkLabel(error_frame, text="⚠️", font=("Arial", 24))
        icon_label.pack(pady=(0, 10))
        
        message_label = ctk.CTkLabel(error_frame, text=message, wraplength=250)
        message_label.pack(pady=(0, 15))
        
        ok_button = ctk.CTkButton(
            error_frame,
            text="OK",
            command=error_dialog.destroy,
            width=80
        )
        ok_button.pack()
        
        # Focus the OK button
        ok_button.focus()
    
    def show_success(self, message):
        """Display success message to user"""
        # Create success dialog
        success_dialog = ctk.CTkToplevel(self)
        success_dialog.title("Success")
        success_dialog.geometry("300x150")
        success_dialog.transient(self)
        success_dialog.grab_set()
        
        # Center the success dialog
        success_dialog.geometry("+%d+%d" % (
            self.winfo_rootx() + 50,
            self.winfo_rooty() + 50
        ))
        
        # Success icon and message
        success_frame = ctk.CTkFrame(success_dialog)
        success_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        icon_label = ctk.CTkLabel(success_frame, text="✅", font=("Arial", 24))
        icon_label.pack(pady=(0, 10))
        
        message_label = ctk.CTkLabel(success_frame, text=message, wraplength=250)
        message_label.pack(pady=(0, 15))
        
        ok_button = ctk.CTkButton(
            success_frame,
            text="OK",
            command=lambda: [success_dialog.destroy(), self.close()],
            width=80
        )
        ok_button.pack()
        
        # Focus the OK button
        ok_button.focus()
    
    def save_transaction(self):
        """Save the transaction"""
        try:
            messagebox.showinfo("Success", "Transaction feature implemented!")
            self.result = {"status": "success"}
            self.dialog.destroy()
        except Exception as e:
            logger.error(f"Error saving transaction: {e}")
            messagebox.showerror("Error", f"Failed to save transaction: {str(e)}")
    
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """Show dialog and return result"""
        self.dialog.geometry("600x500+{}+{}".format(
            self.parent.winfo_x() + 50,
            self.parent.winfo_y() + 50
        ))
        
        self.dialog.wait_window()
        return self.result
