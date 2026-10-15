"""
BharatPay Synthetic Data Generator & Seed Script
Generates fictional Indian users, accounts, UPI VPAs, KYC records, 200+ merchants, and transaction history.
All values are clearly synthetic test data for CC6-IC07 hackathon demo.
"""

import sys
import os
import random
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User
from app.models.account import Account
from app.models.upi import UPIProfile
from app.models.kyc import KYCRecord
from app.models.merchant import Merchant
from app.models.transaction import Transaction
from app.core.security import get_password_hash

def seed_database():
    print("[BharatPay Seed] Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).filter(User.user_code == "u_101").first() and db.query(Merchant).count() >= 200:
            print("[BharatPay Seed] Database already seeded.")
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

        created_accounts = []
        for udata in test_users:
            existing = db.query(User).filter(User.user_code == udata["user_code"]).first()
            if not existing:
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
                created_accounts.append((user, account))

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
                    verified_at=datetime.now(timezone.utc) if udata["kyc_status"] == "VERIFIED" else None
                )
                db.add(kyc)
            else:
                account = db.query(Account).filter(Account.user_id == existing.id).first()
                created_accounts.append((existing, account))

        db.commit()

        # Seed 220+ Merchants across realistic Indian categories
        if db.query(Merchant).count() < 200:
            print("[BharatPay Seed] Seeding 220+ verified merchants...")
            categories = [
                ("Food & Dining", ["Swiggy", "Zomato", "Chai Point", "Cafe Coffee Day", "Haldirams", "Bikanervala", "Subway", "Dominos", "Burger King", "McDonalds", "KFC", "Faasos", "Behrouz Biryani", "Barbeque Nation", "Starbucks", "Blue Tokai"]),
                ("Groceries", ["Blinkit", "Zepto", "Instamart", "BigBasket", "Nature Basket", "DMart Ready", "More Retail", "Spencer Supermarket", "Reliance Fresh", "Star Bazaar", "Kisan Mandi"]),
                ("Utilities & Bills", ["Tata Power", "BSES Yamuna", "Bescom Electricity", "Adani Gas", "Indane LPG", "Bharat Gas", "Mahanagar Gas", "Airtel Broadband", "Jio Fiber", "Tata Play DTH"]),
                ("Travel & Transit", ["Uber India", "Ola Cabs", "Rapido", "MakeMyTrip", "IRCTC Rail", "Cleartrip", "Goibibo", "RedBus", "Delhi Metro DMRC", "Namma Metro", "Air India", "IndiGo"]),
                ("Shopping & Apparel", ["Flipkart", "Amazon Pay", "Myntra", "Ajio", "Nykaa", "Tata Cliq", "Croma Retail", "Reliance Digital", "Zudio", "Max Fashion", "Pantaloons", "FabIndia"]),
                ("Healthcare & Pharmacy", ["Apollo Pharmacy", "1mg Healthcare", "PharmEasy", "Netmeds", "MedPlus", "Max Healthcare", "Dr Lal PathLabs", "Metropolis Health"]),
                ("Entertainment & Gaming", ["BookMyShow", "PVR Cinemas", "INOX", "Hotstar Premium", "SonyLIV", "Zee5", "Spotify India", "Gaana Music", "Dream11", "Nazara Games"]),
                ("Education & Services", ["Urban Company", "Dunzo", "Unacademy", "PhysicsWallah", "Coursera India", "Cult Fit", "Anytime Fitness", "Lenskart", "Pepperfry", "Wakefit"])
            ]

            merchant_count = 0
            for cat_name, brand_list in categories:
                for brand in brand_list:
                    slug = brand.lower().replace(" ", "").replace("&", "")
                    # Add main brand
                    merchant_count += 1
                    db.add(Merchant(
                        merchant_code=f"m_{slug}_{merchant_count:03d}",
                        business_name=f"{brand} Official",
                        vpa=f"{slug}@bharatpay",
                        category=cat_name,
                        verified=True,
                        rating=round(random.uniform(4.2, 4.9), 1)
                    ))
                    # Add regional/franchise branches to reach 220+ total
                    for loc in ["Bangalore", "Mumbai", "Delhi NCR"]:
                        merchant_count += 1
                        loc_slug = loc.lower().replace(" ", "")
                        db.add(Merchant(
                            merchant_code=f"m_{slug}_{loc_slug}_{merchant_count:03d}",
                            business_name=f"{brand} - {loc}",
                            vpa=f"{slug}.{loc_slug}@bharatpay",
                            category=cat_name,
                            verified=True,
                            rating=round(random.uniform(4.0, 4.8), 1)
                        ))

            db.commit()
            print(f"[BharatPay Seed] Successfully seeded {db.query(Merchant).count()} merchants.")

        # Seed realistic initial transaction history for Priya (u_101)
        if db.query(Transaction).count() < 10:
            print("[BharatPay Seed] Seeding initial transactions for user accounts...")
            priya_acc = db.query(Account).filter(Account.id == 1).first()
            rohit_acc = db.query(Account).filter(Account.id == 2).first()

            now = datetime.now(timezone.utc)
            history = [
                ("Blinkit Quick Delivery", "blinkit@bharatpay", 48500, now - timedelta(days=1)),
                ("Swiggy Gourmet Order", "swiggy@bharatpay", 74000, now - timedelta(days=2)),
                ("Uber Premier Ride", "uberindia@bharatpay", 52000, now - timedelta(days=3)),
                ("Tata Power Bill", "tatapower@bharatpay", 285000, now - timedelta(days=5)),
                ("BookMyShow Movie Tickets", "bookmyshow@bharatpay", 112000, now - timedelta(days=7)),
                ("Blue Tokai Coffee", "bluetokai@bharatpay", 38000, now - timedelta(days=9)),
                ("Zepto Daily Fresh", "zepto@bharatpay", 31000, now - timedelta(days=11)),
                ("Cult Fit Monthly", "cultfit@bharatpay", 199900, now - timedelta(days=15)),
                ("Apollo Pharmacy", "apollopharmacy@bharatpay", 65000, now - timedelta(days=18)),
                ("Zomato Dinner", "zomato@bharatpay", 89000, now - timedelta(days=21)),
                ("Dinner Split with Rohit", "rohit.verma@bharatpay", 150000, now - timedelta(days=24)),
                ("Chai Point Snacks", "chaipoint@bharatpay", 24000, now - timedelta(days=27)),
            ]

            for i, (note, to_vpa, amt, txn_time) in enumerate(history, 1):
                txn = Transaction(
                    txn_reference=f"TXN202610{i:04d}SEED",
                    from_account_id=priya_acc.id,
                    to_account_id=rohit_acc.id if "rohit" in to_vpa else None,
                    from_vpa="priya.sharma@bharatpay",
                    to_vpa=to_vpa,
                    amount_paise=amt,
                    note=note,
                    status="SUCCESS",
                    created_at=txn_time
                )
                db.add(txn)

            db.commit()
            print("[BharatPay Seed] Successfully seeded transaction history.")

        print("[BharatPay Seed] Database setup complete!")

    except Exception as e:
        db.rollback()
        print(f"[BharatPay Seed] Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
