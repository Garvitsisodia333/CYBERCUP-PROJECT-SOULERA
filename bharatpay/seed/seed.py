"""
BharatPay Synthetic Data Generator & Seed Script
Generates fictional Indian users, UPI VPAs, accounts, KYC records, and transactions.
All values are clearly synthetic test data for CC6-IC07 hackathon demo.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.db.session import SessionLocal, engine
from app.db.base import Base
import app.models

def seed_database():
    print("[BharatPay Seed] Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        print("[BharatPay Seed] Ready for seeding in Checkpoint 1 & 8.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
