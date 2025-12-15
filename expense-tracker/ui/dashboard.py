import tkinter as tk
from tkinter import ttk
from ui.styles import ModernStyle, create_card_frame, create_icon_button
from services.database import Transaction
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.setup_dashboard()
        
    def setup_dashboard(self):
        # Dashboard title
        ttk.Label(self.parent, text="📊 Dashboard", 
                 style="Title.TLabel").pack(pady=(0, 20))
        
        # Top row - Summary cards
        self.create_summary_cards()
        
        # Middle row - Charts
        self.create_charts_section()
        
        # Bottom row - Recent transactions
        self.create_recent_transactions()
        
    def create_summary_cards(self):
        cards_frame = ttk.Frame(self.parent)
        cards_frame.pack(fill="x", pady=(0, 20))
        
        # Calculate statistics
        transactions = self.db.query(Transaction).all()
        current_month = datetime.now().strftime("%Y-%m")
        
        total_income = sum(t.amount for t in transactions if t.type == "income")
        total_expense = sum(t.amount for t in transactions if t.type == "expense")
        month_expense = sum(t.amount for t in transactions 
                           if t.type == "expense" and t.date.startswith(current_month))
        
        # Create summary cards
        cards_data = [
            ("💰 Total Income", f"₹{total_income:,.0f}", ModernStyle.SUCCESS),
            ("💸 Total Expense", f"₹{total_expense:,.0f}", ModernStyle.DANGER),
            ("📅 This Month", f"₹{month_expense:,.0f}", ModernStyle.PRIMARY),
            ("💳 Net Worth", f"₹{total_income - total_expense:,.0f}", 
             ModernStyle.SUCCESS if total_income >= total_expense else ModernStyle.DANGER)
        ]
        
        for i, (title, value, color) in enumerate(cards_data):
            card = create_card_frame(cards_frame)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10) if i < 3 else (0, 0))
            
            ttk.Label(card, text=title, font=("Segoe UI", 10)).pack()
            ttk.Label(card, text=value, font=("Segoe UI", 16, "bold"), 
                     foreground=color).pack(pady=(5, 0))
                     
    def create_charts_section(self):
        charts_frame = ttk.Frame(self.parent)
        charts_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Left chart - Monthly trend
        left_chart = create_card_frame(charts_frame)
        left_chart.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ttk.Label(left_chart, text="📈 Monthly Trend", 
                 style="Heading.TLabel").pack(pady=(0, 10))
        
        self.create_monthly_chart(left_chart)
        
        # Right chart - Category breakdown
        right_chart = create_card_frame(charts_frame)
        right_chart.pack(side="right", fill="both", expand=True)
        
        ttk.Label(right_chart, text="🥧 Category Breakdown", 
                 style="Heading.TLabel").pack(pady=(0, 10))
        
        self.create_category_chart(right_chart)
        
    def create_monthly_chart(self, parent):
        transactions = self.db.query(Transaction).all()
        monthly = defaultdict(lambda: {"income": 0, "expense": 0})
        
        for t in transactions:
            try:
                # Handle different date formats
                if len(t.date.split('-')) == 3:
                    month = datetime.strptime(t.date, "%Y-%m-%d").strftime("%Y-%m")
                else:
                    # Handle other formats like '2 07 2008'
                    parts = t.date.split()
                    if len(parts) == 3:
                        day, month_num, year = parts
                        month = f"{year}-{month_num.zfill(2)}"
                    else:
                        continue  # Skip invalid dates
                monthly[month][t.type] += t.amount
            except (ValueError, AttributeError):
                continue  # Skip invalid dates
            
        # Get last 6 months
        months = sorted(monthly.keys())[-6:]
        income = [monthly[m]["income"] for m in months]
        expense = [monthly[m]["expense"] for m in months]
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(months, income, label="Income", marker='o', color=ModernStyle.SUCCESS, linewidth=2)
        ax.plot(months, expense, label="Expense", marker='o', color=ModernStyle.DANGER, linewidth=2)
        ax.set_title("Last 6 Months Trend", fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def create_category_chart(self, parent):
        transactions = self.db.query(Transaction).filter(Transaction.type == "expense").all()
        categories = defaultdict(float)
        
        for t in transactions:
            categories[t.category or "Other"] += t.amount
            
        if categories:
            labels = list(categories.keys())[:5]  # Top 5 categories
            sizes = [categories[label] for label in labels]
            
            fig, ax = plt.subplots(figsize=(6, 3))
            colors = [ModernStyle.PRIMARY, ModernStyle.SECONDARY, ModernStyle.SUCCESS, 
                     ModernStyle.DANGER, ModernStyle.GRAY]
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)])
            ax.set_title("Top Expense Categories", fontsize=12, fontweight='bold')
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            ttk.Label(parent, text="No expense data available", 
                     font=("Segoe UI", 10)).pack(expand=True)
            
    def create_recent_transactions(self):
        recent_frame = create_card_frame(self.parent)
        recent_frame.pack(fill="x")
        
        ttk.Label(recent_frame, text="🕒 Recent Transactions", 
                 style="Heading.TLabel").pack(pady=(0, 10))
        
        # Get last 5 transactions
        recent_transactions = self.db.query(Transaction).order_by(Transaction.id.desc()).limit(5).all()
        
        if recent_transactions:
            # Create a simple table
            table_frame = ttk.Frame(recent_frame)
            table_frame.pack(fill="x")
            
            # Headers
            headers = ["Date", "Amount", "Type", "Category", "Notes"]
            for i, header in enumerate(headers):
                ttk.Label(table_frame, text=header, font=("Segoe UI", 10, "bold")).grid(
                    row=0, column=i, padx=10, pady=5, sticky="w")
            
            # Data rows
            for row, t in enumerate(recent_transactions, 1):
                ttk.Label(table_frame, text=t.date).grid(row=row, column=0, padx=10, pady=2, sticky="w")
                
                amount_color = ModernStyle.SUCCESS if t.type == "income" else ModernStyle.DANGER
                ttk.Label(table_frame, text=f"₹{t.amount:,.0f}", 
                         foreground=amount_color).grid(row=row, column=1, padx=10, pady=2, sticky="w")
                
                ttk.Label(table_frame, text=t.type.title()).grid(row=row, column=2, padx=10, pady=2, sticky="w")
                ttk.Label(table_frame, text=t.category or "N/A").grid(row=row, column=3, padx=10, pady=2, sticky="w")
                ttk.Label(table_frame, text=(t.notes or "")[:30] + ("..." if len(t.notes or "") > 30 else "")).grid(
                    row=row, column=4, padx=10, pady=2, sticky="w")
        else:
            ttk.Label(recent_frame, text="No transactions found. Add your first transaction!", 
                     font=("Segoe UI", 10)).pack(pady=20)