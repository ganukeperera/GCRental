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

    @classmethod
    def initialise(cls, db: DatabaseHandler):
        """Create tables"""
        db.execute(cls.USER_TABLE_SCHEMA)

    @classmethod
    def drop_all_tables(cls, db: DatabaseHandler):
        """Drop all tables"""
        db.execute("DROP TABLE IF EXISTS users")
