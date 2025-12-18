# 💰 Personal Expense Tracker

A comprehensive desktop application for tracking personal income and expenses, built with Python and Tkinter.

## 🚀 Features

### Core Functionality
- ✅ **Transaction Management**: Add, edit, delete transactions with date, amount, category, and notes
- ✅ **Categorization**: Organize transactions by income/expense types and custom categories
- ✅ **Budget Management**: Set monthly budgets per category with alerts and tracking
- ✅ **Search & Filters**: Filter transactions by date range, category, type, and amount
- ✅ **Reports & Charts**: Visual analytics with monthly summaries, category breakdowns, and trends
- ✅ **Import/Export**: CSV and JSON import/export functionality
- ✅ **Backup & Restore**: Database backup and restore capabilities
- ✅ **Recurring Transactions**: Automated recurring income and expenses

### User Interface
- 🎨 **Modern GUI**: Professional interface with sidebar navigation
- 📊 **Interactive Dashboard**: Real-time financial overview with charts
- 🎯 **Budget Alerts**: Visual indicators for budget status and warnings
- 📱 **Responsive Design**: Clean, intuitive layout with proper styling

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **GUI Framework**: Tkinter (built-in)
- **Database**: SQLite with SQLAlchemy ORM
- **Charts**: Matplotlib with Seaborn styling
- **Date Handling**: tkcalendar for date picker
- **Image Processing**: Pillow for UI enhancements
- **Packaging**: PyInstaller for executable creation

## 📦 Installation

### Option 1: Run from Source
1. **Install Python 3.10+** from [python.org](https://python.org)

2. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd expense-tracker
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

### Option 2: Download Executable
1. Download the latest release from the releases page
2. Extract and run `ExpenseTracker.exe`

## 🏗️ Project Structure

```
expense-tracker/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── build_executable.py    # Build script for creating executable
├── README.md             # This file
├── business/             # Business logic layer
│   ├── budgets.py        # Budget management
│   └── recurring.py      # Recurring transactions
├── services/             # Data access layer
│   ├── database.py       # Database models and connection
│   ├── budget_service.py # Budget-related services
│   ├── expense_service.py# Transaction services
│   └── report_service.py # Report generation
├── ui/                   # User interface layer
│   ├── main_window.py    # Main application window
│   ├── dashboard.py      # Dashboard with charts and stats
│   ├── transaction_form.py# Add/edit transaction form
│   ├── transaction_list.py# Transaction history view
│   ├── budget_manager.py # Budget management window
│   └── styles.py         # UI styling and themes
├── utils/                # Utility modules
│   ├── charts.py         # Chart generation
│   ├── import_export.py  # Data import/export
│   ├── helpers.py        # Helper functions
│   └── validators.py     # Input validation
├── tests/                # Unit tests
│   └── test_business.py  # Business logic tests
└── data/                 # Database storage
    └── expenses.db       # SQLite database file
```

## 🎯 Quick Start Guide

### 1. Adding Your First Transaction
- Click **"➕ Add Transaction"** in the sidebar
- Select date using the date picker
- Enter amount (e.g., 5000)
- Choose **Income** or **Expense**
- Select category (Food, Salary, etc.)
- Add optional notes
- Click **"💾 SAVE"**

### 2. Setting Up Budgets
- Click **"💰 Budgets"** in the sidebar
- Enter category name (e.g., "Food")
- Set budget amount (e.g., 10000)
- Choose period (Monthly/Weekly/Yearly)
- Click **"➕ Add Budget"**

### 3. Viewing Reports
- Click **"📈 Reports"** in the sidebar
- Choose from:
  - **Monthly Summary**: Income vs Expense trends
  - **Category Breakdown**: Spending by category
  - **Expense Trend**: Monthly expense patterns

### 4. Import/Export Data
- In Reports section, use:
  - **"📄 Export CSV"**: Save all transactions
  - **"📅 Import CSV"**: Load transactions from file
  - **"💾 Backup DB"**: Create database backup

## 🔧 System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, Linux
- **Python**: 3.10 or higher
- **RAM**: 512 MB minimum
- **Storage**: 100 MB free space
- **Display**: 1024x768 minimum resolution

## 🧪 Testing

Run tests to verify installation:
```bash
# Test basic functionality
python -c "import app; print('✅ Installation successful')"

# Run unit tests
set PYTHONPATH=. && python tests/test_business.py
```

## 📦 Building Executable

Create a standalone .exe file:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_executable.py

# Find ExpenseTracker.exe in dist/ folder
```

## 🚀 Advanced Features

### Recurring Transactions
- Set up automatic monthly salary entries
- Configure recurring bills and subscriptions
- System processes them automatically at startup

### Budget Alerts
- 🟢 **Green**: Under 80% of budget
- 🟡 **Yellow**: 80-100% of budget used
- 🔴 **Red**: Over budget limit

### Data Management
- **CSV Import**: Bulk import from spreadsheets
- **JSON Export**: Structured data export
- **Database Backup**: Complete data protection



## 📸 Project Screenshots

![Screenshot 84](images/Screenshot%20(84).png)
![Screenshot 85](images/Screenshot%20(85).png)
![Screenshot 86](images/Screenshot%20(86).png)
![Screenshot 87](images/Screenshot%20(87).png)
![Screenshot 88](images/Screenshot%20(88).png)
![Screenshot 89](images/Screenshot%20(89).png)
![Screenshot 90](images/Screenshot%20(90).png)
![Screenshot 91](images/Screenshot%20(91).png)
![Screenshot 95](images/Screenshot%20(95)%20-%20Copy.png)


