import jwt
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from src.database.redis import get_connection
from dotenv import load_dotenv

# .env 로드
load_dotenv()

# ✅ 환경변수 설정
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ access_token 생성
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ refresh_token 생성
def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ 토큰 블랙리스트에 등록
async def blacklist_token(token: str):
    redis = await get_connection()
    await redis.setex(f"blacklist:{token}", ACCESS_TOKEN_EXPIRE_MINUTES * 60, "true")

# ✅ 토큰 블랙리스트 여부 확인
async def is_token_blacklisted(token: str):
    redis = await get_connection()
    return await redis.exists(f"blacklist:{token}")