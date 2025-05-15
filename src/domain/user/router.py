from fastapi import APIRouter, Depends, HTTPException, Body, Request
from src.domain.user.dto import UserRegisterDTO, UserLoginDTO
from src.domain.user.service import UserService
from src.auth.jwt_handler import create_access_token, create_refresh_token, blacklist_token
from src.dependencies.auth import get_current_user
from src.core.exceptions import DataConflictError, DataNotFoundError, ValidationError
from src.dependencies.auth import verify_token
from typing_extensions import Annotated

router = APIRouter(prefix="/user", tags=["User"])

# ✅ 회원가입
@router.post("/register", summary="회원가입")
async def register(user_data: UserRegisterDTO):
    user_id = await UserService.register_user(user_data.email, user_data.username, user_data.password)
    return {"message": "회원가입 성공", "user_id": user_id}

# ✅ 로그인 (access + refresh 토큰 발급)
@router.post("/login", summary="로그인")
async def login(user_data: UserLoginDTO):
    user = await UserService.login_user(user_data.email, user_data.password)
    user_id = str(user["_id"])
    
    access_token = create_access_token({"user_id": user_id})
    refresh_token = create_refresh_token({"user_id": user_id})


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# ✅ 로그아웃 (access_token 블랙리스트 등록)
@router.post("/logout", summary="로그아웃")
async def logout(request: Request, user: dict = Depends(get_current_user)):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise ValidationError("유효하지 않은 토큰입니다.")

    await blacklist_token(token)
    return {"message": "성공적으로 로그아웃되었습니다."}

# ✅ 내 정보 조회
@router.get("/me", summary="내 정보 조회")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

# ✅ refresh_token으로 새 access_token 발급
@router.post("/refresh", summary="access_token 재발급")
async def refresh_token(refresh_token: str = Body(..., embed=True)):
    payload = await verify_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="유효한 refresh_token이 아닙니다.")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id가 없습니다.")

    new_access_token = create_access_token(user_id)
    return {"access_token": new_access_token, "token_type": "bearer"}

# ✅ 유저 설정 조회
@router.get("/settings", summary="유저 설정 조회")
async def get_user_settings(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    return await UserService.get_settings(current_user["user_id"])

# ✅ 유저 설정 업데이트
@router.put("/settings", summary="유저 설정 저장/업데이트")
async def update_user_settings(
    current_user: Annotated[dict, Depends(get_current_user)],  # 먼저
    settings: dict = Body(...)                                 # 나중에
):
    await UserService.update_settings(current_user["user_id"], settings)
    return {"message": "설정이 저장되었습니다."}