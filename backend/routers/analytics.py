from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Customer, CustomerSegment, EmailCampaign, ModelRun, Order
from ml.preprocessing import FeaturePreprocessor


router = APIRouter()
preprocessor = FeaturePreprocessor()


class DashboardResponse(BaseModel):
    total_customers: int
    revenue_this_month: float
    avg_rfm_score: float
    email_open_rate: float


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(db: Session = Depends(get_db)) -> DashboardResponse:
    now = datetime.utcnow()
    total_customers = db.query(func.count(Customer.id)).scalar() or 0
    revenue_this_month = (
        db.query(func.coalesce(func.sum(Order.amount), 0))
        .filter(func.date_trunc("month", Order.created_at) == func.date_trunc("month", now))
        .scalar()
        or 0
    )
    avg_rfm = db.query(func.avg(CustomerSegment.rfm_total_score)).filter(CustomerSegment.is_current.is_(True)).scalar() or 0

    total_emails = db.query(func.count(EmailCampaign.id)).scalar() or 0
    opened = db.query(func.count(EmailCampaign.id)).filter(EmailCampaign.opened_at.is_not(None)).scalar() or 0
    open_rate = float(opened / total_emails * 100) if total_emails else 0.0

    return DashboardResponse(
        total_customers=int(total_customers),
        revenue_this_month=float(revenue_this_month),
        avg_rfm_score=float(avg_rfm),
        email_open_rate=open_rate,
    )


@router.get("/rfm-heatmap")
def rfm_heatmap(db: Session = Depends(get_db)) -> dict:
    rows = (
        db.query(
            CustomerSegment.rfm_recency_score,
            CustomerSegment.rfm_frequency_score,
            func.count(CustomerSegment.id),
        )
        .filter(CustomerSegment.is_current.is_(True))
        .group_by(CustomerSegment.rfm_recency_score, CustomerSegment.rfm_frequency_score)
        .all()
    )
    return {
        "data": [
            {"recency": r, "frequency": f, "count": c}
            for r, f, c in rows
        ]
    }


@router.get("/cluster-scatter")
def cluster_scatter(limit: int = Query(default=3000, ge=200, le=10000), db: Session = Depends(get_db)) -> dict:
    features = preprocessor.build_feature_frame(db)
    if features.empty:
        return {"data": []}

    if len(features) > limit:
        features = features.sample(n=limit, random_state=42)

    transformed = preprocessor.transform(features)

    segment_map = {
        str(customer_id): segment_label.value
        for customer_id, segment_label in db.query(CustomerSegment.customer_id, CustomerSegment.segment_label)
        .filter(CustomerSegment.is_current.is_(True))
        .all()
    }

    points = []
    for i, row in transformed.features_df.iterrows():
        points.append(
            {
                "customer_id": row["customer_id"],
                "x": float(transformed.pca_matrix[i][0]) if len(transformed.pca_matrix) > i else 0.0,
                "y": float(transformed.pca_matrix[i][1]) if len(transformed.pca_matrix) > i else 0.0,
                "segment": segment_map.get(row["customer_id"], "Unknown"),
            }
        )
    return {"data": points}


@router.get("/revenue-by-segment")
def revenue_by_segment(db: Session = Depends(get_db)) -> dict:
    rows = (
        db.query(
            CustomerSegment.segment_label,
            func.coalesce(func.sum(Order.amount), 0).label("revenue"),
        )
        .join(Order, Order.customer_id == CustomerSegment.customer_id)
        .filter(CustomerSegment.is_current.is_(True))
        .group_by(CustomerSegment.segment_label)
        .all()
    )

    return {
        "data": sorted(
            [{"segment": label.value, "revenue": float(revenue or 0)} for label, revenue in rows],
            key=lambda x: x["revenue"],
            reverse=True,
        )
    }


@router.get("/retention-cohort")
def retention_cohort(db: Session = Depends(get_db)) -> dict:
    orders = db.query(Order.customer_id, Order.created_at).all()
    first_purchase: dict = {}
    activity: dict = defaultdict(set)

    for customer_id, created_at in orders:
        cohort = created_at.strftime("%Y-%m")
        if customer_id not in first_purchase or created_at < first_purchase[customer_id]:
            first_purchase[customer_id] = created_at
        activity[customer_id].add(cohort)

    matrix: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for customer_id, first_date in first_purchase.items():
        cohort_month = first_date.strftime("%Y-%m")
        for active_month in activity[customer_id]:
            matrix[cohort_month][active_month] += 1

    return {"data": [{"cohort": c, "values": dict(v)} for c, v in sorted(matrix.items())]}


@router.get("/model-comparison")
def model_comparison(db: Session = Depends(get_db)) -> dict:
    runs = db.query(ModelRun).order_by(ModelRun.trained_at.desc()).limit(20).all()
    return {
        "data": [
            {
                "model_name": run.model_name,
                "silhouette_score": run.silhouette_score,
                "davies_bouldin_index": run.davies_bouldin_index,
                "calinski_harabasz_score": run.calinski_harabasz_score,
                "is_best": run.is_best,
                "trained_at": run.trained_at,
            }
            for run in runs
        ]
    }
