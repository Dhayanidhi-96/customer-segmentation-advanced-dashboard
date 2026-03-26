from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import CampaignType, EmailCampaign
from tasks.email_tasks import send_campaign_by_type


router = APIRouter()


@router.post("/trigger/{campaign_type}")
def trigger_campaign(campaign_type: CampaignType, async_task: bool = True, db: Session = Depends(get_db)) -> dict:
    if async_task:
        task = send_campaign_by_type.delay(campaign_type.value)
        return {"status": "queued", "task_id": task.id, "campaign_type": campaign_type.value}
    result = send_campaign_by_type(campaign_type.value)
    return {"status": "completed", "result": result}


@router.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)) -> dict:
    campaigns = db.query(EmailCampaign).order_by(EmailCampaign.sent_at.desc().nullslast()).limit(500).all()
    total = db.query(func.count(EmailCampaign.id)).scalar() or 0
    opened = db.query(func.count(EmailCampaign.id)).filter(EmailCampaign.opened_at.is_not(None)).scalar() or 0
    clicked = db.query(func.count(EmailCampaign.id)).filter(EmailCampaign.clicked_at.is_not(None)).scalar() or 0

    return {
        "stats": {
            "total": total,
            "open_rate": (opened / total * 100) if total else 0,
            "click_rate": (clicked / total * 100) if total else 0,
            "timestamp": datetime.utcnow(),
        },
        "data": [
            {
                "id": str(c.id),
                "customer_id": str(c.customer_id),
                "campaign_type": c.campaign_type.value,
                "subject": c.subject,
                "status": c.status.value,
                "sent_at": c.sent_at,
                "opened_at": c.opened_at,
                "clicked_at": c.clicked_at,
                "error_message": c.error_message,
            }
            for c in campaigns
        ],
    }
