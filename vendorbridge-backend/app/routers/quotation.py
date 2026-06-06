import uuid
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import quotation as quotation_crud
from app.database import get_db
from app.schemas.quotation import QuotationCreate, QuotationRead, QuotationUpdate, RFQQuotationComparison

router = APIRouter(prefix="/quotations", tags=["Quotations"])
comparison_router = APIRouter(prefix="/rfqs", tags=["RFQ Quotations"])


@router.post("/", response_model=QuotationRead, status_code=status.HTTP_201_CREATED)
async def create_quotation(payload: QuotationCreate, db: AsyncSession = Depends(get_db)):
    return await quotation_crud.create_quotation(db, payload)


@router.get("/{quotation_id}", response_model=QuotationRead)
async def get_quotation(quotation_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    quotation = await quotation_crud.get_quotation(db, quotation_id)
    if quotation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    return quotation


@router.patch("/{quotation_id}", response_model=QuotationRead)
async def update_quotation(quotation_id: uuid.UUID, payload: QuotationUpdate, db: AsyncSession = Depends(get_db)):
    quotation = await quotation_crud.update_quotation(db, quotation_id, payload)
    if quotation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    return quotation


@router.patch("/{quotation_id}/submit", response_model=QuotationRead)
async def submit_quotation(quotation_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    quotation = await quotation_crud.submit_quotation(db, quotation_id)
    if quotation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quotation not found")
    return quotation


@comparison_router.get("/{rfq_id}/quotations", response_model=RFQQuotationComparison)
async def compare_rfq_quotations(
    rfq_id: uuid.UUID,
    sort_by: Literal["price", "delivery"] = Query(default="price"),
    order: Literal["asc", "desc"] = Query(default="asc"),
    db: AsyncSession = Depends(get_db),
):
    comparison = await quotation_crud.compare_rfq_quotations(db, rfq_id, sort_by, order)
    if comparison is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    return comparison
