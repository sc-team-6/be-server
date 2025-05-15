from src.domain.log.repo import LogRepository
from src.domain.log.model import AppLog
from datetime import date
from typing import List

class LogService:
    @staticmethod
    async def save_logs(user_id: str, date: date, logs: List[AppLog]):
        return await LogRepository.create_logs(user_id, date, logs)

    @staticmethod
    async def get_logs(user_id: str):
        return await LogRepository.get_logs_by_user(user_id)

    @staticmethod
    async def delete_logs(user_id: str, log_date: date):
        return await LogRepository.delete_log_by_date(user_id, log_date)

    @staticmethod
    async def update_logs(user_id: str, log_date: date, logs: List[AppLog]):
        return await LogRepository.update_log_by_date(user_id, log_date, logs)

    @staticmethod
    async def get_logs_between(user_id: str, start: date, end: date):
        return await LogRepository.get_logs_in_range(user_id, start, end)