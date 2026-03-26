from __future__ import annotations

import numpy as np
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import AgglomerativeClustering

from ml.models.base_model import BaseClusteringModel


class HierarchicalSegmentationModel(BaseClusteringModel):
    def __init__(self) -> None:
        super().__init__("hierarchical")
        self.best_linkage = "ward"
        self.best_n_clusters = 2
        self.dendrogram_data: list[list[float]] = []

    def fit(self, X: np.ndarray) -> "HierarchicalSegmentationModel":
        best_score = -1.0
        best_model = None

        for linkage_name in ["ward", "complete", "average"]:
            for n_clusters in range(2, 9):
                model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_name)
                labels = model.fit_predict(X)
                metrics = self.evaluate(X, labels)
                score = metrics.get("silhouette_score") or -1.0
                if score > best_score:
                    best_score = score
                    best_model = model
                    self.best_linkage = linkage_name
                    self.best_n_clusters = n_clusters

        self.model = best_model if best_model is not None else AgglomerativeClustering(n_clusters=2, linkage="ward").fit(X)
        self.labels_ = self.model.labels_
        self.dendrogram_data = linkage(X, method=self.best_linkage).tolist()
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.labels_ is None:
            raise ValueError("Model not fitted")
        return self.labels_

    def get_params(self) -> dict:
        return {
            "linkage": self.best_linkage,
            "n_clusters": self.best_n_clusters,
            "algorithm": "agglomerative",
            "dendrogram_size": len(self.dendrogram_data),
        }
