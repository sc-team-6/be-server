from src.database.mongodb import get_database
from src.domain.user.model import User
from bson import ObjectId

class UserRepository:
    @staticmethod
    async def find_by_email(email: str):
        db = get_database()
        return await db["users"].find_one({"email": email})
    
    @staticmethod
    async def create_user(user: User):
        db = get_database()
        user_dict = user.dict()
        
        result = await db["users"].insert_one(user_dict)
        return str(result.inserted_id)
    
    @staticmethod
    async def update_user_settings(user_id: str, settings: dict):
        db = get_database()
        await db["users"].update_one(
            {"_id": user_id},
            {"$set": settings}
        )

    @staticmethod
    async def get_user_settings(user_id: str):
        db = get_database()
        user = await db["users"].find_one({"_id": user_id}, {"settings": 1})
        return user.get("settings", {}) if user else {}