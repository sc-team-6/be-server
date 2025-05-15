from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from datetime import date
from src.domain.log.service import LogService
from src.domain.log.dto import LogCreateRequest, LogResponse
from src.domain.log.model import AppLog
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.post("/", response_model=LogResponse)
async def create_logs(
    request: LogCreateRequest,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    logs = [AppLog(user_id=current_user["user_id"], date=request.date, **log.dict()) for log in request.logs]
    await LogService.save_logs(current_user["user_id"], request.date, logs)
    return {"status": "ok", "message": "로그 저장 완료"}

@router.get("/", response_model=list[dict])
async def get_logs(current_user: Annotated[dict, Depends(get_current_user)]):
    return await LogService.get_logs(current_user["user_id"])

@router.delete("/{log_date}", response_model=LogResponse)
async def delete_logs(
    log_date: date,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    deleted = await LogService.delete_logs(current_user["user_id"], log_date)
    if not deleted:
        raise HTTPException(status_code=404, detail="로그가 존재하지 않습니다.")
    return {"status": "ok", "message": "로그 삭제 완료"}

@router.put("/{log_date}", response_model=LogResponse)
async def update_logs(
    log_date: date,
    request: LogCreateRequest,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    logs = [AppLog(user_id=current_user["user_id"], date=log_date, **log.dict()) for log in request.logs]
    await LogService.update_logs(current_user["user_id"], log_date, logs)
    return {"status": "ok", "message": "로그 수정 완료"}