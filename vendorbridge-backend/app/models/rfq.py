import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RFQStatus(str, enum.Enum):
    draft = "draft"
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class RFQ(Base):
    __tablename__ = "rfqs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[RFQStatus] = mapped_column(Enum(RFQStatus, name="rfq_status"), nullable=False, default=RFQStatus.draft)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    items: Mapped[list["RFQItem"]] = relationship(back_populates="rfq", cascade="all, delete-orphan", lazy="selectin")
    vendors: Mapped[list["RFQVendor"]] = relationship(back_populates="rfq", cascade="all, delete-orphan", lazy="selectin")
    quotations: Mapped[list["Quotation"]] = relationship(back_populates="rfq", lazy="selectin")


class RFQItem(Base):
    __tablename__ = "rfq_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfq_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rfqs.id", ondelete="CASCADE"), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)

    rfq: Mapped[RFQ] = relationship(back_populates="items")
    quotation_items: Mapped[list["QuotationItem"]] = relationship(back_populates="rfq_item", lazy="selectin")


class RFQVendor(Base):
    __tablename__ = "rfq_vendors"

    rfq_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rfqs.id", ondelete="CASCADE"), primary_key=True)
    vendor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("vendors.id"), primary_key=True)

    rfq: Mapped[RFQ] = relationship(back_populates="vendors")
