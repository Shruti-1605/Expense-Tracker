import tkinter as tk
from tkinter import ttk
from ui.transaction_form import TransactionForm
from ui.transaction_list import TransactionList
from ui.dashboard import Dashboard
from ui.styles import ModernStyle, create_card_frame, create_icon_button
from ui.background import set_background_image
from utils.charts import plot_monthly_summary, plot_category_breakdown, plot_expense_trend
from utils.import_export import ImportExport
from ui.budget_manager import BudgetManagerWindow
from services.database import SessionLocal, Transaction
from datetime import datetime, timedelta

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💰 Personal Expense Tracker")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # Maximize window
        
        # Configure modern styles
        ModernStyle.configure_styles()
        
        self.db = SessionLocal()
        
        # Set simple background color instead of image
        self.root.configure(bg="#E6F3FF")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_container)
        
        # Content area with sidebar and main content
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Sidebar
        self.create_sidebar(content_frame)
        
        # Main content area
        self.main_content = ttk.Frame(content_frame)
        self.main_content.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        # Load dashboard by default
        self.show_dashboard()
        
    def create_header(self, parent):
        header_frame = create_card_frame(parent)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title and stats in header
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill="x")
        
        ttk.Label(title_frame, text="💰 Personal Expense Tracker", 
                 style="Title.TLabel").pack(side="left")
        
        # Quick stats
        stats_frame = ttk.Frame(title_frame)
        stats_frame.pack(side="right")
        
        self.update_header_stats(stats_frame)
        
    def update_header_stats(self, parent):
        # Clear existing stats
        for widget in parent.winfo_children():
            widget.destroy()
            
        # Calculate current month stats
        current_month = datetime.now().strftime("%Y-%m")
        transactions = self.db.query(Transaction).all()
        
        month_income = sum(t.amount for t in transactions 
                          if t.type == "income" and t.date.startswith(current_month))
        month_expense = sum(t.amount for t in transactions 
                           if t.type == "expense" and t.date.startswith(current_month))
        balance = month_income - month_expense
        
        # Stats display
        stats = [
            ("This Month Income", f"₹{month_income:,.0f}", ModernStyle.SUCCESS),
            ("This Month Expense", f"₹{month_expense:,.0f}", ModernStyle.DANGER),
            ("Balance", f"₹{balance:,.0f}", ModernStyle.SUCCESS if balance >= 0 else ModernStyle.DANGER)
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_frame = ttk.Frame(parent)
            stat_frame.pack(side="left", padx=(20, 0))
            
            ttk.Label(stat_frame, text=label, font=("Segoe UI", 9)).pack()
            ttk.Label(stat_frame, text=value, font=("Segoe UI", 12, "bold"), 
                     foreground=color).pack()
    
    def create_sidebar(self, parent):
        sidebar = ttk.Frame(parent, style="Sidebar.TFrame")
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.configure(padding=(20, 20))
        
        # Sidebar title
        ttk.Label(sidebar, text="📊 MENU", style="Sidebar.TLabel", 
                 font=("Segoe UI", 14, "bold")).pack(pady=(0, 30))
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("➕ Add Transaction", self.open_add_form),
            ("📋 View Transactions", self.open_transaction_list),
            ("📈 Reports", self.show_reports),
            ("💰 Budgets", self.open_budget_manager)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(sidebar, text=text, command=command, 
                           style="Sidebar.TButton", width=20)
            btn.pack(pady=(0, 8), fill="x", padx=5)
            
    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
    def show_dashboard(self):
        self.clear_main_content()
        dashboard = Dashboard(self.main_content, self.db)
        self.update_header_stats(self.main_content.master.master.winfo_children()[0].winfo_children()[0].winfo_children()[1])
        
    def show_reports(self):
        self.clear_main_content()
        
        # Reports header
        ttk.Label(self.main_content, text="📈 Reports & Analytics", 
                 style="Title.TLabel").pack(pady=(0, 20))
        
        # Reports grid
        reports_frame = ttk.Frame(self.main_content)
        reports_frame.pack(fill="both", expand=True)
        
        # Chart buttons in a grid
        chart_frame = create_card_frame(reports_frame)
        chart_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(chart_frame, text="📊 Visual Reports", 
                 style="Heading.TLabel").pack(pady=(0, 15))
        
        btn_frame = ttk.Frame(chart_frame)
        btn_frame.pack()
        
        monthly_btn = ttk.Button(btn_frame, text="📈 Monthly Summary", 
                                command=lambda: self.open_chart(plot_monthly_summary),
                                style="Primary.TButton")
        monthly_btn.pack(side="left", padx=(0, 10))
        
        category_btn = ttk.Button(btn_frame, text="🥧 Category Breakdown", 
                                 command=lambda: self.open_chart(plot_category_breakdown),
                                 style="Primary.TButton")
        category_btn.pack(side="left", padx=(0, 10))
        
        trend_btn = ttk.Button(btn_frame, text="📉 Expense Trend", 
                              command=lambda: self.open_chart(plot_expense_trend),
                              style="Primary.TButton")
        trend_btn.pack(side="left")
        
        # Import/Export section
        import_export_frame = create_card_frame(reports_frame)
        import_export_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(import_export_frame, text="💾 Import/Export Data", 
                 style="Heading.TLabel").pack(pady=(0, 15))
        
        ie_btn_frame = ttk.Frame(import_export_frame)
        ie_btn_frame.pack()
        
        export_csv_btn = ttk.Button(ie_btn_frame, text="📄 Export CSV", 
                                   command=self.export_csv, style="Success.TButton")
        export_csv_btn.pack(side="left", padx=(0, 10))
        
        import_csv_btn = ttk.Button(ie_btn_frame, text="📅 Import CSV", 
                                   command=self.import_csv, style="Primary.TButton")
        import_csv_btn.pack(side="left", padx=(0, 10))
        
        backup_btn = ttk.Button(ie_btn_frame, text="💾 Backup DB", 
                               command=self.backup_database, style="Primary.TButton")
        backup_btn.pack(side="left")
        


    def open_add_form(self):
        form = TransactionForm(self.root)
        form.grab_set()
        # Refresh dashboard after adding transaction
        self.root.after(100, lambda: self.update_header_stats(
            self.main_content.master.master.winfo_children()[0].winfo_children()[0].winfo_children()[1]))

    def open_transaction_list(self):
        TransactionList(self.root)

    def open_chart(self, chart_func):
        win = tk.Toplevel(self.root)
        win.title("📊 Financial Report")
        win.geometry("1000x700")
        win.configure(bg=ModernStyle.WHITE)
        chart_func(parent=win)
    
    def export_csv(self):
        """Export transactions to CSV"""
        ie = ImportExport()
        ie.export_to_csv()
    
    def import_csv(self):
        """Import transactions from CSV"""
        ie = ImportExport()
        if ie.import_from_csv():
            # Refresh dashboard after import
            self.show_dashboard()
    
    def backup_database(self):
        """Backup database"""
        ie = ImportExport()
        ie.backup_database()
    
    def open_budget_manager(self):
        """Open budget manager window"""
        BudgetManagerWindow(self.root)

    def run(self):
        self.root.mainloop()
