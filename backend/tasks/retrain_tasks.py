from __future__ import annotations

from database.connection import SessionLocal
from ml.pipeline import run_full_training
from tasks.celery_app import celery_app


@celery_app.task(name="tasks.retrain_tasks.retrain_models_async")
def retrain_models_async() -> dict:
    db = SessionLocal()
    try:
        return run_full_training(db)
    finally:
        db.close()


@celery_app.task(name="tasks.retrain_tasks.weekly_model_retrain")
def weekly_model_retrain() -> dict:
    return retrain_models_async()
