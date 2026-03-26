# Customer Segmentation Platform

Production-style customer analytics platform for segmentation, model comparison, campaign triggering, and AI-assisted recommendations.

## What This Project Includes
- Interactive dashboard built with React and Recharts
- FastAPI backend with modular routers and services
- PostgreSQL data model for customers, orders, segments, campaigns, and model runs
- ML pipeline with multiple clustering strategies and automatic best-model selection
- Celery worker and beat for asynchronous jobs and scheduled retraining
- AI advisor endpoints for campaign and segment recommendations

## Tech Stack
- Frontend: React 18, Vite, Tailwind CSS, React Query, Axios, Recharts
- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic
- Data and Queue: PostgreSQL, Redis, Celery
- ML: scikit-learn, pandas, numpy, joblib
- Infra: Docker Compose, Nginx

## Project Structure
- backend: API, database models, ML pipeline, async tasks
- frontend: React application with pages, hooks, charts, and API clients
- report: project documentation and chapter-wise report files
- docker-compose.yml: complete container stack for local deployment

## Prerequisites
- Python 3.11+
- Node.js 18+
- npm 9+
- uv
- Docker Desktop (recommended for PostgreSQL and Redis)

## Local Setup (Recommended)
1. Clone repository and move into project root.
2. Copy environment template.

```bash
cp .env.example .env
```

3. Start database and Redis.

```bash
docker compose up -d postgres redis
```

4. Install backend dependencies.

```bash
cd backend
uv venv
uv pip install -r requirements.txt
```

5. Install frontend dependencies.

```bash
cd ../frontend
npm install
```

## Run the Application (Local)
Open separate terminals.

1. Backend API

```bash
cd backend
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Celery Worker

```bash
cd backend
uv run celery -A tasks.celery_app worker --loglevel=info
```

3. Celery Beat

```bash
cd backend
uv run celery -A tasks.celery_app beat --loglevel=info
```

4. Frontend

```bash
cd frontend
npm run dev -- --host
```

## Seed Data and Train Models
Default seed and training:

```bash
cd backend
uv run python database/seed.py
```

Large dataset example:

```bash
cd backend
uv run python database/seed.py --customers 2.5lakh --force
```

## Docker Full Stack

```bash
docker compose up --build
```

Application entry points:
- Frontend: http://localhost
- API docs: http://localhost:8000/docs

## Key API Routes
- GET /api/health
- GET /api/customers
- GET /api/segments/summary
- GET /api/analytics/dashboard
- GET /api/models/list
- POST /api/models/retrain
- POST /api/emails/trigger/{campaign_type}
- POST /api/ai/chat

## Screenshots
Screenshots will be added in a later update.

## Notes
- Best model artifacts are stored in backend/ml/artifacts.
- Seed script supports scaled synthetic generation for stress testing.
- Analytics endpoints include sampling and query optimizations for better frontend responsiveness.

## License
For academic and learning use. Add a formal license file if needed for distribution.
