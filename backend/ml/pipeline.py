from __future__ import annotations

import time
import uuid
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
from sqlalchemy.orm import Session

from database.models import CustomerSegment, SegmentLabel
from ml.models.dbscan_model import DBSCANSegmentationModel
from ml.models.gaussian_mixture_model import GaussianMixtureSegmentationModel
from ml.models.hierarchical_model import HierarchicalSegmentationModel
from ml.models.kmeans_model import KMeansSegmentationModel
from ml.models.rfm_scoring import score_rfm
from ml.models.spectral_model import SpectralSegmentationModel
from ml.preprocessing import FeaturePreprocessor
from ml.selector import select_best_model


ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"


def map_cluster_to_segment(cluster_summary: pd.DataFrame) -> dict[int, str]:
    mapping: dict[int, str] = {}
    ranked = cluster_summary.copy()
    ranked["score"] = ranked["recency_days"] + ranked["frequency"] + ranked["monetary"]

    order = ranked.sort_values("score", ascending=False)["cluster_id"].tolist()
    labels = ["VIP", "Loyal", "Potential", "New", "At-Risk", "Churned"]
    for idx, cluster_id in enumerate(order):
        mapping[int(cluster_id)] = labels[min(idx, len(labels) - 1)]
    return mapping


def run_full_training(db: Session) -> dict:
    preprocessor = FeaturePreprocessor()
    features_df = preprocessor.build_feature_frame(db)
    transformed = preprocessor.transform(features_df)
    if transformed.scaled_matrix.shape[0] < 3:
        return {"status": "skipped", "reason": "Not enough customers for clustering"}

    n_samples = int(transformed.scaled_matrix.shape[0])
    large_data_mode = n_samples >= 100000

    if large_data_mode:
        model_instances = [
            KMeansSegmentationModel(),
            GaussianMixtureSegmentationModel(),
        ]
    else:
        model_instances = [
            KMeansSegmentationModel(),
            DBSCANSegmentationModel(),
            HierarchicalSegmentationModel(),
            GaussianMixtureSegmentationModel(),
            SpectralSegmentationModel(),
        ]

    results: list[dict] = []

    for model in model_instances:
        start = time.perf_counter()
        model.fit(transformed.scaled_matrix)
        labels = model.predict(transformed.scaled_matrix)
        metrics = model.evaluate(transformed.scaled_matrix, labels)
        duration = time.perf_counter() - start

        artifact_path = ARTIFACTS_DIR / f"{model.model_name}.pkl"
        model.save(artifact_path)

        n_clusters = len(set(labels.tolist())) if hasattr(labels, "tolist") else len(set(labels))

        results.append(
            {
                "name": model.model_name,
                "instance": model,
                "params": model.get_params(),
                "metrics": metrics,
                "duration": duration,
                "n_samples": n_samples,
                "n_clusters": n_clusters,
                "trained_at": datetime.utcnow(),
                "artifact_path": str(artifact_path),
                "labels": labels,
            }
        )

    best = select_best_model(results, db, ARTIFACTS_DIR)
    best_model = best["instance"]

    joblib.dump(
        {
            "model": best_model,
            "scaler": transformed.scaler,
            "pca": transformed.pca,
            "feature_columns": list(transformed.features_df.columns),
        },
        ARTIFACTS_DIR / "best_model.pkl",
    )

    labels = best["labels"]
    customer_df = transformed.features_df.copy()
    customer_df["cluster_id"] = labels

    cluster_summary = (
        customer_df.groupby("cluster_id")[["recency_days", "frequency", "monetary"]].mean().reset_index()
    )
    cluster_to_segment = map_cluster_to_segment(cluster_summary)

    rfm_df = score_rfm(transformed.features_df)
    rfm_by_customer = {
        row["customer_id"]: row
        for _, row in rfm_df.iterrows()
    }

    db.query(CustomerSegment).update({CustomerSegment.is_current: False})

    segment_rows: list[dict] = []
    segment_batch_size = 10000

    for _, row in customer_df.iterrows():
        cid = row["customer_id"]
        rfm_row = rfm_by_customer.get(cid)
        cluster_id = int(row["cluster_id"]) if row["cluster_id"] != -1 else -1
        segment_name = "Outlier" if cluster_id == -1 else cluster_to_segment.get(cluster_id, "Potential")

        segment_rows.append(
            {
                "id": uuid.uuid4(),
                "customer_id": uuid.UUID(str(cid)),
                "segment_label": SegmentLabel(segment_name),
                "rfm_recency_score": int(rfm_row["r_score"]) if rfm_row is not None else 3,
                "rfm_frequency_score": int(rfm_row["f_score"]) if rfm_row is not None else 3,
                "rfm_monetary_score": int(rfm_row["m_score"]) if rfm_row is not None else 3,
                "rfm_total_score": int(rfm_row["rfm_total_score"]) if rfm_row is not None else 9,
                "cluster_id": cluster_id,
                "model_used": best["name"],
                "confidence_score": float(best["composite_score"]),
                "assigned_at": datetime.utcnow(),
                "is_current": True,
            }
        )

        if len(segment_rows) >= segment_batch_size:
            db.bulk_insert_mappings(CustomerSegment, segment_rows)
            db.commit()
            segment_rows = []

    if segment_rows:
        db.bulk_insert_mappings(CustomerSegment, segment_rows)

    db.commit()
    return {
        "status": "ok",
        "large_data_mode": large_data_mode,
        "best_model": best["name"],
        "composite_score": best["composite_score"],
        "models": [{"name": r["name"], "metrics": r["metrics"], "score": r["composite_score"]} for r in results],
    }
