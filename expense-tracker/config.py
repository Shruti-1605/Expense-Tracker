import os

# Base directory of project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SQLite database path
DB_PATH = os.path.join(BASE_DIR, "data", "expenses.db")
