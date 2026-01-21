"""Vehicle Entity"""

class Vehicle:
    """Represents a vehicle entity in the car rental system"""

    def __init__(
        self,
        plate_number: str,
        make: str,
        model: str,
        year: int,
        mileage: int,
        daily_rate: float,
        min_rent_period: int,
        max_rent_period: int,
        vehicle_id: int = None
    ):
        self.__vehicle_id = vehicle_id
        self.__plate_number = plate_number
        self.__make = make
        self.__model = model
        self.__year = year
        self.__mileage = mileage
        self.__daily_rate = daily_rate
        self.__min_rent_period = min_rent_period
        self.__max_rent_period = max_rent_period

    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @property
    def plate_number(self):
        return self.__plate_number

    @property
    def make(self):
        return self.__make

    @property
    def model(self):
        return self.__model

    @property
    def year(self):
        return self.__year

    @property
    def mileage(self):
        return self.__mileage
 
    @property
    def daily_rate(self):
        return self.__daily_rate

    @property
    def min_rent_period(self):
        return self.__min_rent_period

    @property
    def max_rent_period(self):
        return self.__max_rent_period
    
    @classmethod
    def from_row(cls, row):
        return Vehicle(
            plate_number=row["plate_number"],
            make=row["make"],
            model=row["model"],
            year=row["year"],
            mileage=row["mileage"],
            daily_rate=row["daily_rate"],
            min_rent_period=row["min_rent_period"],
            max_rent_period=row["max_rent_period"],
            vehicle_id=row["id"]
        )
