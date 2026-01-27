"""Schema initializer"""

import logging
from .sqlite_db_handler import DatabaseHandler
from configs.app_constants import UserRole

class SchemaHandler:
    """This class suppose to create necessary tables in the empty db"""

    logger = logging.getLogger(__name__)

    USER_TABLE_SCHEMA = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
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
            user_id INTEGER,
            vehicle_id INTEGER,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected', 'completed')),
            total_cost DECIMAL(10, 2),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE SET NULL
        )
    """

    @classmethod
    def initialise(cls, db: DatabaseHandler):
        """Create tables"""
        db.execute(cls.USER_TABLE_SCHEMA)
        db.execute(cls.VEHICLE_TABLE_SCHEMA)
        db.execute(cls.BOOKING_TABLE_SCHEMA)
        cls.__seed_super_admin(db)

    @classmethod
    def drop_all_tables(cls, db: DatabaseHandler):
        """Drop all tables"""
        db.execute("DROP TABLE IF EXISTS users")
        db.execute("DROP TABLE IF EXISTS vehicles")
        db.execute("DROP TABLE IF EXISTS bookings")

    @classmethod
    def __seed_super_admin(cls, db: DatabaseHandler):

        exists = db.execute_and_fetch_one(
        "SELECT COUNT(*) FROM users WHERE role = ?",
        (UserRole.SUPER_ADMIN.value,)
        )

        if not exists:
            db.execute(
            "INSERT INTO users (fullname, username, password, role) VALUES (?, ?, ?, ?)", ("superadmin", "superadmin", "$2b$12$RDUIHEl327lBsoWJbLaLE.bi.FulZ3Z7wrv8F4FVbnlxHVd5uhoU2", UserRole.SUPER_ADMIN.value) ) 
