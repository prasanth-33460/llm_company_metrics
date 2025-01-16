from datetime import datetime, timedelta

class DateUtils:
    """
    Utility class for handling date-related operations.
    """

    @staticmethod
    def get_default_dates():
        """
        Returns the default start and end dates.
        """
        today = datetime.now()
        one_year_ago = today - timedelta(days=365)
        return one_year_ago.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
