import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.rfq import RFQStatus


class RFQItemCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=255)
    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1, max_length=50)


class RFQItemRead(RFQItemCreate):
    id: uuid.UUID
    rfq_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class RFQCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    deadline: datetime
    created_by: uuid.UUID
    items: list[RFQItemCreate] = Field(min_length=1)
    vendor_ids: list[uuid.UUID] = Field(min_length=1)


class RFQStatusUpdate(BaseModel):
    status: RFQStatus


class RFQVendorRead(BaseModel):
    vendor_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class RFQRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    deadline: datetime
    status: RFQStatus
    created_by: uuid.UUID
    created_at: datetime
    items: list[RFQItemRead]
    vendors: list[RFQVendorRead]

    model_config = ConfigDict(from_attributes=True)


class RFQListRead(BaseModel):
    id: uuid.UUID
    title: str
    deadline: datetime
    status: RFQStatus
    created_by: uuid.UUID
    created_at: datetime
    item_count: int
    vendor_count: int
