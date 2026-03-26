# Customer Segmentation Platform

Full-stack, real-time customer segmentation system for e-commerce using React + FastAPI + PostgreSQL + Celery + ML clustering + Grok AI.

## Tech Stack
- Frontend: React 18, Vite, Tailwind CSS, Recharts, Axios, React Query
- Backend: FastAPI, SQLAlchemy ORM, Alembic, Celery
- Data: PostgreSQL 15, Redis
- ML: scikit-learn, pandas, numpy, joblib, mlflow
- AI: Grok (xAI) via OpenAI-compatible SDK
- Delivery: Docker Compose + Nginx

## Quick Start (Docker)
1. Copy environment file:
   - `cp .env.example .env`
2. Start everything:
   - `docker compose up --build`
3. Open:
   - `http://localhost`

## Quick Start (Local with uv virtual environment)
1. Backend env and deps:
   - `cd backend`
   - `uv venv`
   - Windows CMD: `.venv\\Scripts\\activate`
   - `uv pip install -r requirements.txt`
2. Frontend deps:
   - `cd ../frontend`
   - `npm install`
3. Start PostgreSQL + Redis (Docker only):
   - `cd ..`
   - `docker compose up postgres redis -d`
4. Run API:
   - `cd backend`
   - `uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000`
5. Run worker + beat:
   - `uv run celery -A tasks.celery_app worker --loglevel=info`
   - `uv run celery -A tasks.celery_app beat --loglevel=info`
6. Run frontend:
   - `cd ../frontend`
   - `npm run dev -- --host`

## Seed Data
- Generates 500 customers and realistic order patterns (2-year span).
- Trains all clustering models and picks the best model automatically.

Command:
- `cd backend`
- `uv run python database/seed.py`

## API Endpoints
- `GET /api/health`
- `POST /api/customers/segment`
- `GET /api/customers`
- `GET /api/customers/{id}`
- `GET /api/segments/summary`
- `GET /api/analytics/dashboard`
- `GET /api/analytics/rfm-heatmap`
- `GET /api/analytics/cluster-scatter`
- `GET /api/analytics/revenue-by-segment`
- `GET /api/analytics/retention-cohort`
- `GET /api/models/list`
- `GET /api/models/best`
- `POST /api/models/retrain`
- `POST /api/emails/trigger/{campaign_type}`
- `GET /api/emails/campaigns`
- `POST /api/ai/chat`
- `GET /api/ai/recommendations`

## Implementation Notes
- Model artifacts saved under `backend/ml/artifacts/`.
- Best model persisted as `best_model.pkl`.
- Email sending logs persisted before send attempts.
- Celery tasks are idempotent and safe to retry.

## Next Improvements
- Add authenticated admin login.
- Add websocket stream for live campaign/task status.
- Add pytest test suite + CI pipeline.
