from motor.motor_asyncio import AsyncIOMotorClient
import src.core.config as config
import logging
import pymongo

__all__ = ["get_connection", "get_database"]

logger = logging.getLogger(__name__)

class MongoDataBase:
    client: AsyncIOMotorClient = None
    db_instance = None  # ✅ 데이터베이스 인스턴스 추가

db = MongoDataBase()

def get_connection() -> AsyncIOMotorClient:
    return db.client

def get_database():
    return db.db_instance  # ✅ 데이터베이스 반환

async def connect_mongo(
    connect_string: str, db_name: str = "my_database", max_pool_size: int = 10, min_pool_size: int = 1
):
    if not connect_string:
        raise Exception("❌ MongoDB 연결 문자열이 없습니다.")
    
    logger.info("✅ MongoDB 연결 중...")
    db.client = AsyncIOMotorClient(
        connect_string, maxPoolSize=max_pool_size, minPoolSize=min_pool_size
    )
    
    # ✅ 연결 시 데이터베이스 인스턴스 설정
    db.db_instance = db.client[db_name]
    
    # 연결 상태 확인 (ping)
    try:
        await db.client.admin.command("ping")
        logger.info("✅ MongoDB 연결 성공!")
    except pymongo.errors.PyMongoError as e:
        logger.error(f"❌ MongoDB 연결 실패: {e}")
        raise

async def disconnect_mongo():
    if db.client:
        await db.client.close()
        logger.info("❌ MongoDB 연결 해제 완료!")