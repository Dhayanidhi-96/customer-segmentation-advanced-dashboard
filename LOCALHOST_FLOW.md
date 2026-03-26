# Localhost Flow (Manual Mode)

## 1) Backend Environment Variables

```powershell
Set-Location "D:\cse\customer-segmentation\backend"
$env:POSTGRES_HOST='localhost'
$env:POSTGRES_PORT='5432'
$env:POSTGRES_DB='customer_segmentation'
$env:POSTGRES_USER='postgres'
$env:POSTGRES_PASSWORD='postgres'
$env:DATABASE_URL='postgresql+psycopg://postgres:postgres@localhost:5432/customer_segmentation'
$env:REDIS_URL='redis://localhost:6379/0'
```

## 2) Seed 2.5 Lakh Customers (No Training)

```powershell
.\.venv\Scripts\python.exe database\seed.py --customers 2.5lakh --force --no-train --batch-size 10000 --min-orders 1 --max-orders 8
```

## 3) Train Models on Existing Data

```powershell
.\.venv\Scripts\python.exe -c "from database.connection import SessionLocal; from ml.pipeline import run_full_training; db=SessionLocal(); print(run_full_training(db)); db.close()"
```

## 4) Run Backend API

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir "D:\cse\customer-segmentation\backend" --host 0.0.0.0 --port 8000 --reload
```

## 5) Run Celery Worker (Windows)

```powershell
.\.venv\Scripts\python.exe -m celery -A tasks.celery_app worker --loglevel=info --pool=solo
```

## 6) Run Celery Beat

```powershell
.\.venv\Scripts\python.exe -m celery -A tasks.celery_app beat --loglevel=info
```

## 7) Run Frontend

```powershell
Set-Location "D:\cse\customer-segmentation\frontend"
npm run dev -- --host
```

## 8) Verification

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/health"
Invoke-RestMethod -Uri "http://localhost:8000/api/models/best" | ConvertTo-Json -Depth 5
(Invoke-RestMethod -Uri "http://localhost:8000/api/customers").Count
```

## URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Dashboard: http://localhost:5173/dashboard
