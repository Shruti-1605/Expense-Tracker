from sqlalchemy import Column, Integer, String, Float, Text
from services.database import Base, SessionLocal, Transaction
from datetime import datetime, timedelta
import json

class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income or expense
    category = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    frequency = Column(String, nullable=False)  # daily, weekly, monthly, yearly
    next_date = Column(String, nullable=False)
    is_active = Column(String, default="true")

class RecurringManager:
    def __init__(self):
        self.db = SessionLocal()
    
    def create_recurring(self, name, amount, transaction_type, category, notes, frequency, start_date):
        """Create a new recurring transaction"""
        try:
            recurring = RecurringTransaction(
                name=name,
                amount=amount,
                type=transaction_type,
                category=category,
                notes=notes,
                frequency=frequency,
                next_date=start_date,
                is_active="true"
            )
            
            self.db.add(recurring)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error creating recurring transaction: {e}")
            return False
    
    def get_all_recurring(self):
        """Get all recurring transactions"""
        return self.db.query(RecurringTransaction).filter(RecurringTransaction.is_active == "true").all()
    
    def calculate_next_date(self, current_date, frequency):
        """Calculate next occurrence date based on frequency"""
        date_obj = datetime.strptime(current_date, "%Y-%m-%d")
        
        if frequency == "daily":
            next_date = date_obj + timedelta(days=1)
        elif frequency == "weekly":
            next_date = date_obj + timedelta(weeks=1)
        elif frequency == "monthly":
            # Handle month-end dates properly
            if date_obj.month == 12:
                next_date = date_obj.replace(year=date_obj.year + 1, month=1)
            else:
                try:
                    next_date = date_obj.replace(month=date_obj.month + 1)
                except ValueError:
                    # Handle cases like Jan 31 -> Feb 28
                    next_date = date_obj.replace(month=date_obj.month + 1, day=28)
        elif frequency == "yearly":
            try:
                next_date = date_obj.replace(year=date_obj.year + 1)
            except ValueError:
                # Handle leap year Feb 29
                next_date = date_obj.replace(year=date_obj.year + 1, day=28)
        else:
            return current_date
        
        return next_date.strftime("%Y-%m-%d")
    
    def process_due_recurring(self):
        """Process all recurring transactions that are due"""
        today = datetime.now().strftime("%Y-%m-%d")
        recurring_list = self.get_all_recurring()
        processed_count = 0
        
        for recurring in recurring_list:
            if recurring.next_date <= today:
                # Create the actual transaction
                transaction = Transaction(
                    date=recurring.next_date,
                    amount=recurring.amount,
                    type=recurring.type,
                    category=recurring.category,
                    notes=f"[Recurring: {recurring.name}] {recurring.notes or ''}"
                )
                
                self.db.add(transaction)
                
                # Update next occurrence date
                recurring.next_date = self.calculate_next_date(recurring.next_date, recurring.frequency)
                
                processed_count += 1
        
        if processed_count > 0:
            self.db.commit()
        
        return processed_count
    
    def update_recurring(self, recurring_id, **kwargs):
        """Update a recurring transaction"""
        try:
            recurring = self.db.query(RecurringTransaction).filter(RecurringTransaction.id == recurring_id).first()
            if recurring:
                for key, value in kwargs.items():
                    if hasattr(recurring, key):
                        setattr(recurring, key, value)
                
                self.db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error updating recurring transaction: {e}")
            return False
    
    def delete_recurring(self, recurring_id):
        """Delete (deactivate) a recurring transaction"""
        try:
            recurring = self.db.query(RecurringTransaction).filter(RecurringTransaction.id == recurring_id).first()
            if recurring:
                recurring.is_active = "false"
                self.db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deleting recurring transaction: {e}")
            return False
    
    def get_upcoming_recurring(self, days_ahead=30):
        """Get recurring transactions due in the next N days"""
        end_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        recurring_list = self.get_all_recurring()
        
        upcoming = []
        for recurring in recurring_list:
            if recurring.next_date <= end_date:
                upcoming.append({
                    'id': recurring.id,
                    'name': recurring.name,
                    'amount': recurring.amount,
                    'type': recurring.type,
                    'category': recurring.category,
                    'next_date': recurring.next_date,
                    'frequency': recurring.frequency
                })
        
        return sorted(upcoming, key=lambda x: x['next_date'])