from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import engine
from database.models import Base
from routers import ai, analytics, customers, emails, models, segments


app = FastAPI(title="Customer Segmentation Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(segments.router, prefix="/api/segments", tags=["segments"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(emails.router, prefix="/api/emails", tags=["emails"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
