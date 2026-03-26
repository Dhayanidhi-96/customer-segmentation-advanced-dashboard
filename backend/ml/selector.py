from __future__ import annotations

from pathlib import Path

import numpy as np
from sqlalchemy.orm import Session

from database.models import ModelRun


def _normalize(values: list[float | None], invert: bool = False) -> list[float]:
    cleaned = [0.0 if v is None else float(v) for v in values]
    arr = np.array(cleaned, dtype=float)
    if np.allclose(arr.max(), arr.min()):
        norm = np.ones_like(arr) * 0.5
    else:
        norm = (arr - arr.min()) / (arr.max() - arr.min())
    if invert:
        norm = 1.0 - norm
    return norm.tolist()


def select_best_model(results: list[dict], db: Session, artifact_dir: Path) -> dict:
    sil = _normalize([r.get("metrics", {}).get("silhouette_score") for r in results])
    dbi = _normalize([r.get("metrics", {}).get("davies_bouldin_index") for r in results], invert=True)
    ch = _normalize([r.get("metrics", {}).get("calinski_harabasz_score") for r in results])

    for idx, item in enumerate(results):
        composite = 0.5 * sil[idx] + 0.3 * dbi[idx] + 0.2 * ch[idx]
        item["composite_score"] = float(composite)

    best = max(results, key=lambda r: r["composite_score"])
    artifact_dir.mkdir(parents=True, exist_ok=True)

    for item in results:
        run = ModelRun(
            model_name=item["name"],
            hyperparameters=item.get("params", {}),
            n_clusters=item.get("n_clusters"),
            silhouette_score=item.get("metrics", {}).get("silhouette_score"),
            davies_bouldin_index=item.get("metrics", {}).get("davies_bouldin_index"),
            calinski_harabasz_score=item.get("metrics", {}).get("calinski_harabasz_score"),
            training_duration_seconds=item.get("duration", 0.0),
            n_customers_trained=item.get("n_samples", 0),
            is_best=item["name"] == best["name"],
            trained_at=item.get("trained_at"),
            artifact_path=item.get("artifact_path", ""),
        )
        db.add(run)

    db.commit()
    return best
