from __future__ import annotations

from database.connection import SessionLocal
from database.models import Customer
from services.segmentation_service import SegmentationService
from tasks.celery_app import celery_app


@celery_app.task(name="tasks.segment_tasks.nightly_resegmentation")
def nightly_resegmentation() -> dict:
    db = SessionLocal()
    service = SegmentationService()
    updated = 0
    skipped = 0
    try:
        customers = db.query(Customer).all()
        for customer in customers:
            try:
                service.segment_customer(db, customer.id, recalculate=True)
                updated += 1
            except Exception:  # noqa: BLE001
                skipped += 1
        return {"status": "completed", "updated": updated, "skipped": skipped}
    finally:
        db.close()
