""" This is the entry point of the GCRental application """

import logging
import os
from services.auth_service import AuthService
from services.vehicle_service import VehicleService
from services.bookings_service import BookingService
from database.sqlite_db_handler import SQLiteDBHandler
from database.schema import SchemaHandler
from cui.main_cui import MainCUI
from configs.app_constants import DB_FILE_NAME
from repositories.user_repository import UserRepo
from repositories.vehicle_repository import VehicleRepository
from repositories.bookings_repository import BookingsRepository

def main():
    """main script"""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("GCRental App Launched Successfully!!!")

    # if os.path.exists(DB_FILE_NAME):
    #     os.remove(DB_FILE_NAME)

    db = SQLiteDBHandler(DB_FILE_NAME)
    db.connect()
    SchemaHandler.initialise(db)

    auth = AuthService(UserRepo(db))
    vehicle_service = VehicleService(VehicleRepository(db))
    bookings_service = BookingService(BookingsRepository(db))
    
    main_cui = MainCUI(
        auth_service=auth,
        vehicle_service=vehicle_service,
        booking_service=bookings_service
    )
    main_cui.show_home_screen()

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('gc_app.log', mode='w')
        ]
    )

if __name__ == "__main__":
    main()
