from __future__ import annotations

import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans

from ml.models.base_model import BaseClusteringModel


class KMeansSegmentationModel(BaseClusteringModel):
    def __init__(self) -> None:
        super().__init__("kmeans")
        self.best_k = 2

    def fit(self, X: np.ndarray) -> "KMeansSegmentationModel":
        best_score = -1.0
        best_model = None
        large_dataset = len(X) > 100000
        cluster_range = range(2, 7) if large_dataset else range(2, 11)

        for k in cluster_range:
            if large_dataset:
                model = MiniBatchKMeans(n_clusters=k, n_init=5, random_state=42, batch_size=4096)
            else:
                model = KMeans(n_clusters=k, n_init=10, random_state=42)
            labels = model.fit_predict(X)
            metrics = self.evaluate(X, labels)
            score = metrics.get("silhouette_score") or -1.0
            if score > best_score:
                best_score = score
                best_model = model
                self.best_k = k

        self.model = best_model if best_model is not None else KMeans(n_clusters=2, n_init=10, random_state=42).fit(X)
        self.labels_ = self.model.labels_
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not fitted")
        return self.model.predict(X)

    def get_params(self) -> dict:
        return {"n_clusters": self.best_k, "algorithm": "kmeans"}
