from fastapi import FastAPI, APIRouter, Depends
from src.middlewares.authentication import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from src.middlewares.exception_handler import register_exception_handlers
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from src.domain.user.router import router as user_router
from src.domain.log.router import router as log_router
from src.domain.report.router import router as report_router
from src.database.mongodb import connect_mongo, disconnect_mongo
from src.database.redis import connect_redis, disconnect_redis
from dotenv import load_dotenv
import os
import logging
import logging.config

# 환경변수 로드
load_dotenv(dotenv_path=f".{os.getenv('DOT_ENV', 'test')}.env")

# 로깅 설정
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
def create_app() -> FastAPI:
    app = FastAPI()
    return app

app = create_app()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)
register_exception_handlers(app)

bearer_scheme = HTTPBearer()

# Swagger UI에 보안 스키마 추가
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="FastAPI Project",
        version="1.0.0",
        description="FastAPI with JWT Authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # 전체 API에 보안 스키마 적용
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



# 라우터 연결
app.include_router(user_router, prefix="/api")
app.include_router(log_router, prefix='/api')
app.include_router(report_router, prefix='/api')


# 앱 시작 시 MongoDB, Redis 연결
@app.on_event("startup")
async def on_app_start():
    mongo_conn_url = os.getenv("MONGO_CONNECTION_URL")
    redis_conn_url = os.getenv("REDIS_CONNECTION_URL")

    if mongo_conn_url:
        logger.info("Connecting to MongoDB...")
        await connect_mongo(mongo_conn_url)
        logger.info("Connected to MongoDB!")

    if redis_conn_url:
        logger.info("Connecting to Redis...")
        await connect_redis(redis_conn_url)
        logger.info("Connected to Redis!")

# 앱 종료 시 MongoDB, Redis 연결 해제
@app.on_event("shutdown")
async def on_app_shutdown():
    logger.info("Disconnecting MongoDB and Redis...")
    await disconnect_mongo()
    await disconnect_redis()
    logger.info("Disconnected MongoDB and Redis!")

# 테스트용
@app.get("/api/health")
async def health_check():
    return {"message": "FastAPI와 연결되었습니다!"}

### For further application

from typing import Annotated
from random import randint
from src.dependencies.auth import get_current_user

# rank (for further application)
@app.get("/api/rank")
async def get_user_rank(current_user: Annotated[dict, Depends(get_current_user)]):
    percentile = randint(20, 80)
    return {
        "user_id": current_user["user_id"],
        "rank_percentile": percentile
    }