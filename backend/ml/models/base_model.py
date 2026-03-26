from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import joblib
import numpy as np

from ml.evaluator import evaluate_clustering


class BaseClusteringModel(ABC):
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.model = None
        self.labels_: np.ndarray | None = None

    @abstractmethod
    def fit(self, X: np.ndarray) -> "BaseClusteringModel":
        ...

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        ...

    @abstractmethod
    def get_params(self) -> dict:
        ...

    def evaluate(self, X: np.ndarray, labels: np.ndarray | None = None) -> dict[str, float | None]:
        y = labels if labels is not None else self.predict(X)
        return evaluate_clustering(X, y)

    def save(self, path: str | Path) -> None:
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: str | Path) -> "BaseClusteringModel":
        return joblib.load(path)
