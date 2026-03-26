from __future__ import annotations

import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database.connection import SessionLocal
from database.models import CampaignStatus, CampaignType, Customer, CustomerSegment, EmailCampaign
from services.email_service import EmailService
from services.email_templates import (
    rfm_personalized_template,
    upsell_template,
    vip_discount_template,
    winback_template,
)
from tasks.celery_app import celery_app


email_service = EmailService()


def _select_campaign(segment_label: str, recency_days: float, frequency: int, monetary: float, median_monetary: float) -> CampaignType:
    if segment_label == "VIP":
        return CampaignType.vip_discount
    if segment_label == "Churned" or recency_days > 90:
        return CampaignType.winback
    if segment_label == "Loyal" and frequency > 5 and monetary < median_monetary:
        return CampaignType.upsell
    return CampaignType.rfm_personalized


@celery_app.task(name="tasks.email_tasks.send_single_email")
def send_single_email(customer_id: str, campaign_type: str) -> dict:
    db: Session = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.id == uuid.UUID(customer_id)).first()
        if customer is None:
            return {"status": "skipped", "reason": "customer_not_found"}

        segment = (
            db.query(CustomerSegment)
            .filter(CustomerSegment.customer_id == customer.id, CustomerSegment.is_current.is_(True))
            .first()
        )
        if segment is None:
            return {"status": "skipped", "reason": "segment_not_found"}

        ctype = CampaignType(campaign_type)
        if ctype == CampaignType.vip_discount:
            subject, html = vip_discount_template(customer.name)
        elif ctype == CampaignType.winback:
            days = max(1, segment.rfm_recency_score * 20)
            subject, html = winback_template(customer.name, days)
        elif ctype == CampaignType.upsell:
            subject, html = upsell_template(customer.name)
        else:
            subject, html = rfm_personalized_template(customer.name, segment.segment_label.value)

        campaign = EmailCampaign(
            customer_id=customer.id,
            campaign_type=ctype,
            subject=subject,
            status=CampaignStatus.pending,
        )
        db.add(campaign)
        db.commit()

        try:
            email_service.send_email(customer.email, subject, html)
            campaign.status = CampaignStatus.sent
            campaign.sent_at = datetime.utcnow()
        except Exception as exc:  # noqa: BLE001
            campaign.status = CampaignStatus.failed
            campaign.error_message = str(exc)

        db.commit()
        return {"status": campaign.status.value, "campaign_id": str(campaign.id)}
    finally:
        db.close()


@celery_app.task(name="tasks.email_tasks.send_campaign_by_type")
def send_campaign_by_type(campaign_type: str) -> dict:
    db: Session = SessionLocal()
    try:
        segments = db.query(CustomerSegment).filter(CustomerSegment.is_current.is_(True)).all()
        if not segments:
            return {"status": "skipped", "reason": "no_segments"}

        median_monetary = sorted([s.rfm_monetary_score for s in segments])[len(segments) // 2]
        queued = 0
        for segment in segments:
            customer = db.query(Customer).filter(Customer.id == segment.customer_id).first()
            if customer is None:
                continue
            if CampaignType(campaign_type) != _select_campaign(
                segment.segment_label.value,
                float(30 * (6 - segment.rfm_recency_score)),
                segment.rfm_frequency_score,
                float(segment.rfm_monetary_score),
                float(median_monetary),
            ):
                continue
            send_single_email.delay(str(customer.id), campaign_type)
            queued += 1
        return {"status": "queued", "queued": queued}
    finally:
        db.close()


@celery_app.task(name="tasks.email_tasks.nightly_email_campaign")
def nightly_email_campaign() -> dict:
    db: Session = SessionLocal()
    try:
        segments = db.query(CustomerSegment).filter(CustomerSegment.is_current.is_(True)).all()
        if not segments:
            return {"status": "skipped", "reason": "no_segments"}

        median_monetary = sorted([s.rfm_monetary_score for s in segments])[len(segments) // 2]
        queued = 0

        for seg in segments:
            latest_campaign = (
                db.query(EmailCampaign)
                .filter(EmailCampaign.customer_id == seg.customer_id)
                .order_by(EmailCampaign.sent_at.desc().nullslast())
                .first()
            )
            if latest_campaign and latest_campaign.sent_at and latest_campaign.sent_at > datetime.utcnow() - timedelta(days=7):
                continue

            campaign_type = _select_campaign(
                seg.segment_label.value,
                float(30 * (6 - seg.rfm_recency_score)),
                seg.rfm_frequency_score,
                float(seg.rfm_monetary_score),
                float(median_monetary),
            )
            send_single_email.delay(str(seg.customer_id), campaign_type.value)
            queued += 1

        return {"status": "queued", "queued": queued}
    finally:
        db.close()
