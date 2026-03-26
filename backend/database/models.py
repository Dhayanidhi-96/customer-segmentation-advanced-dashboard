import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class OrderStatus(str, enum.Enum):
    completed = "completed"
    cancelled = "cancelled"
    refunded = "refunded"


class SegmentLabel(str, enum.Enum):
    VIP = "VIP"
    Loyal = "Loyal"
    AtRisk = "At-Risk"
    New = "New"
    Churned = "Churned"
    Potential = "Potential"
    Outlier = "Outlier"


class CampaignType(str, enum.Enum):
    vip_discount = "vip_discount"
    winback = "winback"
    upsell = "upsell"
    rfm_personalized = "rfm_personalized"


class CampaignStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"
    opened = "opened"
    clicked = "clicked"


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    country: Mapped[str | None] = mapped_column(String(120), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    segments: Mapped[list["CustomerSegment"]] = relationship(
        "CustomerSegment", back_populates="customer", cascade="all, delete-orphan"
    )
    campaigns: Mapped[list["EmailCampaign"]] = relationship(
        "EmailCampaign", back_populates="customer", cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), index=True)
    order_number: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    items_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status"), default=OrderStatus.completed)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    customer: Mapped[Customer] = relationship("Customer", back_populates="orders")


class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), index=True)
    segment_label: Mapped[SegmentLabel] = mapped_column(Enum(SegmentLabel, name="segment_label"), nullable=False)
    rfm_recency_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rfm_frequency_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rfm_monetary_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rfm_total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    cluster_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    model_used: Mapped[str] = mapped_column(String(120), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    customer: Mapped[Customer] = relationship("Customer", back_populates="segments")


class EmailCampaign(Base):
    __tablename__ = "email_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"), index=True)
    campaign_type: Mapped[CampaignType] = mapped_column(Enum(CampaignType, name="campaign_type"), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[CampaignStatus] = mapped_column(
        Enum(CampaignStatus, name="campaign_status"), default=CampaignStatus.pending, nullable=False
    )
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    opened_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    clicked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    customer: Mapped[Customer] = relationship("Customer", back_populates="campaigns")


class ModelRun(Base):
    __tablename__ = "model_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name: Mapped[str] = mapped_column(String(120), nullable=False)
    hyperparameters: Mapped[dict] = mapped_column(JSONB().with_variant(JSON(), "sqlite"), nullable=False, default=dict)
    n_clusters: Mapped[int | None] = mapped_column(Integer, nullable=True)
    silhouette_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    davies_bouldin_index: Mapped[float | None] = mapped_column(Float, nullable=True)
    calinski_harabasz_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    training_duration_seconds: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    n_customers_trained: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_best: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    trained_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    artifact_path: Mapped[str] = mapped_column(String(500), nullable=False)


class GrokSession(Base):
    __tablename__ = "grok_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    messages: Mapped[list[dict]] = mapped_column(JSONB().with_variant(JSON(), "sqlite"), default=list, nullable=False)
    context_snapshot: Mapped[dict] = mapped_column(JSONB().with_variant(JSON(), "sqlite"), default=dict, nullable=False)
    total_tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
