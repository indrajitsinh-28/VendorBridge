import uuid

from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_rfqs: int
    total_quotations: int
    total_purchase_orders: int
    total_invoices: int
    total_spend: float
    pending_approvals: int


class MonthlyTrend(BaseModel):
    month: str
    total_spend: float
    po_count: int


class VendorPerformance(BaseModel):
    vendor_id: uuid.UUID
    total_quotations: int
    accepted_quotations: int
    total_po_value: float
    avg_delivery_days: float
