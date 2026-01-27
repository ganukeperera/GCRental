
from datetime import date
from decimal import Decimal
from typing import Optional


class Booking:
    """Represents a Booking entity in the car rental system"""

    def __init__(
        self,
        user_id: int,
        vehicle_id: int,
        start_date: date,
        end_date: date,
        status: str = "pending",
        total_cost: Optional[Decimal] = None,
        booking_id: Optional[int] = None
    ):
        self.__id = booking_id
        self.__user_id = user_id
        self.__vehicle_id = vehicle_id
        self.__start_date = start_date
        self.__end_date = end_date
        self.__status = status
        self.__total_cost = total_cost

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def user_id(self):
        return self.__user_id

    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @property
    def start_date(self):
        return self.__start_date

    @property
    def end_date(self):
        return self.__end_date

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def total_cost(self):
        return self.__total_cost
    
    @total_cost.setter
    def total_cost(self, value):
        self.__total_cost = value

