from __future__ import annotations

import argparse
import random
import sys
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from faker import Faker

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.connection import SessionLocal, engine
from database.models import (
    Base,
    Customer,
    CustomerSegment,
    EmailCampaign,
    GrokSession,
    ModelRun,
    Order,
    OrderStatus,
)
from ml.pipeline import run_full_training


fake = Faker()
random.seed(42)


def weighted_customer_profile() -> str:
    return random.choices(
        ["vip", "loyal", "atrisk", "new", "churned", "potential"],
        weights=[8, 20, 17, 20, 15, 20],
        k=1,
    )[0]


def profile_order_count(profile: str) -> int:
    if profile == "vip":
        return random.randint(20, 50)
    if profile == "loyal":
        return random.randint(8, 18)
    if profile == "atrisk":
        return random.randint(6, 12)
    if profile == "new":
        return random.randint(1, 4)
    if profile == "churned":
        return random.randint(1, 3)
    return random.randint(3, 8)


def profile_amount(profile: str) -> Decimal:
    if profile == "vip":
        return Decimal(str(round(random.uniform(120, 900), 2)))
    if profile == "loyal":
        return Decimal(str(round(random.uniform(50, 250), 2)))
    if profile == "atrisk":
        return Decimal(str(round(random.uniform(30, 180), 2)))
    if profile == "new":
        return Decimal(str(round(random.uniform(20, 120), 2)))
    if profile == "churned":
        return Decimal(str(round(random.uniform(15, 80), 2)))
    return Decimal(str(round(random.uniform(20, 170), 2)))


def profile_date(profile: str) -> datetime:
    now = datetime.utcnow()
    if profile == "churned":
        return now - timedelta(days=random.randint(150, 730))
    if profile == "atrisk":
        return now - timedelta(days=random.randint(60, 180))
    if profile == "new":
        return now - timedelta(days=random.randint(1, 30))
    if profile == "vip":
        return now - timedelta(days=random.randint(1, 45))
    return now - timedelta(days=random.randint(5, 120))


def parse_customer_count(value: str) -> int:
    cleaned = value.strip().lower().replace(",", "")
    if cleaned.endswith("lakh"):
        return int(float(cleaned[:-4]) * 100000)
    if cleaned.endswith("lac"):
        return int(float(cleaned[:-3]) * 100000)
    if cleaned.endswith("l"):
        return int(float(cleaned[:-1]) * 100000)
    if cleaned.endswith("k"):
        return int(float(cleaned[:-1]) * 1000)
    return int(float(cleaned))


def clear_existing_data(db) -> None:
    db.query(EmailCampaign).delete()
    db.query(CustomerSegment).delete()
    db.query(Order).delete()
    db.query(ModelRun).delete()
    db.query(GrokSession).delete()
    db.query(Customer).delete()
    db.commit()


def seed(
    customers_count: int = 500,
    min_orders: int = 1,
    max_orders: int = 50,
    batch_size: int = 5000,
    force_reset: bool = False,
    train_after_seed: bool = True,
) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_customers = db.query(Customer).count()
        if existing_customers > 0 and not force_reset:
            print("Seed skipped: customers already exist")
            return

        if existing_customers > 0 and force_reset:
            print("Force reset enabled: clearing existing data...")
            clear_existing_data(db)

        customer_rows: list[dict] = []
        customer_profile_pairs: list[tuple[uuid.UUID, str]] = []
        for index in range(customers_count):
            profile = weighted_customer_profile()
            customer_id = uuid.uuid4()
            customer_rows.append(
                {
                    "id": customer_id,
                    "email": f"customer_{index}_{customer_id.hex[:8]}@example.com",
                    "name": fake.name(),
                    "phone": fake.phone_number(),
                    "country": fake.country(),
                    "city": fake.city(),
                    "age": random.randint(18, 70),
                    "gender": random.choice(["male", "female", "other"]),
                    "is_active": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            )
            customer_profile_pairs.append((customer_id, profile))

            if len(customer_rows) >= batch_size:
                db.bulk_insert_mappings(Customer, customer_rows)
                db.commit()
                print(f"Inserted customers: {len(customer_profile_pairs)}/{customers_count}")
                customer_rows = []

        if customer_rows:
            db.bulk_insert_mappings(Customer, customer_rows)
            db.commit()

        total_orders = 0
        order_rows: list[dict] = []
        for customer_id, profile in customer_profile_pairs:
            base_orders = profile_order_count(profile)
            order_count = max(min_orders, min(max_orders, base_orders))
            total_orders += order_count

            for _ in range(order_count):
                status = random.choices(
                    [OrderStatus.completed, OrderStatus.cancelled, OrderStatus.refunded],
                    weights=[88, 8, 4],
                    k=1,
                )[0]
                order_rows.append(
                    {
                        "id": uuid.uuid4(),
                        "customer_id": customer_id,
                        "order_number": f"ORD-{uuid.uuid4().hex[:10].upper()}",
                        "amount": profile_amount(profile),
                        "items_count": random.randint(1, 8),
                        "status": status,
                        "created_at": profile_date(profile),
                        "updated_at": datetime.utcnow(),
                    }
                )

                if len(order_rows) >= batch_size * 4:
                    db.bulk_insert_mappings(Order, order_rows)
                    db.commit()
                    order_rows = []

        if order_rows:
            db.bulk_insert_mappings(Order, order_rows)
            db.commit()

        print(f"Seed complete: {customers_count} customers, {total_orders} orders")

        if not train_after_seed:
            print("Training skipped (--no-train used)")
            return

        result = run_full_training(db)
        print("Training result:", result)
    finally:
        db.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed customer segmentation database")
    parser.add_argument("--customers", type=str, default="500", help="Number of customers (e.g. 500, 100k, 1l, 2.5lakh)")
    parser.add_argument("--min-orders", type=int, default=1, help="Minimum orders per customer")
    parser.add_argument("--max-orders", type=int, default=50, help="Maximum orders per customer")
    parser.add_argument("--batch-size", type=int, default=5000, help="Batch insert size")
    parser.add_argument("--force", action="store_true", help="Delete existing data before seeding")
    parser.add_argument("--no-train", action="store_true", help="Skip model training after seed")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    seed(
        customers_count=parse_customer_count(args.customers),
        min_orders=args.min_orders,
        max_orders=args.max_orders,
        batch_size=args.batch_size,
        force_reset=args.force,
        train_after_seed=not args.no_train,
    )
