from __future__ import annotations

import numpy as np
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score


def evaluate_clustering(X: np.ndarray, labels: np.ndarray) -> dict[str, float | None]:
    unique_labels = np.unique(labels)
    if len(unique_labels) < 2:
        return {
            "silhouette_score": None,
            "davies_bouldin_index": None,
            "calinski_harabasz_score": None,
        }

    sample_size = min(len(X), 5000)

    return {
        "silhouette_score": float(silhouette_score(X, labels, sample_size=sample_size, random_state=42)),
        "davies_bouldin_index": float(davies_bouldin_score(X, labels)),
        "calinski_harabasz_score": float(calinski_harabasz_score(X, labels)),
    }
