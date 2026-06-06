"""initial vendorbridge procurement tables

Revision ID: 20260606_0001
Revises:
Create Date: 2026-06-06 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260606_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    rfq_status = postgresql.ENUM("draft", "open", "closed", "cancelled", name="rfq_status", create_type=False)
    quotation_status = postgresql.ENUM("draft", "submitted", "accepted", "rejected", name="quotation_status", create_type=False)
    purchase_order_status = postgresql.ENUM("pending", "confirmed", "delivered", "cancelled", name="purchase_order_status", create_type=False)
    invoice_status = postgresql.ENUM("draft", "sent", "paid", name="invoice_status", create_type=False)
    rfq_status.create(op.get_bind(), checkfirst=True)
    quotation_status.create(op.get_bind(), checkfirst=True)
    purchase_order_status.create(op.get_bind(), checkfirst=True)
    invoice_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "rfqs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", rfq_status, nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
    )
    op.create_table(
        "rfq_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("rfq_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("product_name", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(["rfq_id"], ["rfqs.id"], ondelete="CASCADE"),
    )
    op.create_table(
        "rfq_vendors",
        sa.Column("rfq_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("vendor_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.ForeignKeyConstraint(["rfq_id"], ["rfqs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vendor_id"], ["vendors.id"]),
    )
    op.create_table(
        "quotations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("rfq_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("vendor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", quotation_status, nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["rfq_id"], ["rfqs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vendor_id"], ["vendors.id"]),
        sa.UniqueConstraint("rfq_id", "vendor_id", name="uq_quotation_rfq_vendor"),
    )
    op.create_table(
        "quotation_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rfq_item_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("delivery_days", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["quotation_id"], ["quotations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["rfq_item_id"], ["rfq_items.id"]),
        sa.UniqueConstraint("quotation_id", "rfq_item_id", name="uq_quotation_item_rfq_item"),
    )
    op.create_table(
        "purchase_orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("rfq_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quotation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("po_number", sa.String(length=32), nullable=False),
        sa.Column("status", purchase_order_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["rfq_id"], ["rfqs.id"]),
        sa.ForeignKeyConstraint(["quotation_id"], ["quotations.id"]),
        sa.UniqueConstraint("quotation_id"),
        sa.UniqueConstraint("po_number"),
    )
    op.create_index("ix_purchase_orders_po_number", "purchase_orders", ["po_number"])
    op.create_table(
        "po_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("po_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("product_name", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("tax_pct", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["po_id"], ["purchase_orders.id"], ondelete="CASCADE"),
    )
    op.create_table(
        "invoices",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("po_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("invoice_number", sa.String(length=32), nullable=False),
        sa.Column("status", invoice_status, nullable=False),
        sa.Column("subtotal", sa.Float(), nullable=False),
        sa.Column("tax_amount", sa.Float(), nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["po_id"], ["purchase_orders.id"]),
        sa.UniqueConstraint("invoice_number"),
        sa.UniqueConstraint("po_id"),
    )
    op.create_index("ix_invoices_invoice_number", "invoices", ["invoice_number"])
    op.create_table(
        "invoice_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("invoice_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("tax_pct", sa.Float(), nullable=False),
        sa.Column("line_total", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["invoice_id"], ["invoices.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("invoice_items")
    op.drop_index("ix_invoices_invoice_number", table_name="invoices")
    op.drop_table("invoices")
    op.drop_table("po_items")
    op.drop_index("ix_purchase_orders_po_number", table_name="purchase_orders")
    op.drop_table("purchase_orders")
    op.drop_table("quotation_items")
    op.drop_table("quotations")
    op.drop_table("rfq_vendors")
    op.drop_table("rfq_items")
    op.drop_table("rfqs")
    postgresql.ENUM(name="invoice_status").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="purchase_order_status").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="quotation_status").drop(op.get_bind(), checkfirst=True)
    postgresql.ENUM(name="rfq_status").drop(op.get_bind(), checkfirst=True)
