from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import ModelRun
from ml.pipeline import run_full_training
from tasks.retrain_tasks import retrain_models_async


router = APIRouter()


@router.get("/list")
def list_models(db: Session = Depends(get_db)) -> dict:
    runs = db.query(ModelRun).order_by(ModelRun.trained_at.desc()).all()
    return {
        "data": [
            {
                "id": str(run.id),
                "model_name": run.model_name,
                "hyperparameters": run.hyperparameters,
                "n_clusters": run.n_clusters,
                "silhouette_score": run.silhouette_score,
                "davies_bouldin_index": run.davies_bouldin_index,
                "calinski_harabasz_score": run.calinski_harabasz_score,
                "training_duration_seconds": run.training_duration_seconds,
                "n_customers_trained": run.n_customers_trained,
                "is_best": run.is_best,
                "trained_at": run.trained_at,
                "artifact_path": run.artifact_path,
            }
            for run in runs
        ]
    }


@router.get("/best")
def best_model(db: Session = Depends(get_db)) -> dict:
    run = db.query(ModelRun).filter(ModelRun.is_best.is_(True)).order_by(ModelRun.trained_at.desc()).first()
    if run is None:
        return {"data": None}
    return {
        "data": {
            "id": str(run.id),
            "model_name": run.model_name,
            "hyperparameters": run.hyperparameters,
            "silhouette_score": run.silhouette_score,
            "davies_bouldin_index": run.davies_bouldin_index,
            "calinski_harabasz_score": run.calinski_harabasz_score,
            "trained_at": run.trained_at,
        }
    }


@router.post("/retrain")
def retrain_models(async_task: bool = True, db: Session = Depends(get_db)) -> dict:
    if async_task:
        task = retrain_models_async.delay()
        return {"status": "queued", "task_id": task.id}
    result = run_full_training(db)
    return {"status": "completed", "result": result}
