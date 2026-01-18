"""Schema initializer"""

import logging
from .sqlite_db_handler import DatabaseHandler

class SchemaHandler:
    """This class suppose to create necessary tables in the empty db"""

    logger = logging.getLogger(__name__)

    USER_TABLE_SCHEMA = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            mobile VARCHAR(15),
            role INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    VEHICLE_TABLE_SCHEMA = """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT UNIQUE NOT NULL,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            mileage INTEGER,
            daily_rate DECIMAL(10, 2) NOT NULL,
            min_rent_period INTEGER NOT NULL,
            max_rent_period INTEGER NOT NULL
        )
    """

    BOOKING_TABLE_SCHEMA = """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            vehicle_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'confirmed', 'cancelled', 'completed')),
            total_cost DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        )
    """

    @classmethod
    def initialise(cls, db: DatabaseHandler):
        """Create tables"""
        db.execute(cls.USER_TABLE_SCHEMA)
        db.execute(cls.VEHICLE_TABLE_SCHEMA)
        db.execute(cls.BOOKING_TABLE_SCHEMA)

    @classmethod
    def drop_all_tables(cls, db: DatabaseHandler):
        """Drop all tables"""
        db.execute("DROP TABLE IF EXISTS users")
        db.execute("DROP TABLE IF EXISTS vehicles")
        db.execute("DROP TABLE IF EXISTS bookings")
