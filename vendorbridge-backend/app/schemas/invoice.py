import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.invoice import InvoiceStatus


class InvoiceCreate(BaseModel):
    po_id: uuid.UUID


class InvoiceStatusUpdate(BaseModel):
    status: InvoiceStatus


class InvoiceEmailRequest(BaseModel):
    recipient_email: EmailStr
    subject: str
    body: str


class InvoiceItemRead(BaseModel):
    id: uuid.UUID
    invoice_id: uuid.UUID
    description: str
    quantity: float
    unit_price: float
    tax_pct: float
    line_total: float

    model_config = ConfigDict(from_attributes=True)


class InvoiceRead(BaseModel):
    id: uuid.UUID
    po_id: uuid.UUID
    invoice_number: str
    status: InvoiceStatus
    subtotal: float
    tax_amount: float
    total_amount: float
    created_at: datetime
    items: list[InvoiceItemRead]

    model_config = ConfigDict(from_attributes=True)


class InvoiceEmailResponse(BaseModel):
    success: bool
    message: str
