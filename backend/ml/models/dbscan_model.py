from __future__ import annotations

import numpy as np
from sklearn.cluster import DBSCAN

from ml.models.base_model import BaseClusteringModel


class DBSCANSegmentationModel(BaseClusteringModel):
    def __init__(self) -> None:
        super().__init__("dbscan")
        self.best_eps = 0.5
        self.best_min_samples = 5

    def fit(self, X: np.ndarray) -> "DBSCANSegmentationModel":
        best_score = -1.0
        best_model = None
        best_labels = None

        for eps in np.arange(0.1, 2.1, 0.2):
            for min_samples in range(2, 11):
                model = DBSCAN(eps=float(round(eps, 2)), min_samples=min_samples)
                labels = model.fit_predict(X)
                metrics = self.evaluate(X, labels)
                score = metrics.get("silhouette_score") or -1.0
                if score > best_score:
                    best_score = score
                    best_model = model
                    best_labels = labels
                    self.best_eps = float(round(eps, 2))
                    self.best_min_samples = min_samples

        self.model = best_model if best_model is not None else DBSCAN(eps=0.5, min_samples=5).fit(X)
        self.labels_ = best_labels if best_labels is not None else self.model.fit_predict(X)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.labels_ is None:
            raise ValueError("Model not fitted")
        # DBSCAN does not support true out-of-sample prediction.
        return self.labels_

    def get_params(self) -> dict:
        return {"eps": self.best_eps, "min_samples": self.best_min_samples, "algorithm": "dbscan"}
