from __future__ import annotations

import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn.neighbors import KNeighborsClassifier

from ml.models.base_model import BaseClusteringModel


class SpectralSegmentationModel(BaseClusteringModel):
    def __init__(self) -> None:
        super().__init__("spectral")
        self.best_n_clusters = 2
        self.knn: KNeighborsClassifier | None = None

    def fit(self, X: np.ndarray) -> "SpectralSegmentationModel":
        best_score = -1.0
        best_labels = None

        for n_clusters in range(2, 9):
            model = SpectralClustering(n_clusters=n_clusters, affinity="rbf", random_state=42)
            labels = model.fit_predict(X)
            metrics = self.evaluate(X, labels)
            score = metrics.get("silhouette_score") or -1.0
            if score > best_score:
                best_score = score
                best_labels = labels
                self.best_n_clusters = n_clusters

        self.model = SpectralClustering(n_clusters=self.best_n_clusters, affinity="rbf", random_state=42)
        self.labels_ = best_labels if best_labels is not None else self.model.fit_predict(X)
        self.knn = KNeighborsClassifier(n_neighbors=min(5, len(X)))
        self.knn.fit(X, self.labels_)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.knn is None:
            raise ValueError("Model not fitted")
        return self.knn.predict(X)

    def get_params(self) -> dict:
        return {"n_clusters": self.best_n_clusters, "kernel": "rbf", "algorithm": "spectral"}
