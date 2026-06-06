from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import analytics as analytics_crud
from app.database import get_db
from app.schemas.analytics import AnalyticsSummary, MonthlyTrend, VendorPerformance
from app.utils.export import generate_procurement_export

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
async def get_summary(db: AsyncSession = Depends(get_db)):
    return await analytics_crud.get_summary(db)


@router.get("/monthly-trend", response_model=list[MonthlyTrend])
async def get_monthly_trend(db: AsyncSession = Depends(get_db)):
    return await analytics_crud.get_monthly_trend(db)


@router.get("/vendor-performance", response_model=list[VendorPerformance])
async def get_vendor_performance(db: AsyncSession = Depends(get_db)):
    return await analytics_crud.get_vendor_performance(db)


@router.get("/export")
async def export_analytics(db: AsyncSession = Depends(get_db)):
    export_path = await generate_procurement_export(db)
    return FileResponse(
        path=export_path,
        filename=export_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
