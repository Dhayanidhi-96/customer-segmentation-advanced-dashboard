from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from database.models import Customer, Order, OrderStatus


FEATURE_COLUMNS = [
    "recency_days",
    "frequency",
    "monetary",
    "avg_order_value",
    "order_std_dev",
    "days_between_orders",
    "cancellation_rate",
]


@dataclass
class PreprocessingResult:
    features_df: pd.DataFrame
    feature_matrix: np.ndarray
    scaled_matrix: np.ndarray
    pca_matrix: np.ndarray
    scaler: StandardScaler
    pca: PCA


class FeaturePreprocessor:
    def __init__(self) -> None:
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2, random_state=42)

    def build_feature_frame(self, db: Session, reference_time: datetime | None = None) -> pd.DataFrame:
        now = reference_time or datetime.utcnow()

        if db.query(Customer.id).first() is None:
            return pd.DataFrame(columns=["customer_id", *FEATURE_COLUMNS])

        agg_subq = (
            db.query(
                Order.customer_id.label("customer_id"),
                func.count(Order.id).label("frequency"),
                func.coalesce(func.sum(Order.amount), 0).label("monetary"),
                func.coalesce(func.avg(Order.amount), 0).label("avg_order_value"),
                func.coalesce(func.stddev_pop(Order.amount), 0).label("order_std_dev"),
                func.max(Order.created_at).label("last_order_date"),
                func.coalesce(
                    func.sum(case((Order.status == OrderStatus.cancelled, 1), else_=0)),
                    0,
                ).label("cancelled_count"),
            )
            .group_by(Order.customer_id)
            .subquery()
        )

        gap_source_subq = db.query(
            Order.customer_id.label("customer_id"),
            (
                func.extract(
                    "epoch",
                    Order.created_at
                    - func.lag(Order.created_at).over(
                        partition_by=Order.customer_id,
                        order_by=Order.created_at,
                    ),
                )
                / 86400.0
            ).label("gap_days"),
        ).subquery()

        gap_subq = (
            db.query(
                gap_source_subq.c.customer_id.label("customer_id"),
                func.coalesce(func.avg(gap_source_subq.c.gap_days), 0).label("days_between_orders"),
            )
            .filter(gap_source_subq.c.gap_days.is_not(None))
            .group_by(gap_source_subq.c.customer_id)
            .subquery()
        )

        feature_rows = (
            db.query(
                Customer.id.label("customer_id"),
                agg_subq.c.frequency,
                agg_subq.c.monetary,
                agg_subq.c.avg_order_value,
                agg_subq.c.order_std_dev,
                agg_subq.c.last_order_date,
                agg_subq.c.cancelled_count,
                gap_subq.c.days_between_orders,
            )
            .outerjoin(agg_subq, Customer.id == agg_subq.c.customer_id)
            .outerjoin(gap_subq, Customer.id == gap_subq.c.customer_id)
            .all()
        )

        rows: list[dict] = []
        for row in feature_rows:
            cid = str(row.customer_id)
            frequency = int(row.frequency or 0)
            if frequency == 0:
                recency_days = 365.0
                monetary = 0.0
                avg_order_value = 0.0
                order_std_dev = 0.0
                days_between_orders = 365.0
                cancellation_rate = 0.0
            else:
                last_order_date = row.last_order_date
                recency_days = float(max((now - last_order_date).days, 0))
                monetary = float(row.monetary or 0.0)
                avg_order_value = float(row.avg_order_value or (monetary / max(frequency, 1)))
                order_std_dev = float(row.order_std_dev or 0.0)
                days_between_orders = float(row.days_between_orders or recency_days)
                cancelled = int(row.cancelled_count or 0)
                cancellation_rate = float(cancelled / max(frequency, 1))

            rows.append(
                {
                    "customer_id": cid,
                    "recency_days": recency_days,
                    "frequency": frequency,
                    "monetary": monetary,
                    "avg_order_value": avg_order_value,
                    "order_std_dev": order_std_dev,
                    "days_between_orders": days_between_orders,
                    "cancellation_rate": cancellation_rate,
                }
            )

        features_df = pd.DataFrame(rows)
        return features_df

    def transform(self, features_df: pd.DataFrame) -> PreprocessingResult:
        if features_df.empty:
            empty = np.empty((0, len(FEATURE_COLUMNS)))
            return PreprocessingResult(features_df, empty, empty, np.empty((0, 2)), self.scaler, self.pca)

        transformed = features_df.copy()
        transformed["recency_days"] = np.log1p(transformed["recency_days"])
        transformed["monetary"] = np.log1p(transformed["monetary"])

        feature_matrix = transformed[FEATURE_COLUMNS].values.astype(float)
        scaled_matrix = self.scaler.fit_transform(feature_matrix)
        pca_matrix = self.pca.fit_transform(scaled_matrix)

        return PreprocessingResult(transformed, feature_matrix, scaled_matrix, pca_matrix, self.scaler, self.pca)
