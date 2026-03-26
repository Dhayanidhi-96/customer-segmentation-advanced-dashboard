from __future__ import annotations

import uuid
from pathlib import Path

import joblib
import numpy as np
from sqlalchemy.orm import Session

from database.models import Customer, CustomerSegment, SegmentLabel
from ml.models.rfm_scoring import score_rfm
from ml.preprocessing import FEATURE_COLUMNS, FeaturePreprocessor


ARTIFACT_PATH = Path(__file__).resolve().parents[1] / "ml" / "artifacts" / "best_model.pkl"


RECOMMENDED_ACTIONS = {
    "VIP": "Send VIP discount offer",
    "Loyal": "Send upsell recommendation",
    "At-Risk": "Trigger win-back campaign",
    "New": "Start welcome series",
    "Churned": "Run aggressive retention offer",
    "Potential": "Send nurture campaign",
    "Outlier": "Review manually for custom strategy",
}


class SegmentationService:
    def __init__(self) -> None:
        self.preprocessor = FeaturePreprocessor()

    def _load_bundle(self) -> dict:
        if not ARTIFACT_PATH.exists():
            raise FileNotFoundError("Best model artifact not found. Retrain models first.")
        return joblib.load(ARTIFACT_PATH)

    def segment_customer(self, db: Session, customer_id: uuid.UUID, recalculate: bool = True) -> dict:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer is None:
            raise ValueError("Customer not found")

        if not recalculate:
            current = (
                db.query(CustomerSegment)
                .filter(CustomerSegment.customer_id == customer_id, CustomerSegment.is_current.is_(True))
                .first()
            )
            if current:
                return {
                    "customer_id": str(customer_id),
                    "segment_label": current.segment_label.value,
                    "rfm_scores": {
                        "recency": current.rfm_recency_score,
                        "frequency": current.rfm_frequency_score,
                        "monetary": current.rfm_monetary_score,
                    },
                    "cluster_id": current.cluster_id,
                    "confidence": current.confidence_score,
                    "model_used": current.model_used,
                    "recommended_action": RECOMMENDED_ACTIONS.get(current.segment_label.value, "Review customer behavior"),
                    "features": {},
                }

        bundle = self._load_bundle()
        model = bundle["model"]
        scaler = bundle["scaler"]

        features_df = self.preprocessor.build_feature_frame(db)
        selected = features_df[features_df["customer_id"] == str(customer_id)]
        if selected.empty:
            raise ValueError("No feature row found for customer")

        transformed = selected.copy()
        transformed["recency_days"] = transformed["recency_days"].apply(lambda x: np.log1p(x))
        transformed["monetary"] = transformed["monetary"].apply(lambda x: np.log1p(x))

        X = scaler.transform(transformed[FEATURE_COLUMNS].values)
        cluster_id = int(model.predict(X)[0])

        rfm_df = score_rfm(features_df)
        rfm_row = rfm_df[rfm_df["customer_id"] == str(customer_id)].iloc[0]

        segment_map = {
            0: "Potential",
            1: "Loyal",
            2: "VIP",
            3: "New",
            4: "At-Risk",
            5: "Churned",
            -1: "Outlier",
        }
        segment_label = segment_map.get(cluster_id, rfm_row["segment_label"])

        if hasattr(model, "predict_proba"):
            confidence = float(model.predict_proba(X).max())
        else:
            confidence = 0.87

        db.query(CustomerSegment).filter(
            CustomerSegment.customer_id == customer_id, CustomerSegment.is_current.is_(True)
        ).update({CustomerSegment.is_current: False})

        new_segment = CustomerSegment(
            customer_id=customer_id,
            segment_label=SegmentLabel(segment_label),
            rfm_recency_score=int(rfm_row["r_score"]),
            rfm_frequency_score=int(rfm_row["f_score"]),
            rfm_monetary_score=int(rfm_row["m_score"]),
            rfm_total_score=int(rfm_row["rfm_total_score"]),
            cluster_id=cluster_id,
            model_used=getattr(model, "model_name", "best_model"),
            confidence_score=confidence,
            is_current=True,
        )
        db.add(new_segment)
        db.commit()

        return {
            "customer_id": str(customer_id),
            "segment_label": segment_label,
            "rfm_scores": {
                "recency": int(rfm_row["r_score"]),
                "frequency": int(rfm_row["f_score"]),
                "monetary": int(rfm_row["m_score"]),
            },
            "cluster_id": cluster_id,
            "confidence": confidence,
            "model_used": getattr(model, "model_name", "best_model"),
            "recommended_action": RECOMMENDED_ACTIONS.get(segment_label, "Review customer behavior"),
            "features": selected.iloc[0].to_dict(),
        }
