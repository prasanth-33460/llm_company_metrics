from datetime import datetime, timedelta

class DateUtils:
    @staticmethod
    def get_default_dates():
        end_date = datetime.today()
        start_date = end_date - timedelta(days=365)
        return start_date.isoformat(), end_date.isoformat()

    @staticmethod
    def parse_relative_date(date_str):
        today = datetime.today()

        try:
            date_str = date_str.lower()

            if "today" in date_str:
                return today.isoformat(), today.isoformat()

            elif "yesterday" in date_str:
                yesterday = today - timedelta(days=1)
                return yesterday.isoformat(), yesterday.isoformat()

            elif "this week" in date_str:
                start_date = today - timedelta(days=today.weekday())
                return start_date.isoformat(), today.isoformat()

            elif "last week" in date_str:
                start_date = today - timedelta(days=today.weekday() + 7)
                end_date = start_date + timedelta(days=6)
                return start_date.isoformat(), end_date.isoformat()

            elif "this month" in date_str:
                start_date = today.replace(day=1)
                return start_date.isoformat(), today.isoformat()

            elif "previous month" in date_str:
                first_of_this_month = today.replace(day=1)
                last_month_end = first_of_this_month - timedelta(days=1)
                last_month_start = last_month_end.replace(day=1)
                return last_month_start.isoformat(), last_month_end.isoformat()

            elif "last 3 months" in date_str or "three months" in date_str:
                start_date = today - timedelta(days=90)
                return start_date.isoformat(), today.isoformat()

            elif "last 6 months" in date_str or "six months" in date_str:
                start_date = today - timedelta(days=180)
                return start_date.isoformat(), today.isoformat()

            elif "this year" in date_str:
                start_date = today.replace(month=1, day=1)
                return start_date.isoformat(), today.isoformat()

            elif "last year" in date_str:
                start_date = today.replace(year=today.year - 1, month=1, day=1)
                end_date = start_date.replace(year=today.year - 1, month=12, day=31)
                return start_date.isoformat(), end_date.isoformat()

            elif "last quarter" in date_str:
                current_month = today.month
                quarter = (current_month - 1) // 3 + 1
                quarter_start_month = (quarter - 1) * 3 - 2

                if quarter_start_month <= 0:
                    quarter_start_month += 12
                    year = today.year - 1
                else:
                    year = today.year

                start_date = today.replace(year=year, month=quarter_start_month, day=1)
                end_date = start_date.replace(month=start_date.month + 3, day=1) - timedelta(days=1)
                return start_date.isoformat(), end_date.isoformat()

            elif "last 7 days" in date_str or "past week" in date_str:
                start_date = today - timedelta(days=7)
                return start_date.isoformat(), today.isoformat()

            elif "last 30 days" in date_str or "past month" in date_str:
                start_date = today - timedelta(days=30)
                return start_date.isoformat(), today.isoformat()

            elif "last 90 days" in date_str or "past three months" in date_str:
                start_date = today - timedelta(days=90)
                return start_date.isoformat(), today.isoformat()

            elif "all time" in date_str or "since the beginning" in date_str:
                start_date = datetime(1970, 1, 1)
                return start_date.isoformat(), today.isoformat()

            else:
                return today.isoformat(), today.isoformat()

        except Exception as e:
            print(f"Error parsing relative date: {e}")
            return today.isoformat(), today.isoformat()