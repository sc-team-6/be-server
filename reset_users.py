# reset_users.py
import os
import asyncio
from dotenv import load_dotenv
from src.database.mongodb import connect_mongo, get_database

# ✅ 환경변수 로드
load_dotenv()
MONGO_URL = os.getenv("MONGO_CONNECTION_URL", 'mongodb://root:example@localhost:27017')
DB_NAME = os.getenv("MONGO_DB_NAME", "my_database")  # .env에 설정돼 있다면 반영

async def reset_users():
    if not MONGO_URL:
        raise Exception("❌ MONGO_CONNECTION_URL 환경변수가 없습니다.")
    
    await connect_mongo(MONGO_URL, db_name=DB_NAME)
    db = get_database()

    if db is None:
        raise Exception("❌ MongoDB 연결 실패: db 인스턴스가 None입니다.")
    
    await db["users"].drop()
    print("✅ users 컬렉션 삭제 완료")

if __name__ == "__main__":
    asyncio.run(reset_users())