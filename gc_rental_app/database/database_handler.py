"""Interface for DB handlers"""

from abc import ABC, abstractmethod

class DatabaseHandler(ABC):
    """Abstract base class for DB handlers"""

    _instance = None
    _connection = None

    @abstractmethod
    def connect(self):
        """Abstract Method: Establish the database connection"""

    @abstractmethod
    def close(self):
        """Abstract Method: Close the database connection"""

    @abstractmethod
    def execute(self, sql, params=()):
        """Abstract Method: Execute given sql statement"""

    def execute_many(self, sql, params=()):
        """Abstract Method: Execute more than one sql statements with given parameter array"""

    def execute_and_fetch_one(self, sql, params=()):
        """Abstract Method: Execute sql statement and returns one record"""

    def execute_and_fetch_all(self, sql, params=()):
        """Abstract Method: Execute sql statement and returns all records found"""
