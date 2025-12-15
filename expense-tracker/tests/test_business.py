import unittest
import os
import tempfile
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import our modules
from services.database import Base, Transaction
from business.budgets import Budget, BudgetManager
from business.recurring import RecurringTransaction, RecurringManager

class TestBudgetManager(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        
        self.engine = create_engine(f"sqlite:///{self.test_db.name}")
        Base.metadata.create_all(self.engine)
        
        SessionLocal = sessionmaker(bind=self.engine)
        self.db = SessionLocal()
        
        # Patch the BudgetManager to use our test database
        self.budget_manager = BudgetManager()
        self.budget_manager.db = self.db
    
    def tearDown(self):
        """Clean up test database"""
        self.db.close()
        os.unlink(self.test_db.name)
    
    def test_create_budget(self):
        """Test creating a budget"""
        result = self.budget_manager.create_budget("Food", 5000, "monthly")
        self.assertTrue(result)
        
        # Check if budget was created
        budget = self.db.query(Budget).filter(Budget.category == "Food").first()
        self.assertIsNotNone(budget)
        self.assertEqual(budget.amount, 5000)
        self.assertEqual(budget.period, "monthly")
    
    def test_budget_status_calculation(self):
        """Test budget status calculation"""
        # Create a budget
        self.budget_manager.create_budget("Food", 5000, "monthly")
        
        # Add some transactions
        today = datetime.now().strftime("%Y-%m-%d")
        transaction1 = Transaction(date=today, amount=2000, type="expense", category="Food")
        transaction2 = Transaction(date=today, amount=1500, type="expense", category="Food")
        
        self.db.add(transaction1)
        self.db.add(transaction2)
        self.db.commit()
        
        # Check budget status
        status = self.budget_manager.get_budget_status("Food", "monthly")
        self.assertIsNotNone(status)
        self.assertEqual(status['budget_amount'], 5000)
        self.assertEqual(status['spent_amount'], 3500)
        self.assertEqual(status['remaining'], 1500)
        self.assertEqual(status['percentage'], 70.0)
        self.assertFalse(status['is_over_budget'])

if __name__ == '__main__':
    unittest.main()