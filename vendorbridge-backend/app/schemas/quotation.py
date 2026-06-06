import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.quotation import QuotationStatus


class QuotationItemCreate(BaseModel):
    rfq_item_id: uuid.UUID
    unit_price: float = Field(ge=0)
    delivery_days: int = Field(ge=0)


class QuotationItemRead(QuotationItemCreate):
    id: uuid.UUID
    quotation_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class QuotationCreate(BaseModel):
    rfq_id: uuid.UUID
    vendor_id: uuid.UUID
    notes: str | None = None
    items: list[QuotationItemCreate] = Field(min_length=1)


class QuotationUpdate(BaseModel):
    notes: str | None = None
    items: list[QuotationItemCreate] = Field(min_length=1)


class QuotationRead(BaseModel):
    id: uuid.UUID
    rfq_id: uuid.UUID
    vendor_id: uuid.UUID
    status: QuotationStatus
    notes: str | None
    submitted_at: datetime | None
    created_at: datetime
    items: list[QuotationItemRead]

    model_config = ConfigDict(from_attributes=True)


class RFQComparisonItem(BaseModel):
    item_name: str
    quantity: float
    unit: str


class QuotationComparisonItem(BaseModel):
    rfq_item_id: uuid.UUID
    unit_price: float
    delivery_days: int


class QuotationComparisonEntry(BaseModel):
    quotation_id: uuid.UUID
    vendor_id: uuid.UUID
    vendor_name: str
    total_price: float
    avg_delivery_days: float
    is_lowest_price: bool
    items: list[QuotationComparisonItem]


class RFQQuotationComparison(BaseModel):
    rfq_id: uuid.UUID
    rfq_title: str
    items: list[RFQComparisonItem]
    quotations: list[QuotationComparisonEntry]
