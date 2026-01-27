"""SQLite Database Module"""

import sqlite3
import logging
from typing import Optional
from .database_handler import DatabaseHandler

class SQLiteDBHandler(DatabaseHandler):
    """SQLite Database handler"""

    logger = logging.getLogger(__name__)
    _instance: Optional['SQLiteDBHandler'] = None
    _connection: Optional[sqlite3.Connection] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_path):
        """Abstract Method: Init with db path"""
        self.__db_path = db_path
        self._connect()

    def _connect(self):
        """Connect to the sqlite DB"""
        if self._connection is None:
            self._connection = sqlite3.connect(
                self.__db_path,
                timeout = 5.0
            )
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
            SQLiteDBHandler.logger.info("SQLite DB connection done")
        return self._connection

    def close(self):
        """Close the sqlite db connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
            SQLiteDBHandler.logger.info("SQLite DB connection close")

    def execute(self, sql, params=()):
        """Execute an sql statement"""

        try:
            SQLiteDBHandler.logger.debug("Start execution of the SQL command: %s", sql)
            cursor = self._connection.cursor()
            cursor.execute(sql, params)
            self._connection.commit()
            return cursor
        except sqlite3.Error as e:
            SQLiteDBHandler.logger.error("Execution of the SQL command failed: %s, error: %s", sql, e)
            raise

    def execute_many(self, sql, params=()):
        """Execute more than one sql statement with given parameter array"""
        try:
            SQLiteDBHandler.logger.debug("Start execution of the SQL command: %s", sql)
            cursor = self._connection.cursor()
            cursor.executemany(sql, params)
            self._connection.commit()
            return cursor
        except sqlite3.Error as e:
            SQLiteDBHandler.logger.error("Execution of the SQL command failed: %s, error: %s", sql, e)
            raise

    def execute_and_fetch_one(self, sql, params=()):
        """Execute sql statement and returns one record"""
        try:
            SQLiteDBHandler.logger.debug("Start execution of the SQL command: %s", sql)
            cursor = self._connection.cursor()
            result = cursor.execute(sql, params)
            (record,) = result.fetchone()
            return record
        except sqlite3.Error as e:
            SQLiteDBHandler.logger.error("Execution of the SQL command failed: %s, error: %s", sql, e)
            raise

    def execute_and_fetch_all(self, sql, params=()):
        """Execute sql statement and returns all records found"""

        try:
            cursor = self._connection.cursor()
            result = cursor.execute(sql, params)
            return result.fetchall()
        except sqlite3.Error as e:
            SQLiteDBHandler.logger.error("Execution of the SQL command failed: %s, error: %s", sql, e)
            raise
