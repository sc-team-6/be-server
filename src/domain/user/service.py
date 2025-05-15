from src.domain.user.repo import UserRepository
from src.auth.jwt_handler import hash_password, verify_password
from src.database.redis import get_connection
from src.domain.user.model import User
from src.core.exceptions import (
    DataConflictError,
    DataNotFoundError,
    DatabaseConnectionError
)

class UserService:
    @staticmethod
    async def register_user(email: str, username: str, password: str):
        redis = get_connection()
        if not redis:
            raise DatabaseConnectionError("Redis 연결이 필요합니다.")

        # ✅ Redis에 이메일이 캐시되어 있는지 확인
        cached_user = await redis.get(f"user:{email}")
        if cached_user:
            raise DataConflictError("이미 존재하는 이메일입니다.")

        # ✅ MongoDB에 이메일 중복 확인
        existing_user = await UserRepository.find_by_email(email)
        if existing_user:
            await redis.set(f"user:{email}", "exists", ex=300)  # 5분 캐시
            raise DataConflictError("이미 존재하는 이메일입니다.")

        # ✅ 비밀번호 해싱 및 유저 생성
        hashed_pw = hash_password(password)
        user = User(email=email, username=username, hashed_password=hashed_pw)
        return await UserRepository.create_user(user)

    @staticmethod
    async def login_user(email: str, password: str):
        user = await UserRepository.find_by_email(email)
        if not user:
            raise DataNotFoundError("존재하지 않는 이메일입니다.")

        if not verify_password(password, user['hashed_password']):
            raise DataConflictError("잘못된 이메일 또는 비밀번호입니다.")

        return user
    
    @staticmethod
    async def update_settings(user_id: str, settings: dict):
        return await UserRepository.update_user_settings(user_id, settings)

    @staticmethod
    async def get_settings(user_id: str):
        return await UserRepository.get_user_settings(user_id)
