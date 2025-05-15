from src.database.mongodb import get_database
from datetime import date
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException

class ReportRepository:
    @staticmethod
    async def get_latest_report(user_id: str):
        db = get_database()
        doc = await db["reports"].find_one({"user_id": user_id}, sort=[("week", -1)])

        if not doc:
            raise HTTPException(status_code=404, detail="리포트가 존재하지 않습니다.")

        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        
        return doc

    @staticmethod
    async def get_report_by_week(user_id: str, week: str):
        db = get_database()
        doc = await db["reports"].find_one({"user_id": user_id, "week": week})
        if not doc:
            raise HTTPException(status_code=404, detail="리포트가 존재하지 않습니다.")
        doc["_id"] = str(doc["_id"])
        return doc

    @staticmethod
    async def get_report_summaries(user_id: str):
        db = get_database()
        cursor = db["reports"].find({"user_id": user_id}, {"week": 1, "summary": 1}).sort("week", -1)
        results = await cursor.to_list(length=None)
        for r in results:
            r["_id"] = str(r["_id"])
        return results
    
    @staticmethod
    async def get_logs_in_range(user_id: str, start: date, end: date):
        db = get_database()

        start_dt = datetime.combine(start, datetime.min.time())  # 00:00:00
        end_dt = datetime.combine(end, datetime.min.time())      # 00:00:00 of next day

        cursor = db["logs"].find({
            "user_id": user_id,
            "date": {"$gte": start_dt, "$lt": end_dt}
        })
        return await cursor.to_list(length=None)

    @staticmethod
    async def insert_report(report: dict):
        db = get_database()
        result = await db["reports"].insert_one(report)
        report["_id"] = str(result.inserted_id)
        return report