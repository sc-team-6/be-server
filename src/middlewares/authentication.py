from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.auth.jwt_handler import SECRET_KEY, ALGORITHM, is_token_blacklisted
import jwt

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 인증이 필요 없는 경로는 통과
        public_paths = ["/api/health", "/api/user/login", "/api/user/register", "/docs", "/openapi.json"]
        if request.url.path in public_paths:
            return await call_next(request)
        
        # Authorization 헤더에서 토큰 추출
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "토큰이 필요합니다."})
        
        token = token.split(" ")[1]

        # 블랙리스트 확인
        if await is_token_blacklisted(token):
            return JSONResponse(status_code=401, content={"detail": "블랙리스트 토큰입니다."})

        # 토큰 유효성 검사
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user_id = payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "토큰이 만료되었습니다."})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "유효하지 않은 토큰입니다."})

        return await call_next(request)