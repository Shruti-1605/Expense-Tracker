import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from services.database import SessionLocal, Transaction
from datetime import datetime, timedelta
from collections import defaultdict
from ui.styles import ModernStyle

db = SessionLocal()

# Configure matplotlib for better appearance
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'Segoe UI'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'

def embed_chart_in_window(parent, fig, canvas_holder=None):
    """Embed chart into Tkinter window, supports refresh"""
    if canvas_holder:
        canvas_holder.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas

# Example: Monthly Summary
def plot_monthly_summary(parent=None, canvas_holder=None):
    transactions = db.query(Transaction).all()
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

    months = sorted(monthly.keys())[-12:]  # Last 12 months
    income = [monthly[m]["income"] for m in months]
    expense = [monthly[m]["expense"] for m in months]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    
    # Plot with modern colors
    ax.plot(months, income, label="💰 Income", marker='o', 
           color=ModernStyle.SUCCESS, linewidth=3, markersize=8)
    ax.plot(months, expense, label="💸 Expense", marker='o', 
           color=ModernStyle.DANGER, linewidth=3, markersize=8)
    
    ax.set_title("📈 Monthly Income vs Expense Trend", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Month", fontsize=12, fontweight='bold')
    ax.set_ylabel("Amount (₹)", fontsize=12, fontweight='bold')
    
    # Format y-axis to show currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
    
    ax.legend(fontsize=11, frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()

    if parent:
        return embed_chart_in_window(parent, fig, canvas_holder)
    else:
        plt.show()

def plot_category_breakdown(parent=None, canvas_holder=None):
    """Create a pie chart showing expense breakdown by category"""
    transactions = db.query(Transaction).filter(Transaction.type == "expense").all()
    categories = defaultdict(float)
    
    for t in transactions:
        categories[t.category or "Other"] += t.amount
        
    if not categories:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'No expense data available', 
               horizontalalignment='center', verticalalignment='center',
               transform=ax.transAxes, fontsize=14)
        ax.set_title("🥧 Expense Categories")
    else:
        labels = list(categories.keys())
        sizes = list(categories.values())
        
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('white')
        
        colors = [ModernStyle.PRIMARY, ModernStyle.SECONDARY, ModernStyle.SUCCESS, 
                 ModernStyle.DANGER, ModernStyle.GRAY, '#FF6B6B', '#4ECDC4', '#45B7D1']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                         colors=colors[:len(labels)], startangle=90,
                                         textprops={'fontsize': 10})
        
        # Enhance the appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            
        ax.set_title("🥧 Expense Breakdown by Category", fontsize=16, fontweight='bold', pad=20)
        
    plt.tight_layout()
    
    if parent:
        return embed_chart_in_window(parent, fig, canvas_holder)
    else:
        plt.show()

def plot_expense_trend(parent=None, canvas_holder=None):
    """Create a line chart showing expense trend over last 12 months"""
    transactions = db.query(Transaction).filter(Transaction.type == "expense").all()
    monthly_expenses = defaultdict(float)
    
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
            monthly_expenses[month] += t.amount
        except (ValueError, AttributeError):
            continue  # Skip invalid dates
        
    months = sorted(monthly_expenses.keys())[-12:]  # Last 12 months
    expenses = [monthly_expenses[m] for m in months]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    
    ax.plot(months, expenses, marker='o', color=ModernStyle.DANGER, 
           linewidth=3, markersize=8, markerfacecolor='white', 
           markeredgecolor=ModernStyle.DANGER, markeredgewidth=2)
    
    # Fill area under the curve
    ax.fill_between(months, expenses, alpha=0.3, color=ModernStyle.DANGER)
    
    ax.set_title("📉 Expense Trend (Last 12 Months)", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel("Month", fontsize=12, fontweight='bold')
    ax.set_ylabel("Expense Amount (₹)", fontsize=12, fontweight='bold')
    
    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
    
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if parent:
        return embed_chart_in_window(parent, fig, canvas_holder)
    else:
        plt.show()
