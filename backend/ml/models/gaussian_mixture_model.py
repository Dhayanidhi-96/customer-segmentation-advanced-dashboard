from __future__ import annotations

import numpy as np
from sklearn.mixture import GaussianMixture

from ml.models.base_model import BaseClusteringModel


class GaussianMixtureSegmentationModel(BaseClusteringModel):
    def __init__(self) -> None:
        super().__init__("gaussian_mixture")
        self.best_n_components = 2

    def fit(self, X: np.ndarray) -> "GaussianMixtureSegmentationModel":
        best_bic = float("inf")
        best_model = None
        large_dataset = len(X) > 120000

        fit_X = X
        if large_dataset:
            rng = np.random.default_rng(42)
            sample_idx = rng.choice(len(X), size=120000, replace=False)
            fit_X = X[sample_idx]

        component_range = range(2, 6) if large_dataset else range(2, 9)

        for n_components in component_range:
            model = GaussianMixture(n_components=n_components, covariance_type="diag", random_state=42, max_iter=200)
            model.fit(fit_X)
            bic = model.bic(fit_X)
            if bic < best_bic:
                best_bic = bic
                best_model = model
                self.best_n_components = n_components

        self.model = best_model if best_model is not None else GaussianMixture(n_components=2, random_state=42).fit(fit_X)
        self.labels_ = self.model.predict(X)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not fitted")
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not fitted")
        return self.model.predict_proba(X)

    def get_params(self) -> dict:
        return {"n_components": self.best_n_components, "algorithm": "gaussian_mixture"}
