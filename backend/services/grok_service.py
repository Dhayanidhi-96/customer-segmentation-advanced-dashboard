from __future__ import annotations

from datetime import datetime

from openai import OpenAI
from sqlalchemy import func
from sqlalchemy.orm import Session

from config import settings
from database.models import CustomerSegment, GrokSession, ModelRun, SegmentLabel


SYSTEM_PROMPT = """
You are an expert e-commerce marketing analyst and customer segmentation specialist.
You have access to real-time customer segmentation data for this e-commerce business.

Current business context will be injected with each message including:
- Segment distribution (how many customers in each segment)
- Revenue breakdown by segment
- Recent RFM score trends
- Email campaign performance stats
- Best performing ML model and its metrics

Your job is to:
1. Explain why customers are in certain segments
2. Recommend specific marketing campaigns per segment
3. Identify at-risk patterns before churn happens
4. Suggest optimal email timing and content
5. Give actionable business insights from clustering results

Always be specific, data-driven, and actionable. Reference the actual numbers provided.
"""


client = OpenAI(api_key=settings.GROK_API_KEY, base_url="https://api.x.ai/v1")


def build_context(db: Session) -> str:
    segment_counts = (
        db.query(CustomerSegment.segment_label, func.count(CustomerSegment.id))
        .filter(CustomerSegment.is_current.is_(True))
        .group_by(CustomerSegment.segment_label)
        .all()
    )
    best_model = (
        db.query(ModelRun)
        .filter(ModelRun.is_best.is_(True))
        .order_by(ModelRun.trained_at.desc())
        .first()
    )

    segment_text = "\n".join([f"- {label.value if isinstance(label, SegmentLabel) else label}: {count}" for label, count in segment_counts])

    model_text = "No model run available"
    if best_model:
        model_text = (
            f"Best model: {best_model.model_name}, silhouette={best_model.silhouette_score}, "
            f"dbi={best_model.davies_bouldin_index}, ch={best_model.calinski_harabasz_score}, "
            f"trained_at={best_model.trained_at}"
        )

    return f"Segment distribution:\n{segment_text}\n\n{model_text}"


async def chat(session_id: str, user_message: str, db: Session) -> str:
    context = build_context(db)
    session = db.query(GrokSession).filter(GrokSession.session_id == session_id).first()
    if session is None:
        session = GrokSession(session_id=session_id, messages=[], context_snapshot={})
        db.add(session)
        db.flush()

    history = session.messages or []
    history.append({"role": "user", "content": user_message})

    if not settings.GROK_API_KEY:
        response_text = (
            "Grok API key is not configured.\n"
            "Set GROK_API_KEY in .env to enable AI recommendations.\n"
            f"Context snapshot:\n{context}"
        )
    else:
        completion = client.chat.completions.create(
            model=settings.GROK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": context},
                *history,
            ],
            temperature=0.3,
        )
        response_text = completion.choices[0].message.content or "No response"
        session.total_tokens_used += int(getattr(completion.usage, "total_tokens", 0) or 0)

    history.append({"role": "assistant", "content": response_text})

    session.messages = history[-30:]
    session.context_snapshot = {"context": context}
    session.updated_at = datetime.utcnow()
    db.commit()

    return response_text
