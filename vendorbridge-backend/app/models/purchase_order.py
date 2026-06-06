import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PurchaseOrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    delivered = "delivered"
    cancelled = "cancelled"


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfq_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rfqs.id"), nullable=False)
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("quotations.id"), nullable=False, unique=True)
    po_number: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    status: Mapped[PurchaseOrderStatus] = mapped_column(Enum(PurchaseOrderStatus, name="purchase_order_status"), nullable=False, default=PurchaseOrderStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    quotation: Mapped["Quotation"] = relationship(back_populates="purchase_order", lazy="selectin")
    items: Mapped[list["POItem"]] = relationship(back_populates="purchase_order", cascade="all, delete-orphan", lazy="selectin")
    invoice: Mapped["Invoice | None"] = relationship(back_populates="purchase_order")


class POItem(Base):
    __tablename__ = "po_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    po_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    tax_pct: Mapped[float] = mapped_column(Float, nullable=False, default=18.0)

    purchase_order: Mapped[PurchaseOrder] = relationship(back_populates="items")
