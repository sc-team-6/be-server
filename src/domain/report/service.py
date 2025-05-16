from src.domain.report.repo import ReportRepository
from src.domain.log.repo import LogRepository
from datetime import datetime, timedelta, date
from fastapi import HTTPException
import random
from collections import Counter, defaultdict

class ReportService:
    @staticmethod
    async def get_latest(user_id: str):
        return await ReportRepository.get_latest_report(user_id)

    @staticmethod
    async def get_by_week(user_id: str, week: str):
        return await ReportRepository.get_report_by_week(user_id, week)

    @staticmethod
    async def get_summaries(user_id: str):
        return await ReportRepository.get_report_summaries(user_id)

    @staticmethod
    async def generate_report_by_week(user_id: str, week: str):
        # week = "2025-W15" 형식이어야 함
        try:
            week = week.strip()
            if not week.startswith("20") or "-W" not in week:
                raise ValueError()
            iso_year, iso_week = map(int, week.replace("-W", "-").split("-"))
            start_date = datetime.fromisocalendar(iso_year, iso_week, 1).date()  # 월요일
            end_date = start_date + timedelta(days=6)  # 일요일
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"주차 형식이 올바르지 않습니다. 예: 2025-W15 (입력값: '{week}')"
            )
        logs = await ReportRepository.get_logs_in_range(user_id, start_date, end_date)
        if not logs:
            raise HTTPException(status_code=404, detail="해당 기간에 로그 데이터가 없습니다.")

        total_minutes = sum(log["total_minutes"] for log in logs)
        scroll_meters = total_minutes * 0.6
        alerts_total = sum(1 for log in logs if log["is_overuse"])
        alert_days = len(set(
            log["date"].date() if isinstance(log["date"], datetime) else log["date"]
            for log in logs if log["is_overuse"]
        ))

        warn_count = Counter(log["app_package"] for log in logs if log["is_overuse"])
        most_warned_app = warn_count.most_common(1)[0][0] if warn_count else None

        weekday_map = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekday_count = Counter(
            (
                log["date"].weekday()
                if isinstance(log["date"], datetime) else
                datetime.fromisoformat(log["date"]).weekday()
            )
            for log in logs if log["is_overuse"]
        )
        most_difficult_day = weekday_map[weekday_count.most_common(1)[0][0]] if weekday_count else None

        app_minutes = defaultdict(int)
        for log in logs:
            app_minutes[log["app_package"]] += log["total_minutes"]
        top_used_app = max(app_minutes, key=app_minutes.get) if app_minutes else None

        summary = (
            f"This week, you spent a total of {total_minutes} minutes, with an estimated scroll distance of {round(scroll_meters, 1)} meters. "
            f"Overuse alerts were triggered on {alert_days} day(s), mainly due to '{most_warned_app}'. "
            f"'{most_difficult_day}' was your most challenging day, and '{top_used_app}' was your most used app. "
            "Consider managing your screen time more consciously next week."
        )

        report = {
            "user_id": user_id,
            "week": week,
            "overrun_threshold": 80,
            "overrun_days": alert_days,
            "most_warned_app": most_warned_app,
            "scroll_distance_m": round(scroll_meters, 1),
            "goal_achieved": alerts_total <= 3,
            "summary": summary,
            "most_difficult_day": most_difficult_day,
            "alerts_total": alerts_total,
            "top_used_app": top_used_app
        }

        return await ReportRepository.insert_report(report)
    