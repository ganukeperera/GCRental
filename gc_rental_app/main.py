""" This is the entry point of the GCRental application """

import logging
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

    db = SQLiteDBHandler(DB_FILE_NAME)
    db.connect()
    SchemaHandler.initialise(db)

    auth_service = AuthService(UserRepo(db))
    vehicle_repo = VehicleRepository(db)
    booking_repo = BookingsRepository(db)
    vehicle_service = VehicleService(vehicle_repo, booking_repo)
    bookings_service = BookingService(booking_repo, vehicle_repo)
    
    main_cui = MainCUI(
        auth_service=auth_service,
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
