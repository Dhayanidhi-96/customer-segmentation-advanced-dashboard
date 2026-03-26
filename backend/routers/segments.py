from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import CustomerSegment, Order


router = APIRouter()


class SegmentSummary(BaseModel):
    segment_label: str
    customer_count: int
    revenue: float


@router.get("/summary", response_model=list[SegmentSummary])
def segments_summary(db: Session = Depends(get_db)) -> list[SegmentSummary]:
    rows = (
        db.query(
            CustomerSegment.segment_label,
            func.count(CustomerSegment.id).label("customer_count"),
            func.coalesce(func.sum(Order.amount), 0).label("revenue"),
        )
        .outerjoin(Order, Order.customer_id == CustomerSegment.customer_id)
        .filter(CustomerSegment.is_current.is_(True))
        .group_by(CustomerSegment.segment_label)
        .all()
    )

    return [
        SegmentSummary(
            segment_label=label.value,
            customer_count=int(customer_count),
            revenue=float(revenue or 0),
        )
        for label, customer_count, revenue in rows
    ]
