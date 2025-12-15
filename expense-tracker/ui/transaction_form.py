import tkinter as tk
from tkinter import ttk, messagebox
from services.database import SessionLocal, Transaction
from ui.styles import ModernStyle, create_card_frame, create_icon_button
from ui.background import set_background_image
from datetime import datetime
from tkcalendar import DateEntry

class TransactionForm(tk.Toplevel):
    def __init__(self, master=None, transaction_id=None):
        super().__init__(master)
        self.title("💰 Add Transaction" if not transaction_id else "✏️ Edit Transaction")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Set simple background color
        self.configure(bg="#F0F8FF")
        
        # Center the window
        self.transient(master)
        self.grab_set()
        
        self.db = SessionLocal()
        self.transaction_id = transaction_id
        
        # Configure styles
        ModernStyle.configure_styles()
        
        self.setup_ui()
        
        # If edit mode, load existing data
        if self.transaction_id:
            self.load_transaction()
            
    def setup_ui(self):
        # Main container
        main_frame = create_card_frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_text = "Add New Transaction" if not self.transaction_id else "Edit Transaction"
        ttk.Label(main_frame, text=title_text, style="Title.TLabel").pack(pady=(0, 30))
        
        # Form fields
        self.create_form_fields(main_frame)
        
        # Buttons
        self.create_buttons(main_frame)
        
    def create_form_fields(self, parent):
        # Date field
        date_frame = ttk.Frame(parent)
        date_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(date_frame, text="📅 Date", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.date_entry = DateEntry(date_frame, width=12, background=ModernStyle.PRIMARY,
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(fill="x", pady=(5, 0))
        
        # Amount field
        amount_frame = ttk.Frame(parent)
        amount_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(amount_frame, text="💵 Amount (₹)", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.amount_entry = ttk.Entry(amount_frame, style="Modern.TEntry", font=("Segoe UI", 11))
        self.amount_entry.pack(fill="x", pady=(5, 0))
        
        # Type field
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(type_frame, text="📊 Type", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.type_entry = ttk.Combobox(type_frame, values=["income", "expense"], 
                                      state="readonly", font=("Segoe UI", 11))
        self.type_entry.pack(fill="x", pady=(5, 0))
        self.type_entry.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # Category field
        cat_frame = ttk.Frame(parent)
        cat_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(cat_frame, text="🏷️ Category", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        
        # Predefined categories based on type
        self.income_categories = ["Salary", "Freelance", "Investment", "Business", "Other"]
        self.expense_categories = ["Food", "Transportation", "Entertainment", "Shopping", 
                                 "Bills", "Healthcare", "Education", "Other"]
        
        self.cat_entry = ttk.Combobox(cat_frame, values=self.expense_categories, 
                                     font=("Segoe UI", 11))
        self.cat_entry.pack(fill="x", pady=(5, 0))
        
        # Notes field
        notes_frame = ttk.Frame(parent)
        notes_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(notes_frame, text="📝 Notes (Optional)", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        self.notes_entry = tk.Text(notes_frame, height=4, font=("Segoe UI", 10), 
                                  relief="solid", borderwidth=2)
        self.notes_entry.pack(fill="x", pady=(5, 0))
        
    def on_type_change(self, event=None):
        """Update category options based on transaction type"""
        transaction_type = self.type_entry.get()
        if transaction_type == "income":
            self.cat_entry['values'] = self.income_categories
        else:
            self.cat_entry['values'] = self.expense_categories
        self.cat_entry.set('')  # Clear current selection
        
    def create_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        # Cancel button with maximum visibility
        cancel_btn = tk.Button(btn_frame, text="❌ CANCEL", command=self.destroy,
                              bg="#FF0000", fg="#FFFFFF", font=("Segoe UI", 12, "bold"),
                              relief="raised", bd=3, padx=20, pady=10)
        cancel_btn.pack(side="right", padx=(10, 0))
        
        # Save button with maximum visibility
        save_text = "💾 SAVE" if not self.transaction_id else "✅ UPDATE"
        save_btn = tk.Button(btn_frame, text=save_text, command=self.save_transaction,
                            bg="#00FF00", fg="#000000", font=("Segoe UI", 12, "bold"),
                            relief="raised", bd=3, padx=20, pady=10)
        save_btn.pack(side="right")

    def load_transaction(self):
        t = self.db.query(Transaction).filter(Transaction.id == self.transaction_id).first()
        if t:
            # Set date
            self.date_entry.set_date(datetime.strptime(t.date, "%Y-%m-%d").date())
            
            # Set amount
            self.amount_entry.insert(0, str(t.amount))
            
            # Set type and update categories
            self.type_entry.set(t.type)
            self.on_type_change()
            
            # Set category
            self.cat_entry.set(t.category or "")
            
            # Set notes
            if t.notes:
                self.notes_entry.insert("1.0", t.notes)

    def save_transaction(self):
        try:
            # Validate inputs
            if not self.amount_entry.get() or not self.type_entry.get():
                messagebox.showerror("Error", "Please fill in all required fields!")
                return
                
            date = self.date_entry.get()
            amount = float(self.amount_entry.get())
            t_type = self.type_entry.get()
            category = self.cat_entry.get() or "Other"
            notes = self.notes_entry.get("1.0", tk.END).strip()
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0!")
                return

            if self.transaction_id:
                # Update existing
                t = self.db.query(Transaction).filter(Transaction.id == self.transaction_id).first()
                t.date = date
                t.amount = amount
                t.type = t_type
                t.category = category
                t.notes = notes
                self.db.commit()
                messagebox.showinfo("✅ Success", "Transaction updated successfully!")
            else:
                # Add new
                t = Transaction(date=date, amount=amount, type=t_type, category=category, notes=notes)
                self.db.add(t)
                self.db.commit()
                messagebox.showinfo("✅ Success", "Transaction added successfully!")

            self.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
