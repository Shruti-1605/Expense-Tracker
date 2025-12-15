from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_PATH

# Database engine
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Base class for models
Base = declarative_base()

# Session
SessionLocal = sessionmaker(bind=engine)

# -------------------
# Transaction Model
# -------------------
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income or expense
    category = Column(String, nullable=True)
    notes = Column(String, nullable=True)
