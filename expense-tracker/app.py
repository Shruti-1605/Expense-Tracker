from services.database import Base, engine
from ui.main_window import MainWindow
from business.budgets import Budget
from business.recurring import RecurringTransaction, RecurringManager

def setup_database():
    Base.metadata.create_all(engine)
    print("Database setup complete!")

def process_recurring_transactions():
    """Process any due recurring transactions at startup"""
    try:
        recurring_manager = RecurringManager()
        processed = recurring_manager.process_due_recurring()
        if processed > 0:
            print(f"Processed {processed} recurring transactions")
    except Exception as e:
        print(f"Error processing recurring transactions: {e}")

if __name__ == "__main__":
    setup_database()
    process_recurring_transactions()

    # Start GUI
    app = MainWindow()
    app.run()
