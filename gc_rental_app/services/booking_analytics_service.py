"""BookingAnalythicsService"""

from datetime import datetime, timedelta, date
import pandas as pd
from repositories.bookings_repository import BookingsRepository

class BookingAnalyticsService:
    """This class suppose to process booking data using pandas"""

    def __init__(self, booking_repository: BookingsRepository):
        self._booking_repository = booking_repository

    def _build_dataframe(self):
        # Load all booking records in the table
        bookings = self._booking_repository.get_all()

        # Define the data frame to be used within the analytics service
        df = pd.DataFrame([{
            "user_id": b.user_id,
            "vehicle_id": b.vehicle_id,
            "start_date": b.start_date,
            "end_date": b.end_date,
            "total_cost": b.total_cost
        } for b in bookings])

        if not df.empty:
            df["start_date"] = pd.to_datetime(df["start_date"])

        return df

    # 
    def calculate_demand_factor(self,
                                vehicle_id: str,
                                start_date: date,
                                window_days: int = 30
                                ) -> float:
        """
        This function used to dynamically calculate the daily rate of
        the given vehicle based on the demand within the given period.
        Higher booking period will increase the pricing multiplier dynamically
        """
        df = self._build_dataframe()
        if df.empty:
            return 1.0
        
        # Ensure new_start_date is datetime
        if isinstance(start_date, datetime):
            booking_start = start_date
        else:
            booking_start = datetime.combine(start_date, datetime.min.time())
        
        # Define demand window (default last 7 days)
        delta = timedelta(days=window_days)
        window_start = booking_start - delta
        window_end = booking_start + delta

        recent_bookings = df[
            (df["vehicle_id"] == vehicle_id) &
            (df["start_date"] >= window_start) &
            (df["start_date"] < window_end)
        ]

        count = len(recent_bookings)

        if count >= 5:
            return 1.2
        elif count >= 3:
            return 1.1
        else:
            return 1.0
