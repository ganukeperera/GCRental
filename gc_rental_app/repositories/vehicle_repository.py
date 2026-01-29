"""Vehicle Repository"""

import logging
from datetime import date
from database.database_handler import DatabaseHandler
from .entities.vehicle import Vehicle

logger = logging.getLogger(__name__)

class VehicleRepository:
    """Methods related to vehicle repo"""
    def __init__(self, db: DatabaseHandler):
        self.__db = db

    def add(self, vehicle: Vehicle):
        """Add vehicle to the table"""
        sql = """
        INSERT INTO vehicles (
            plate_number, make, model, year,
            mileage, daily_rate,
            min_rent_period, max_rent_period
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            vehicle.plate_number,
            vehicle.make,
            vehicle.model,
            vehicle.year,
            vehicle.mileage,
            vehicle.daily_rate,
            vehicle.min_rent_period,
            vehicle.max_rent_period
        )
        self.__db.execute(sql, params)

    def update(self, vehicle: Vehicle):
        """Update vehicle"""
        logger.debug("Update vehicle get called with: %s", vehicle.vehicle_id)
        sql = """
            UPDATE vehicles
            SET plate_number = ?, make = ?, model = ?, year = ?,
                mileage = ?, daily_rate = ?,
                min_rent_period = ?, max_rent_period = ?
            WHERE id = ?
            """
        params = (
            vehicle.plate_number,
            vehicle.make,
            vehicle.model,
            vehicle.year,
            vehicle.mileage,
            vehicle.daily_rate,
            vehicle.min_rent_period,
            vehicle.max_rent_period,
            vehicle.vehicle_id
        )
        self.__db.execute(sql, params)

    def remove(self, vehicle_id):
        """Delete record from vehicle table"""
        sql = "DELETE FROM vehicles WHERE id = ?"
        self.__db.execute(sql, (vehicle_id,))

    def get_all(self):
        """Get all vehicles"""
        cursor = self.__db.execute("SELECT * FROM vehicles")
        rows = cursor.fetchall()
        return [Vehicle.from_row(row) for row in rows]

    def get_by_id(self, vehicle_id):
        """Search vehicle using id"""
        cursor = self.__db.execute(
                "SELECT * FROM vehicles WHERE id = ?",
                (vehicle_id,)
            )
        row = cursor.fetchone()
        return Vehicle.from_row(row) if row else None

    def get_by_plate(self, plate_number):
        """Search vehicle by plate number"""
        cursor = self.__db.execute(
                "SELECT * FROM vehicles WHERE plate_number = ?",
                (plate_number,)
            )
        row = cursor.fetchone()
        return Vehicle.from_row(row) if row else None
    
    def update_vehicle_mileage(self, vehicle_id: int, new_mileage: int):
        """Repo method to update the mileage for given vehicles"""
        
        sql = """
        UPDATE vehicles
        SET mileage = ?
        WHERE id = ?
        """
        self.__db.execute(sql, (new_mileage, vehicle_id))
        

