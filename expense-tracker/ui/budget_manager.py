import tkinter as tk
from tkinter import ttk, messagebox
from ui.styles import ModernStyle, create_card_frame
from business.budgets import BudgetManager

class BudgetManagerWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("💰 Budget Manager")
        self.geometry("800x600")
        self.configure(bg="#E6F3FF")
        
        # Configure styles
        ModernStyle.configure_styles()
        
        # Center window
        self.transient(master)
        self.grab_set()
        
        self.budget_manager = BudgetManager()
        self.setup_ui()
        self.load_budgets()
    
    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(main_container, text="💰 Budget Manager", 
                 style="Title.TLabel").pack(pady=(0, 20))
        
        # Add budget section
        add_frame = create_card_frame(main_container)
        add_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(add_frame, text="➕ Add New Budget", 
                 style="Heading.TLabel").pack(pady=(0, 15))
        
        # Form fields
        form_frame = ttk.Frame(add_frame)
        form_frame.pack(fill="x")
        
        # Category
        ttk.Label(form_frame, text="Category:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=(0, 10), sticky="w")
        self.category_entry = ttk.Entry(form_frame, width=20)
        self.category_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Amount
        ttk.Label(form_frame, text="Budget Amount (₹):", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=(0, 10), sticky="w")
        self.amount_entry = ttk.Entry(form_frame, width=15)
        self.amount_entry.grid(row=0, column=3, padx=(0, 20))
        
        # Period
        ttk.Label(form_frame, text="Period:", font=("Segoe UI", 10, "bold")).grid(row=0, column=4, padx=(0, 10), sticky="w")
        self.period_combo = ttk.Combobox(form_frame, values=["monthly", "weekly", "yearly"], 
                                        state="readonly", width=12)
        self.period_combo.set("monthly")
        self.period_combo.grid(row=0, column=5)
        
        # Add button
        add_btn = ttk.Button(add_frame, text="➕ Add Budget", command=self.add_budget,
                            style="Success.TButton")
        add_btn.pack(pady=(15, 0))
        
        # Budget list section
        list_frame = create_card_frame(main_container)
        list_frame.pack(fill="both", expand=True)
        
        ttk.Label(list_frame, text="📊 Current Budgets", 
                 style="Heading.TLabel").pack(pady=(0, 15))
        
        # Treeview for budgets
        self.tree = ttk.Treeview(list_frame, 
                                columns=("category", "budget", "spent", "remaining", "percentage", "status"),
                                show="headings", height=12)
        
        # Configure columns
        columns_config = {
            "category": ("Category", 120),
            "budget": ("Budget (₹)", 100),
            "spent": ("Spent (₹)", 100),
            "remaining": ("Remaining (₹)", 120),
            "percentage": ("Used %", 80),
            "status": ("Status", 100)
        }
        
        for col, (heading, width) in columns_config.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor="center")
        
        self.tree.pack(fill="both", expand=True, pady=(0, 15))
        
        # Action buttons
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack()
        
        refresh_btn = ttk.Button(btn_frame, text="🔄 Refresh", command=self.load_budgets,
                                style="Primary.TButton")
        refresh_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ttk.Button(btn_frame, text="🗑️ Delete Selected", command=self.delete_budget,
                               style="Danger.TButton")
        delete_btn.pack(side="left")
    
    def add_budget(self):
        """Add a new budget"""
        try:
            category = self.category_entry.get().strip()
            amount = float(self.amount_entry.get())
            period = self.period_combo.get()
            
            if not category or amount <= 0:
                messagebox.showerror("Error", "Please enter valid category and amount!")
                return
            
            if self.budget_manager.create_budget(category, amount, period):
                messagebox.showinfo("Success", f"Budget created for {category}")
                self.category_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                self.load_budgets()
            else:
                messagebox.showerror("Error", "Failed to create budget!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def load_budgets(self):
        """Load and display all budgets with their status"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get budget status for all categories
        budget_status_list = self.budget_manager.get_all_budget_status()
        
        for status in budget_status_list:
            # Determine status text and color
            if status['is_over_budget']:
                status_text = "⚠️ Over Budget"
                tags = ("over_budget",)
            elif status['percentage'] >= 80:
                status_text = "⚡ Near Limit"
                tags = ("warning",)
            else:
                status_text = "✅ On Track"
                tags = ("good",)
            
            # Insert row
            item = self.tree.insert("", "end", values=(
                status['category'],
                f"₹{status['budget_amount']:,.0f}",
                f"₹{status['spent_amount']:,.0f}",
                f"₹{status['remaining']:,.0f}",
                f"{status['percentage']:.1f}%",
                status_text
            ), tags=tags)
        
        # Configure row colors
        self.tree.tag_configure("over_budget", background="#FFE6E6")
        self.tree.tag_configure("warning", background="#FFF3CD")
        self.tree.tag_configure("good", background="#E6F7E6")
    
    def delete_budget(self):
        """Delete selected budget"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a budget to delete!")
            return
        
        category = self.tree.item(selected[0])["values"][0]
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete the budget for '{category}'?")
        
        if confirm:
            if self.budget_manager.delete_budget(category):
                messagebox.showinfo("Success", f"Budget for '{category}' deleted!")
                self.load_budgets()
            else:
                messagebox.showerror("Error", "Failed to delete budget!")