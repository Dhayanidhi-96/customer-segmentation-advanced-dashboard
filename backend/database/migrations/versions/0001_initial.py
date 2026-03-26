"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-03-26
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


order_status = sa.Enum("completed", "cancelled", "refunded", name="order_status")
segment_label = sa.Enum("VIP", "Loyal", "At-Risk", "New", "Churned", "Potential", "Outlier", name="segment_label")
campaign_type = sa.Enum("vip_discount", "winback", "upsell", "rfm_personalized", name="campaign_type")
campaign_status = sa.Enum("pending", "sent", "failed", "opened", "clicked", name="campaign_status")


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("country", sa.String(length=120), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("gender", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_customers_email", "customers", ["email"])

    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("customers.id"), nullable=False),
        sa.Column("order_number", sa.String(length=64), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("items_count", sa.Integer(), nullable=False),
        sa.Column("status", order_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("order_number"),
    )
    op.create_index("ix_orders_customer_id", "orders", ["customer_id"])

    op.create_table(
        "customer_segments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("customers.id"), nullable=False),
        sa.Column("segment_label", segment_label, nullable=False),
        sa.Column("rfm_recency_score", sa.Integer(), nullable=False),
        sa.Column("rfm_frequency_score", sa.Integer(), nullable=False),
        sa.Column("rfm_monetary_score", sa.Integer(), nullable=False),
        sa.Column("rfm_total_score", sa.Integer(), nullable=False),
        sa.Column("cluster_id", sa.Integer(), nullable=True),
        sa.Column("model_used", sa.String(length=120), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("assigned_at", sa.DateTime(), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False),
    )
    op.create_index("ix_customer_segments_customer_id", "customer_segments", ["customer_id"])

    op.create_table(
        "email_campaigns",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("customers.id"), nullable=False),
        sa.Column("campaign_type", campaign_type, nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("status", campaign_status, nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.Column("opened_at", sa.DateTime(), nullable=True),
        sa.Column("clicked_at", sa.DateTime(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
    )
    op.create_index("ix_email_campaigns_customer_id", "email_campaigns", ["customer_id"])

    op.create_table(
        "model_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("model_name", sa.String(length=120), nullable=False),
        sa.Column("hyperparameters", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("n_clusters", sa.Integer(), nullable=True),
        sa.Column("silhouette_score", sa.Float(), nullable=True),
        sa.Column("davies_bouldin_index", sa.Float(), nullable=True),
        sa.Column("calinski_harabasz_score", sa.Float(), nullable=True),
        sa.Column("training_duration_seconds", sa.Float(), nullable=False),
        sa.Column("n_customers_trained", sa.Integer(), nullable=False),
        sa.Column("is_best", sa.Boolean(), nullable=False),
        sa.Column("trained_at", sa.DateTime(), nullable=False),
        sa.Column("artifact_path", sa.String(length=500), nullable=False),
    )

    op.create_table(
        "grok_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", sa.String(length=255), nullable=False),
        sa.Column("messages", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("context_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("total_tokens_used", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_grok_sessions_session_id", "grok_sessions", ["session_id"])


def downgrade() -> None:
    op.drop_index("ix_grok_sessions_session_id", table_name="grok_sessions")
    op.drop_table("grok_sessions")
    op.drop_table("model_runs")
    op.drop_index("ix_email_campaigns_customer_id", table_name="email_campaigns")
    op.drop_table("email_campaigns")
    op.drop_index("ix_customer_segments_customer_id", table_name="customer_segments")
    op.drop_table("customer_segments")
    op.drop_index("ix_orders_customer_id", table_name="orders")
    op.drop_table("orders")
    op.drop_index("ix_customers_email", table_name="customers")
    op.drop_table("customers")
    campaign_status.drop(op.get_bind(), checkfirst=True)
    campaign_type.drop(op.get_bind(), checkfirst=True)
    segment_label.drop(op.get_bind(), checkfirst=True)
    order_status.drop(op.get_bind(), checkfirst=True)
