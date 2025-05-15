import os
import jwt
import logging
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.database.redis import get_connection
from src.core.exceptions import AuthenticationError

# ✅ 환경변수 로드
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# ✅ 보안 및 로깅 설정
security = HTTPBearer()
logger = logging.getLogger(__name__)

# ✅ Access Token 생성
def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Refresh Token 생성
def create_refresh_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"user_id": user_id, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ✅ 현재 유저 정보 추출 (access token 기준)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="❌ 인증 토큰이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        redis = await get_connection()
        if redis:
            is_blacklisted = await redis.get(f"blacklist:{token}")
            if is_blacklisted:
                logger.warning("⛔ 블랙리스트 토큰 차단됨")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="블랙리스트에 등록된 토큰입니다.",
                )

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

        return {"user_id": user_id, "token": token}

    except jwt.ExpiredSignatureError:
        logger.error("⏰ 토큰 만료")
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")

    except jwt.InvalidTokenError:
        logger.error("🚫 유효하지 않은 토큰")
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

# ✅ 토큰 수동 검증 (refresh token 등)
async def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        raise AuthenticationError("유효하지 않은 토큰입니다.")