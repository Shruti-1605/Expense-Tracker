from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from services.database import Base, SessionLocal, Transaction
from datetime import datetime, timedelta
from collections import defaultdict

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    period = Column(String, default="monthly")  # monthly, weekly, yearly
    start_date = Column(String, nullable=False)

class BudgetManager:
    def __init__(self):
        self.db = SessionLocal()
    
    def create_budget(self, category, amount, period="monthly"):
        """Create a new budget for a category"""
        try:
            # Check if budget already exists for this category
            existing = self.db.query(Budget).filter(Budget.category == category).first()
            if existing:
                existing.amount = amount
                existing.period = period
                existing.start_date = datetime.now().strftime("%Y-%m-%d")
            else:
                budget = Budget(
                    category=category,
                    amount=amount,
                    period=period,
                    start_date=datetime.now().strftime("%Y-%m-%d")
                )
                self.db.add(budget)
            
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error creating budget: {e}")
            return False
    
    def get_all_budgets(self):
        """Get all budgets"""
        return self.db.query(Budget).all()
    
    def get_budget_status(self, category, period="monthly"):
        """Get current spending vs budget for a category"""
        try:
            budget = self.db.query(Budget).filter(Budget.category == category).first()
            if not budget:
                return None
            
            # Calculate date range based on period
            today = datetime.now()
            if period == "monthly":
                start_date = today.replace(day=1)
            elif period == "weekly":
                start_date = today - timedelta(days=today.weekday())
            else:  # yearly
                start_date = today.replace(month=1, day=1)
            
            start_date_str = start_date.strftime("%Y-%m-%d")
            
            # Get total spending in this period for this category
            spent = self.db.query(Transaction).filter(
                Transaction.category == category,
                Transaction.type == "expense",
                Transaction.date >= start_date_str
            ).all()
            
            total_spent = sum(t.amount for t in spent)
            
            return {
                'budget_amount': budget.amount,
                'spent_amount': total_spent,
                'remaining': budget.amount - total_spent,
                'percentage': (total_spent / budget.amount * 100) if budget.amount > 0 else 0,
                'is_over_budget': total_spent > budget.amount
            }
            
        except Exception as e:
            print(f"Error getting budget status: {e}")
            return None
    
    def get_all_budget_status(self):
        """Get budget status for all categories"""
        budgets = self.get_all_budgets()
        status_list = []
        
        for budget in budgets:
            status = self.get_budget_status(budget.category, budget.period)
            if status:
                status['category'] = budget.category
                status['period'] = budget.period
                status_list.append(status)
        
        return status_list
    
    def delete_budget(self, category):
        """Delete a budget"""
        try:
            budget = self.db.query(Budget).filter(Budget.category == category).first()
            if budget:
                self.db.delete(budget)
                self.db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error deleting budget: {e}")
            return False
    
    def get_budget_alerts(self):
        """Get alerts for budgets that are over or near limit"""
        alerts = []
        status_list = self.get_all_budget_status()
        
        for status in status_list:
            if status['is_over_budget']:
                alerts.append({
                    'type': 'over_budget',
                    'category': status['category'],
                    'message': f"Over budget in {status['category']}: ₹{status['spent_amount']:.0f} / ₹{status['budget_amount']:.0f}"
                })
            elif status['percentage'] >= 80:  # Warning at 80%
                alerts.append({
                    'type': 'warning',
                    'category': status['category'],
                    'message': f"Near budget limit in {status['category']}: {status['percentage']:.0f}% used"
                })
        
        return alerts