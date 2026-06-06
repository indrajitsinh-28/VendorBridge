from datetime import UTC, datetime

from sqlalchemy import case, extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice import Invoice
from app.models.purchase_order import PurchaseOrder, PurchaseOrderStatus
from app.models.quotation import Quotation, QuotationItem, QuotationStatus
from app.models.rfq import RFQ


async def get_summary(db: AsyncSession) -> dict:
    return {
        "total_rfqs": await db.scalar(select(func.count()).select_from(RFQ)) or 0,
        "total_quotations": await db.scalar(select(func.count()).select_from(Quotation)) or 0,
        "total_purchase_orders": await db.scalar(select(func.count()).select_from(PurchaseOrder)) or 0,
        "total_invoices": await db.scalar(select(func.count()).select_from(Invoice)) or 0,
        "total_spend": float(await db.scalar(select(func.coalesce(func.sum(Invoice.total_amount), 0))) or 0),
        "pending_approvals": await db.scalar(select(func.count()).select_from(PurchaseOrder).where(PurchaseOrder.status == PurchaseOrderStatus.pending)) or 0,
    }


async def get_monthly_trend(db: AsyncSession) -> list[dict]:
    now = datetime.now(UTC)
    start_year = now.year if now.month > 11 else now.year - 1
    start_month = ((now.month - 12) % 12) + 1
    rows = (
        await db.execute(
            select(
                extract("year", Invoice.created_at).label("year"),
                extract("month", Invoice.created_at).label("month"),
                func.coalesce(func.sum(Invoice.total_amount), 0).label("total_spend"),
                func.count(Invoice.po_id.distinct()).label("po_count"),
            )
            .where(Invoice.created_at >= datetime(start_year, start_month, 1, tzinfo=UTC))
            .group_by("year", "month")
        )
    ).all()
    by_month = {(int(year), int(month)): (float(spend), int(po_count)) for year, month, spend, po_count in rows}
    result = []
    for offset in range(11, -1, -1):
        month_index = now.month - offset
        year = now.year + (month_index - 1) // 12
        month = ((month_index - 1) % 12) + 1
        spend, po_count = by_month.get((year, month), (0.0, 0))
        result.append({"month": f"{year}-{month:02d}", "total_spend": round(spend, 2), "po_count": po_count})
    return result


async def get_vendor_performance(db: AsyncSession) -> list[dict]:
    rows = (
        await db.execute(
            select(
                Quotation.vendor_id,
                func.count(Quotation.id.distinct()).label("total_quotations"),
                func.sum(case((Quotation.status == QuotationStatus.accepted, 1), else_=0)).label("accepted_quotations"),
                func.coalesce(func.sum(Invoice.total_amount), 0).label("total_po_value"),
                func.coalesce(func.avg(QuotationItem.delivery_days), 0).label("avg_delivery_days"),
            )
            .outerjoin(PurchaseOrder, PurchaseOrder.quotation_id == Quotation.id)
            .outerjoin(Invoice, Invoice.po_id == PurchaseOrder.id)
            .outerjoin(QuotationItem, QuotationItem.quotation_id == Quotation.id)
            .group_by(Quotation.vendor_id)
        )
    ).all()
    return [
        {
            "vendor_id": vendor_id,
            "total_quotations": total,
            "accepted_quotations": accepted or 0,
            "total_po_value": round(float(value or 0), 2),
            "avg_delivery_days": round(float(avg_days or 0), 2),
        }
        for vendor_id, total, accepted, value, avg_days in rows
    ]
