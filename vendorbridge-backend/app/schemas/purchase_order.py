import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.purchase_order import PurchaseOrderStatus


class PurchaseOrderCreate(BaseModel):
    rfq_id: uuid.UUID
    quotation_id: uuid.UUID


class PurchaseOrderStatusUpdate(BaseModel):
    status: PurchaseOrderStatus


class POItemRead(BaseModel):
    id: uuid.UUID
    po_id: uuid.UUID
    product_name: str
    quantity: float
    unit_price: float
    tax_pct: float
    line_subtotal: float
    line_tax: float
    line_total: float

    model_config = ConfigDict(from_attributes=True)


class PurchaseOrderRead(BaseModel):
    id: uuid.UUID
    rfq_id: uuid.UUID
    quotation_id: uuid.UUID
    po_number: str
    status: PurchaseOrderStatus
    created_at: datetime
    subtotal: float
    tax_amount: float
    total_amount: float
    items: list[POItemRead]

    model_config = ConfigDict(from_attributes=True)
