""" This is the entry point of the GCRental application """

import logging
from services.auth_service import AuthService
from services.vehicle_service import VehicleService
from services.bookings_service import BookingService
from services.booking_analytics_service import BookingAnalyticsService
from database.sqlite_db_handler import SQLiteDBHandler
from database.schema import SchemaHandler
from cui.gc_rental_app import GCRentalApp
from cui.session import Session
from configs.app_constants import DB_FILE_NAME
from repositories.user_repository import UserRepo
from repositories.vehicle_repository import VehicleRepository
from repositories.bookings_repository import BookingsRepository

def main():
    """main script"""

    # Initialize logging mechanism
    setup_logging()
    logger = logging.getLogger(__name__)

    # Initialize the SQLite Database
    db = SQLiteDBHandler(DB_FILE_NAME)
    # Run schemas to create tables
    SchemaHandler.initialise(db)

    # Initialize the Repositories injecting SQLite database handler
    user_repo = UserRepo(db)
    vehicle_repo = VehicleRepository(db)
    booking_repo = BookingsRepository(db)

    # Used dependency injection to initialize service layer with required dependencies
    auth_service = AuthService(user_repo)
    vehicle_service = VehicleService(vehicle_repo)
    analytics_service = BookingAnalyticsService(booking_repo)
    bookings_service = BookingService(booking_repo, vehicle_repo, analytics_service)
    
    # Show Initial Menu
    rental_app = GCRentalApp(
        session= Session(),
        auth_service=auth_service,
        vehicle_service=vehicle_service,
        booking_service=bookings_service
    )
    rental_app.start()
    logger.info("GCRental App Launched Successfully!!!")

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('gc_app.log', mode='w')
        ]
    )

if __name__ == "__main__":
    main()
