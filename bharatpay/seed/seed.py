"""
BharatPay Synthetic Data Generator & Seed Script
Generates fictional Indian users, accounts, UPI VPAs, and KYC records.
All values are clearly synthetic test data for CC6-IC07 hackathon demo.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User
from app.models.account import Account
from app.models.upi import UPIProfile
from app.models.kyc import KYCRecord
from app.models.merchant import Merchant
from app.core.security import get_password_hash

def seed_database():
    print("[BharatPay Seed] Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).filter(User.user_code == "u_101").first():
            print("[BharatPay Seed] Database already seeded with initial users.")
            return

        print("[BharatPay Seed] Seeding primary synthetic users...")
        test_users = [
            {
                "user_code": "u_101",
                "full_name": "Priya Sharma",
                "email": "priya.sharma@bharatpay.com",
                "phone": "9876501001",
                "password": "Password@123",
                "account_num": "501002341001",
                "masked_acc": "XXXXXXXX1001",
                "balance_paise": 4850000,  # ₹48,500.00
                "vpa": "priya.sharma@bharatpay",
                "pan": "ABCDE1234F",
                "masked_pan": "ABCDE****F",
                "aadhaar": "999988881001",
                "masked_aadhaar": "XXXXXXXX1001",
                "kyc_status": "VERIFIED"
            },
            {
                "user_code": "u_102",
                "full_name": "Rohit Verma",
                "email": "rohit.verma@bharatpay.com",
                "phone": "9876501002",
                "password": "Password@123",
                "account_num": "501002341002",
                "masked_acc": "XXXXXXXX1002",
                "balance_paise": 12500000,  # ₹1,25,000.00
                "vpa": "rohit.verma@bharatpay",
                "pan": "BCDEF2345G",
                "masked_pan": "BCDEF****G",
                "aadhaar": "999988881002",
                "masked_aadhaar": "XXXXXXXX1002",
                "kyc_status": "VERIFIED"
            },
            {
                "user_code": "u_103",
                "full_name": "Ananya Iyer",
                "email": "ananya.iyer@bharatpay.com",
                "phone": "9876501003",
                "password": "Password@123",
                "account_num": "501002341003",
                "masked_acc": "XXXXXXXX1003",
                "balance_paise": 1820000,  # ₹18,200.00
                "vpa": "ananya.iyer@bharatpay",
                "pan": "CDEFG3456H",
                "masked_pan": "CDEFG****H",
                "aadhaar": "999988881003",
                "masked_aadhaar": "XXXXXXXX1003",
                "kyc_status": "PENDING"
            }
        ]

        for udata in test_users:
            user = User(
                user_code=udata["user_code"],
                full_name=udata["full_name"],
                email=udata["email"],
                phone=udata["phone"],
                hashed_password=get_password_hash(udata["password"]),
                role="customer"
            )
            db.add(user)
            db.flush()

            account = Account(
                user_id=user.id,
                account_number=udata["account_num"],
                masked_account_number=udata["masked_acc"],
                ifsc_code="BPAY0001042",
                balance_paise=udata["balance_paise"],
                daily_limit_paise=10000000,  # ₹1,00,000.00
                currency="INR",
                status="ACTIVE"
            )
            db.add(account)
            db.flush()

            upi = UPIProfile(
                user_id=user.id,
                account_id=account.id,
                vpa=udata["vpa"],
                is_primary=True,
                status="ACTIVE"
            )
            db.add(upi)

            kyc = KYCRecord(
                user_id=user.id,
                pan_synthetic=udata["pan"],
                masked_pan=udata["masked_pan"],
                aadhaar_synthetic=udata["aadhaar"],
                masked_aadhaar=udata["masked_aadhaar"],
                kyc_status=udata["kyc_status"],
                verified_at=datetime.utcnow() if udata["kyc_status"] == "VERIFIED" else None
            )
            db.add(kyc)

        db.commit()
        print("[BharatPay Seed] Successfully seeded 3 synthetic test users and accounts.")

    except Exception as e:
        db.rollback()
        print(f"[BharatPay Seed] Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
