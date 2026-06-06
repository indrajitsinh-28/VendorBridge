import uuid

from fastapi import HTTPException, status
from sqlalchemy import Select, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import text

from app.models.rfq import RFQ, RFQItem, RFQStatus, RFQVendor
from app.schemas.rfq import RFQCreate


async def _ensure_user_exists(db: AsyncSession, user_id: uuid.UUID) -> None:
    exists = await db.scalar(text("SELECT 1 FROM users WHERE id = :user_id"), {"user_id": str(user_id)})
    if exists is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="created_by user does not exist")


async def _ensure_vendors_exist(db: AsyncSession, vendor_ids: list[uuid.UUID]) -> None:
    missing_vendor_ids = []
    for vendor_id in dict.fromkeys(vendor_ids):
        exists = await db.scalar(text("SELECT 1 FROM vendors WHERE id = :vendor_id"), {"vendor_id": str(vendor_id)})
        if exists is None:
            missing_vendor_ids.append(str(vendor_id))
    if missing_vendor_ids:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "One or more vendors do not exist", "vendor_ids": missing_vendor_ids},
        )


async def create_rfq(db: AsyncSession, payload: RFQCreate) -> RFQ:
    await _ensure_user_exists(db, payload.created_by)
    await _ensure_vendors_exist(db, payload.vendor_ids)
    rfq = RFQ(
        title=payload.title,
        description=payload.description,
        deadline=payload.deadline,
        created_by=payload.created_by,
        items=[RFQItem(**item.model_dump()) for item in payload.items],
        vendors=[RFQVendor(vendor_id=vendor_id) for vendor_id in dict.fromkeys(payload.vendor_ids)],
    )
    db.add(rfq)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="RFQ references a user or vendor that does not exist",
        ) from exc
    return await get_rfq(db, rfq.id)


async def list_rfqs(db: AsyncSession, status: RFQStatus | None = None, created_by: uuid.UUID | None = None) -> list[dict]:
    item_count = select(func.count(RFQItem.id)).where(RFQItem.rfq_id == RFQ.id).scalar_subquery()
    vendor_count = select(func.count(RFQVendor.vendor_id)).where(RFQVendor.rfq_id == RFQ.id).scalar_subquery()
    stmt: Select = select(RFQ, item_count.label("item_count"), vendor_count.label("vendor_count")).order_by(RFQ.created_at.desc())
    if status is not None:
        stmt = stmt.where(RFQ.status == status)
    if created_by is not None:
        stmt = stmt.where(RFQ.created_by == created_by)
    rows = (await db.execute(stmt)).all()
    return [
        {
            "id": rfq.id,
            "title": rfq.title,
            "deadline": rfq.deadline,
            "status": rfq.status,
            "created_by": rfq.created_by,
            "created_at": rfq.created_at,
            "item_count": item_total,
            "vendor_count": vendor_total,
        }
        for rfq, item_total, vendor_total in rows
    ]


async def get_rfq(db: AsyncSession, rfq_id: uuid.UUID) -> RFQ | None:
    stmt = select(RFQ).options(selectinload(RFQ.items), selectinload(RFQ.vendors)).where(RFQ.id == rfq_id)
    return (await db.execute(stmt)).scalar_one_or_none()


async def update_rfq_status(db: AsyncSession, rfq_id: uuid.UUID, status: RFQStatus) -> RFQ | None:
    rfq = await get_rfq(db, rfq_id)
    if rfq is None:
        return None
    rfq.status = status
    await db.commit()
    return await get_rfq(db, rfq_id)


async def cancel_rfq(db: AsyncSession, rfq_id: uuid.UUID) -> RFQ | None:
    return await update_rfq_status(db, rfq_id, RFQStatus.cancelled)
