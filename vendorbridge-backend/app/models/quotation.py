import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class QuotationStatus(str, enum.Enum):
    draft = "draft"
    submitted = "submitted"
    accepted = "accepted"
    rejected = "rejected"


class Quotation(Base):
    __tablename__ = "quotations"
    __table_args__ = (UniqueConstraint("rfq_id", "vendor_id", name="uq_quotation_rfq_vendor"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfq_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rfqs.id", ondelete="CASCADE"), nullable=False)
    vendor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False)
    status: Mapped[QuotationStatus] = mapped_column(Enum(QuotationStatus, name="quotation_status"), nullable=False, default=QuotationStatus.draft)
    notes: Mapped[str | None] = mapped_column(Text)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    rfq: Mapped["RFQ"] = relationship(back_populates="quotations")
    items: Mapped[list["QuotationItem"]] = relationship(back_populates="quotation", cascade="all, delete-orphan", lazy="selectin")
    purchase_order: Mapped["PurchaseOrder | None"] = relationship(back_populates="quotation")


class QuotationItem(Base):
    __tablename__ = "quotation_items"
    __table_args__ = (UniqueConstraint("quotation_id", "rfq_item_id", name="uq_quotation_item_rfq_item"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quotation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False)
    rfq_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rfq_items.id"), nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    delivery_days: Mapped[int] = mapped_column(Integer, nullable=False)

    quotation: Mapped[Quotation] = relationship(back_populates="items")
    rfq_item: Mapped["RFQItem"] = relationship(back_populates="quotation_items", lazy="selectin")
