from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy import case, func
from sqlalchemy.orm import Session, joinedload

from database.connection import get_db
from database.models import Customer, CustomerSegment, Order, OrderStatus
from services.segmentation_service import SegmentationService


router = APIRouter()
service = SegmentationService()


class SegmentRequest(BaseModel):
    customer_id: uuid.UUID
    recalculate: bool = True


class RfmScores(BaseModel):
    recency: int
    frequency: int
    monetary: int


class SegmentResponse(BaseModel):
    customer_id: str
    segment_label: str
    rfm_scores: RfmScores
    cluster_id: int | None
    confidence: float
    model_used: str
    recommended_action: str
    features: dict

    model_config = ConfigDict(protected_namespaces=())


class CustomerRow(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    segment_label: str | None
    rfm_total_score: int | None
    total_spend: float
    last_order: datetime | None

    model_config = ConfigDict(from_attributes=True)


class OrderRow(BaseModel):
    id: uuid.UUID
    order_number: str
    amount: Decimal
    items_count: int
    status: str
    created_at: datetime


class SegmentHistoryRow(BaseModel):
    segment_label: str
    rfm_total_score: int
    model_used: str
    assigned_at: datetime

    model_config = ConfigDict(protected_namespaces=())


class CustomerDetail(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    phone: str | None
    country: str | None
    city: str | None
    age: int | None
    gender: str | None
    is_active: bool
    orders: list[OrderRow]
    segment_history: list[SegmentHistoryRow]


@router.post("/segment", response_model=SegmentResponse)
def segment_customer(payload: SegmentRequest, db: Session = Depends(get_db)) -> SegmentResponse:
    try:
        result = service.segment_customer(db, payload.customer_id, payload.recalculate)
        return SegmentResponse(**result)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("", response_model=list[CustomerRow])
def list_customers(
    limit: int = Query(default=500, ge=1, le=5000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[CustomerRow]:
    order_agg_subq = (
        db.query(
            Order.customer_id.label("customer_id"),
            func.coalesce(
                func.sum(case((Order.status == OrderStatus.completed, Order.amount), else_=0)),
                0,
            ).label("total_spend"),
            func.max(Order.created_at).label("last_order"),
        )
        .group_by(Order.customer_id)
        .subquery()
    )

    segment_subq = (
        db.query(
            CustomerSegment.customer_id.label("customer_id"),
            CustomerSegment.segment_label.label("segment_label"),
            CustomerSegment.rfm_total_score.label("rfm_total_score"),
        )
        .filter(CustomerSegment.is_current.is_(True))
        .subquery()
    )

    customers = (
        db.query(
            Customer.id,
            Customer.name,
            Customer.email,
            segment_subq.c.segment_label,
            segment_subq.c.rfm_total_score,
            order_agg_subq.c.total_spend,
            order_agg_subq.c.last_order,
        )
        .outerjoin(segment_subq, segment_subq.c.customer_id == Customer.id)
        .outerjoin(order_agg_subq, order_agg_subq.c.customer_id == Customer.id)
        .order_by(Customer.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    rows: list[CustomerRow] = []
    for c in customers:
        rows.append(
            CustomerRow(
                id=c.id,
                name=c.name,
                email=c.email,
                segment_label=c.segment_label.value if c.segment_label else None,
                rfm_total_score=c.rfm_total_score,
                total_spend=float(c.total_spend or 0),
                last_order=c.last_order,
            )
        )
    return rows


@router.get("/{customer_id}", response_model=CustomerDetail)
def customer_detail(customer_id: uuid.UUID, db: Session = Depends(get_db)) -> CustomerDetail:
    customer = (
        db.query(Customer)
        .options(joinedload(Customer.orders), joinedload(Customer.segments))
        .filter(Customer.id == customer_id)
        .first()
    )
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return CustomerDetail(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        country=customer.country,
        city=customer.city,
        age=customer.age,
        gender=customer.gender,
        is_active=customer.is_active,
        orders=[
            OrderRow(
                id=o.id,
                order_number=o.order_number,
                amount=o.amount,
                items_count=o.items_count,
                status=o.status.value,
                created_at=o.created_at,
            )
            for o in sorted(customer.orders, key=lambda x: x.created_at, reverse=True)
        ],
        segment_history=[
            SegmentHistoryRow(
                segment_label=s.segment_label.value,
                rfm_total_score=s.rfm_total_score,
                model_used=s.model_used,
                assigned_at=s.assigned_at,
            )
            for s in sorted(customer.segments, key=lambda x: x.assigned_at, reverse=True)
        ],
    )
