import tkinter as tk
from tkinter import ttk, messagebox
from services.database import SessionLocal, Transaction
from ui.transaction_form import TransactionForm
from ui.styles import ModernStyle, create_card_frame, create_icon_button
from ui.background import set_background_image
from datetime import datetime

class TransactionList(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("📋 Transaction History")
        self.geometry("1100x700")
        self.db = SessionLocal()
        
        # Set simple background color
        self.configure(bg="#E6F3FF")
        
        # Configure styles
        ModernStyle.configure_styles()
        
        # Center window
        self.transient(master)
        self.grab_set()

        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_container, text="📋 Transaction History", 
                 style="Title.TLabel").pack(pady=(0, 20))
        
        # Filters card
        filter_card = create_card_frame(main_container)
        filter_card.pack(fill="x", pady=(0, 20))
        
        ttk.Label(filter_card, text="🔍 Filters", 
                 style="Heading.TLabel").pack(pady=(0, 15))
        
        filter_grid = ttk.Frame(filter_card)
        filter_grid.pack(fill="x")

        # Type Filter
        ttk.Label(filter_grid, text="Type:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.type_var = tk.StringVar()
        type_options = ["All", "income", "expense"]
        self.type_combo = ttk.Combobox(filter_grid, values=type_options, textvariable=self.type_var, 
                                      state="readonly", width=15)
        self.type_combo.current(0)
        self.type_combo.grid(row=0, column=1, padx=5, pady=5)

        # Category Filter
        ttk.Label(filter_grid, text="Category:", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=(20, 5), sticky="w")
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(filter_grid, values=["All"], textvariable=self.cat_var, 
                                     state="readonly", width=15)
        self.cat_combo.current(0)
        self.cat_combo.grid(row=0, column=3, padx=5, pady=5)

        # Date Range
        ttk.Label(filter_grid, text="Start Date:", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, padx=(0, 5), sticky="w")
        self.start_date = ttk.Entry(filter_grid, width=15)
        self.start_date.grid(row=1, column=1, padx=5, pady=5)
        self.start_date.insert(0, "YYYY-MM-DD")

        ttk.Label(filter_grid, text="End Date:", font=("Segoe UI", 10, "bold")).grid(row=1, column=2, padx=(20, 5), sticky="w")
        self.end_date = ttk.Entry(filter_grid, width=15)
        self.end_date.grid(row=1, column=3, padx=5, pady=5)
        self.end_date.insert(0, "YYYY-MM-DD")

        # Filter buttons
        btn_frame = ttk.Frame(filter_card)
        btn_frame.pack(pady=(15, 0))
        
        apply_btn = ttk.Button(btn_frame, text="🔍 Apply Filters", command=self.apply_filters,
                              style="Primary.TButton")
        apply_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ttk.Button(btn_frame, text="🔄 Clear Filters", command=self.clear_filters,
                              style="Primary.TButton")
        clear_btn.pack(side="left")

        # Transactions table card
        table_card = create_card_frame(main_container)
        table_card.pack(fill="both", expand=True, pady=(0, 20))
        
        ttk.Label(table_card, text="📊 Transactions", 
                 style="Heading.TLabel").pack(pady=(0, 15))
        
        # Treeview for Transactions
        tree_frame = ttk.Frame(table_card)
        tree_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "date", "amount", "type", "category", "notes"),
            show="headings",
            height=15,
            style="Modern.Treeview"
        )
        
        # Configure columns
        columns_config = {
            "id": ("ID", 50),
            "date": ("Date", 100),
            "amount": ("Amount (₹)", 120),
            "type": ("Type", 80),
            "category": ("Category", 120),
            "notes": ("Notes", 200)
        }
        
        for col, (heading, width) in columns_config.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor="center" if col in ["amount", "type"] else "w")
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        action_card = create_card_frame(main_container)
        action_card.pack(fill="x")
        
        btn_frame = ttk.Frame(action_card)
        btn_frame.pack()
        
        # Create buttons with explicit styling
        edit_btn = ttk.Button(btn_frame, text="✏️ Edit Selected", command=self.edit_transaction, 
                             style="Primary.TButton")
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ttk.Button(btn_frame, text="🗑️ Delete Selected", command=self.delete_transaction, 
                               style="Danger.TButton")
        delete_btn.pack(side="left", padx=(0, 10))
        
        add_btn = ttk.Button(btn_frame, text="➕ Add New", command=self.add_new_transaction, 
                            style="Success.TButton")
        add_btn.pack(side="left")

        # Load all transactions initially
        self.load_transactions()
        self.load_categories()
        
    def clear_filters(self):
        """Clear all filters and reload transactions"""
        self.type_combo.current(0)
        self.cat_combo.current(0)
        self.start_date.delete(0, tk.END)
        self.start_date.insert(0, "YYYY-MM-DD")
        self.end_date.delete(0, tk.END)
        self.end_date.insert(0, "YYYY-MM-DD")
        self.load_transactions()
        
    def add_new_transaction(self):
        """Open form to add new transaction"""
        form = TransactionForm(self)
        self.wait_window(form)
        self.load_transactions()
        self.load_categories()

    def load_categories(self):
        cats = set([t.category for t in self.db.query(Transaction).all() if t.category])
        self.cat_combo["values"] = ["All"] + list(cats)

    def load_transactions(self, filters=None):
        # Clear current tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        query = self.db.query(Transaction)

        if filters:
            if filters.get("type") and filters["type"] != "All":
                query = query.filter(Transaction.type == filters["type"])
            if filters.get("category") and filters["category"] != "All":
                query = query.filter(Transaction.category == filters["category"])
            if filters.get("start_date"):
                query = query.filter(Transaction.date >= filters["start_date"])
            if filters.get("end_date"):
                query = query.filter(Transaction.date <= filters["end_date"])

        for t in query.all():
            # Format amount with currency symbol and color coding
            amount_display = f"₹{t.amount:,.0f}"
            
            # Insert with tags for styling
            item = self.tree.insert("", "end", values=(t.id, t.date, amount_display, 
                                                       t.type.title(), t.category or "N/A", 
                                                       (t.notes or "")[:50] + ("..." if len(t.notes or "") > 50 else "")))
            
            # Add tags for income/expense styling
            if t.type == "income":
                self.tree.set(item, "type", "💰 Income")
            else:
                self.tree.set(item, "type", "💸 Expense")

    def apply_filters(self):
        filters = {
            "type": self.type_var.get(),
            "category": self.cat_var.get(),
            "start_date": self.start_date.get() if self.start_date.get() and self.start_date.get() != "YYYY-MM-DD" else None,
            "end_date": self.end_date.get() if self.end_date.get() and self.end_date.get() != "YYYY-MM-DD" else None
        }
        self.load_transactions(filters)

    def edit_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No transaction selected!")
            return
        t_id = self.tree.item(selected[0])["values"][0]

        # Open TransactionForm in Edit mode
        form = TransactionForm(self, transaction_id=t_id)
        form.grab_set()
        self.wait_window(form)  # Wait until form is closed

        # Refresh transaction list after editing
        self.load_transactions()
        self.load_categories()

    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No transaction selected!")
            return
        t_id = self.tree.item(selected[0])["values"][0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete transaction ID: {t_id}?")
        if confirm:
            t = self.db.query(Transaction).filter(Transaction.id == t_id).first()
            if t:
                self.db.delete(t)
                self.db.commit()
                messagebox.showinfo("Deleted", "Transaction deleted successfully!")
                self.load_transactions()
                self.load_categories()
