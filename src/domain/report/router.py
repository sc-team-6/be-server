from fastapi import APIRouter, Depends, Path
from typing import List
from datetime import date
from src.dependencies.auth import get_current_user
from src.domain.report.service import ReportService
from src.domain.report.dto import WeeklyReportDTO, WeeklyReportSummaryDTO
from typing import Annotated
from fastapi import Query

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/latest", response_model=WeeklyReportDTO)
async def get_latest_report(current_user: Annotated[dict, Depends(get_current_user)]):
    return await ReportService.get_latest(current_user["user_id"])

@router.get("/summary", response_model=List[WeeklyReportSummaryDTO])
async def get_report_summaries(current_user: Annotated[dict, Depends(get_current_user)]):
    return await ReportService.get_summaries(current_user["user_id"])

@router.get("/{week}", response_model=WeeklyReportDTO)
async def get_report_by_week(
    current_user: Annotated[dict, Depends(get_current_user)],
    week: str = Path(..., description="분석 주차 (예: 2025-W15)")
):
    return await ReportService.get_by_week(current_user["user_id"], week)
@router.post("/generate", response_model=WeeklyReportDTO)
async def generate_report(
    current_user: Annotated[dict, Depends(get_current_user)],
    week: str = Query(..., description="분석 주차 (예: 2025-W15)")
):
    return await ReportService.generate_report_by_week(
        user_id=current_user["user_id"],
        week=week
    )