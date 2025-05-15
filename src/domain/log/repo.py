from src.database.mongodb import get_database
from typing import List
from datetime import date, datetime
from src.domain.log.model import AppLog
from bson import ObjectId

class LogRepository:
    @staticmethod
    async def create_logs(user_id: str, date_val: date, logs: List[AppLog]):
        db = get_database()
        log_docs = [
            {
                "user_id": user_id,
                "date": datetime.combine(date_val, datetime.min.time()),  # ← 여기!
                "app_package": log.app_package,
                "total_minutes": log.total_minutes,
                "notification_shown": log.notification_shown,
                "notification_accepted": log.notification_accepted,
                "location_zone": log.location_zone,
                "is_overuse": log.is_overuse
            } for log in logs
        ]
        await db["logs"].insert_many(log_docs)

    @staticmethod
    async def get_logs_by_user(user_id: str):
        db = get_database()
        cursor = db["logs"].find({"user_id": user_id})
        results = await cursor.to_list(length=None)

        for doc in results:
            if "_id" in doc and isinstance(doc["_id"], ObjectId):
                doc["_id"] = str(doc["_id"])

        return results
    
    @staticmethod
    async def delete_log_by_date(user_id: str, log_date: date):
        db = get_database()
        mongo_date = datetime.combine(log_date, datetime.min.time())

        result = await db["logs"].delete_many({
            "user_id": user_id,
            "date": mongo_date
        })
        return result.deleted_count > 0

    @staticmethod
    async def update_log_by_date(user_id: str, log_date: date, logs: List[AppLog]):
        db = get_database()
        mongo_date = datetime.combine(log_date, datetime.min.time())


        await db["logs"].delete_many({"user_id": user_id, "date": mongo_date})
        await LogRepository.create_logs(user_id, mongo_date, logs)

    @staticmethod
    async def get_logs_in_range(user_id: str, start: date, end: date):
        db = get_database()
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end, datetime.min.time())
        cursor = db["logs"].find({
            "user_id": user_id,
            "date": {"$gte": start_dt, "$lt": end_dt}
        })
        results = await cursor.to_list(length=None)
        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
        return results