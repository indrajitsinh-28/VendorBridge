import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import rfq as rfq_crud
from app.database import get_db
from app.models.rfq import RFQStatus
from app.schemas.rfq import RFQCreate, RFQListRead, RFQRead, RFQStatusUpdate

router = APIRouter(prefix="/rfqs", tags=["RFQs"])


@router.post("/", response_model=RFQRead, status_code=status.HTTP_201_CREATED)
async def create_rfq(payload: RFQCreate, db: AsyncSession = Depends(get_db)):
    return await rfq_crud.create_rfq(db, payload)


@router.get("/", response_model=list[RFQListRead])
async def list_rfqs(status_filter: RFQStatus | None = None, created_by: uuid.UUID | None = None, db: AsyncSession = Depends(get_db)):
    return await rfq_crud.list_rfqs(db, status_filter, created_by)


@router.get("/{rfq_id}", response_model=RFQRead)
async def get_rfq(rfq_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    rfq = await rfq_crud.get_rfq(db, rfq_id)
    if rfq is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    return rfq


@router.patch("/{rfq_id}/status", response_model=RFQRead)
async def update_rfq_status(rfq_id: uuid.UUID, payload: RFQStatusUpdate, db: AsyncSession = Depends(get_db)):
    rfq = await rfq_crud.update_rfq_status(db, rfq_id, payload.status)
    if rfq is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    return rfq


@router.delete("/{rfq_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rfq(rfq_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    rfq = await rfq_crud.cancel_rfq(db, rfq_id)
    if rfq is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
