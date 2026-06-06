import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.quotation import Quotation, QuotationItem, QuotationStatus
from app.models.rfq import RFQ, RFQItem, RFQVendor
from app.schemas.quotation import QuotationCreate, QuotationUpdate


async def _ensure_vendor_assigned(db: AsyncSession, rfq_id: uuid.UUID, vendor_id: uuid.UUID) -> None:
    exists = await db.scalar(select(RFQVendor).where(RFQVendor.rfq_id == rfq_id, RFQVendor.vendor_id == vendor_id))
    if exists is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Vendor is not assigned to this RFQ")


async def _ensure_items_belong_to_rfq(db: AsyncSession, rfq_id: uuid.UUID, rfq_item_ids: list[uuid.UUID]) -> None:
    rows = await db.scalars(select(RFQItem.id).where(RFQItem.rfq_id == rfq_id, RFQItem.id.in_(rfq_item_ids)))
    found_ids = set(rows.all())
    if set(rfq_item_ids) != found_ids:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="One or more quotation items do not belong to the RFQ")


async def create_quotation(db: AsyncSession, payload: QuotationCreate) -> Quotation:
    await _ensure_vendor_assigned(db, payload.rfq_id, payload.vendor_id)
    await _ensure_items_belong_to_rfq(db, payload.rfq_id, [item.rfq_item_id for item in payload.items])
    quotation = Quotation(
        rfq_id=payload.rfq_id,
        vendor_id=payload.vendor_id,
        notes=payload.notes,
        items=[QuotationItem(**item.model_dump()) for item in payload.items],
    )
    db.add(quotation)
    await db.commit()
    return await get_quotation(db, quotation.id)


async def get_quotation(db: AsyncSession, quotation_id: uuid.UUID) -> Quotation | None:
    stmt = select(Quotation).options(selectinload(Quotation.items)).where(Quotation.id == quotation_id)
    return (await db.execute(stmt)).scalar_one_or_none()


async def update_quotation(db: AsyncSession, quotation_id: uuid.UUID, payload: QuotationUpdate) -> Quotation | None:
    quotation = await get_quotation(db, quotation_id)
    if quotation is None:
        return None
    if quotation.status != QuotationStatus.draft:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only draft quotations can be edited")
    await _ensure_items_belong_to_rfq(db, quotation.rfq_id, [item.rfq_item_id for item in payload.items])
    quotation.notes = payload.notes
    existing_items = {item.rfq_item_id: item for item in quotation.items}
    updated_items = []
    for item_payload in payload.items:
        item = existing_items.get(item_payload.rfq_item_id)
        if item is None:
            item = QuotationItem(rfq_item_id=item_payload.rfq_item_id)
        item.unit_price = item_payload.unit_price
        item.delivery_days = item_payload.delivery_days
        updated_items.append(item)
    quotation.items = updated_items
    await db.commit()
    return await get_quotation(db, quotation_id)


async def submit_quotation(db: AsyncSession, quotation_id: uuid.UUID) -> Quotation | None:
    quotation = await get_quotation(db, quotation_id)
    if quotation is None:
        return None
    if quotation.status != QuotationStatus.draft:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only draft quotations can be submitted")
    quotation.status = QuotationStatus.submitted
    quotation.submitted_at = datetime.now(UTC)
    await db.commit()
    return await get_quotation(db, quotation_id)


async def accept_quotation(db: AsyncSession, quotation_id: uuid.UUID) -> Quotation | None:
    quotation = await get_quotation(db, quotation_id)
    if quotation is None:
        return None
    if quotation.status != QuotationStatus.submitted:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only submitted quotations can be accepted")
    quotation.status = QuotationStatus.accepted
    await db.commit()
    return await get_quotation(db, quotation_id)


async def reject_quotation(db: AsyncSession, quotation_id: uuid.UUID) -> Quotation | None:
    quotation = await get_quotation(db, quotation_id)
    if quotation is None:
        return None
    if quotation.status != QuotationStatus.submitted:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only submitted quotations can be rejected")
    quotation.status = QuotationStatus.rejected
    await db.commit()
    return await get_quotation(db, quotation_id)


async def compare_rfq_quotations(db: AsyncSession, rfq_id: uuid.UUID, sort_by: str, order: str) -> dict | None:
    rfq = (await db.execute(select(RFQ).options(selectinload(RFQ.items)).where(RFQ.id == rfq_id))).scalar_one_or_none()
    if rfq is None:
        return None
    quotations = (
        await db.execute(
            select(Quotation)
            .options(selectinload(Quotation.items).selectinload(QuotationItem.rfq_item))
            .where(Quotation.rfq_id == rfq_id, Quotation.status == QuotationStatus.submitted)
        )
    ).scalars().all()
    quantity_by_item = {item.id: item.quantity for item in rfq.items}
    entries = []
    for quotation in quotations:
        total_price = sum(item.unit_price * quantity_by_item.get(item.rfq_item_id, 0) for item in quotation.items)
        avg_delivery = sum(item.delivery_days for item in quotation.items) / len(quotation.items) if quotation.items else 0
        entries.append(
            {
                "quotation_id": quotation.id,
                "vendor_id": quotation.vendor_id,
                "vendor_name": f"Vendor {quotation.vendor_id}",
                "total_price": round(total_price, 2),
                "avg_delivery_days": round(avg_delivery, 2),
                "is_lowest_price": False,
                "items": [
                    {"rfq_item_id": item.rfq_item_id, "unit_price": item.unit_price, "delivery_days": item.delivery_days}
                    for item in quotation.items
                ],
            }
        )
    if entries:
        lowest = min(entry["total_price"] for entry in entries)
        for entry in entries:
            entry["is_lowest_price"] = entry["total_price"] == lowest
    reverse = order == "desc"
    key = "total_price" if sort_by == "price" else "avg_delivery_days"
    entries.sort(key=lambda entry: entry[key], reverse=reverse)
    return {
        "rfq_id": rfq.id,
        "rfq_title": rfq.title,
        "items": [{"item_name": item.product_name, "quantity": item.quantity, "unit": item.unit} for item in rfq.items],
        "quotations": entries,
    }
