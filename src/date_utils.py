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
        
        if "last quarter" in date_str.lower():
            quarter_start = (today.month - 1) // 3 * 3 - 2
            start_date = today.replace(month=quarter_start, day=1)
            end_date = start_date.replace(month=start_date.month + 3, day=1) - timedelta(days=1)
            return start_date.isoformat(), end_date.isoformat()
        
        elif "previous month" in date_str.lower():
            first_of_last_month = today.replace(day=1) - timedelta(days=1)
            last_month_start = first_of_last_month.replace(day=1)
            return last_month_start.isoformat(), first_of_last_month.isoformat()
        
        return today.isoformat(), today.isoformat()