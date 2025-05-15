import redis.asyncio as aioredis
import logging

logger = logging.getLogger(__name__)

class RedisDatabase:
    client: aioredis.Redis = None

db = RedisDatabase()

async def connect_redis(connect_string: str):
    try:
        if not connect_string:
            raise ValueError("Redis 연결 문자열이 없습니다.")
        
        logger.info("✅ Redis 연결 중...")
        db.client = aioredis.from_url(connect_string, decode_responses=True)
        await db.client.ping()  # ✅ 연결 확인
        logger.info("✅ Redis 연결 완료!")
        
    except Exception as e:
        logger.error(f"❌ Redis 연결 실패: {e}")

async def disconnect_redis():
    if db.client:
        await db.client.close()
        logger.info("❌ Redis 연결 해제 완료!")
        
# ✅ Redis 연결 객체 반환 함수
def get_connection() -> aioredis.Redis:
    if db.client is None:
        logger.error("❌ Redis가 연결되지 않았습니다.")
    return db.client