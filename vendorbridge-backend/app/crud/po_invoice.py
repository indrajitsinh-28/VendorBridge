import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.invoice import Invoice, InvoiceItem, InvoiceStatus
from app.models.purchase_order import POItem, PurchaseOrder, PurchaseOrderStatus
from app.models.quotation import Quotation, QuotationItem, QuotationStatus


def _po_to_dict(po: PurchaseOrder) -> dict:
    item_rows = []
    subtotal = 0.0
    tax_amount = 0.0
    for item in po.items:
        line_subtotal = item.quantity * item.unit_price
        line_tax = line_subtotal * item.tax_pct / 100
        subtotal += line_subtotal
        tax_amount += line_tax
        item_rows.append(
            {
                "id": item.id,
                "po_id": item.po_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "tax_pct": item.tax_pct,
                "line_subtotal": round(line_subtotal, 2),
                "line_tax": round(line_tax, 2),
                "line_total": round(line_subtotal + line_tax, 2),
            }
        )
    return {
        "id": po.id,
        "rfq_id": po.rfq_id,
        "quotation_id": po.quotation_id,
        "po_number": po.po_number,
        "status": po.status,
        "created_at": po.created_at,
        "subtotal": round(subtotal, 2),
        "tax_amount": round(tax_amount, 2),
        "total_amount": round(subtotal + tax_amount, 2),
        "items": item_rows,
    }


async def _next_sequence_number(db: AsyncSession, model: type, column_name: str, prefix: str) -> str:
    today = datetime.now(UTC).strftime("%Y%m%d")
    column = getattr(model, column_name)
    count = await db.scalar(select(func.count()).select_from(model).where(column.like(f"{prefix}-{today}-%")))
    return f"{prefix}-{today}-{int(count or 0) + 1:04d}"


async def create_purchase_order(db: AsyncSession, rfq_id: uuid.UUID, quotation_id: uuid.UUID) -> dict:
    quotation = (
        await db.execute(
            select(Quotation)
            .options(selectinload(Quotation.items).selectinload(QuotationItem.rfq_item))
            .where(Quotation.id == quotation_id, Quotation.rfq_id == rfq_id)
        )
    ).scalar_one_or_none()
    if quotation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found for RFQ")
    if quotation.status != QuotationStatus.accepted:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only accepted quotations can create purchase orders")
    po = PurchaseOrder(
        rfq_id=rfq_id,
        quotation_id=quotation_id,
        po_number=await _next_sequence_number(db, PurchaseOrder, "po_number", "PO"),
        items=[
            POItem(
                product_name=item.rfq_item.product_name,
                quantity=item.rfq_item.quantity,
                unit_price=item.unit_price,
                tax_pct=18.0,
            )
            for item in quotation.items
        ],
    )
    db.add(po)
    await db.commit()
    return await get_purchase_order(db, po.id)


async def get_purchase_order(db: AsyncSession, po_id: uuid.UUID) -> dict | None:
    po = (await db.execute(select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).where(PurchaseOrder.id == po_id))).scalar_one_or_none()
    return _po_to_dict(po) if po else None


async def update_purchase_order_status(db: AsyncSession, po_id: uuid.UUID, new_status: PurchaseOrderStatus) -> dict | None:
    po = (await db.execute(select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).where(PurchaseOrder.id == po_id))).scalar_one_or_none()
    if po is None:
        return None
    po.status = new_status
    await db.commit()
    return await get_purchase_order(db, po_id)


async def create_invoice(db: AsyncSession, po_id: uuid.UUID) -> Invoice:
    po = (await db.execute(select(PurchaseOrder).options(selectinload(PurchaseOrder.items)).where(PurchaseOrder.id == po_id))).scalar_one_or_none()
    if po is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    subtotal = sum(item.quantity * item.unit_price for item in po.items)
    tax_amount = sum(item.quantity * item.unit_price * item.tax_pct / 100 for item in po.items)
    invoice = Invoice(
        po_id=po_id,
        invoice_number=await _next_sequence_number(db, Invoice, "invoice_number", "INV"),
        subtotal=round(subtotal, 2),
        tax_amount=round(tax_amount, 2),
        total_amount=round(subtotal + tax_amount, 2),
        items=[
            InvoiceItem(
                description=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                tax_pct=item.tax_pct,
                line_total=round(item.quantity * item.unit_price * (1 + item.tax_pct / 100), 2),
            )
            for item in po.items
        ],
    )
    db.add(invoice)
    await db.commit()
    return await get_invoice(db, invoice.id)


async def get_invoice(db: AsyncSession, invoice_id: uuid.UUID) -> Invoice | None:
    stmt = select(Invoice).options(selectinload(Invoice.items), selectinload(Invoice.purchase_order).selectinload(PurchaseOrder.quotation)).where(Invoice.id == invoice_id)
    return (await db.execute(stmt)).scalar_one_or_none()


async def update_invoice_status(db: AsyncSession, invoice_id: uuid.UUID, new_status: InvoiceStatus) -> Invoice | None:
    invoice = await get_invoice(db, invoice_id)
    if invoice is None:
        return None
    invoice.status = new_status
    await db.commit()
    return await get_invoice(db, invoice_id)
