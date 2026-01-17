"""Authentication and User based things"""

import logging
from abc import ABC, abstractmethod
from database.database_handler import DatabaseHandler
from configs.app_constants import UserRole

logger = logging.getLogger(__name__)

class User(ABC):
    """The base class for all the user types"""
    def __init__(self, username: str):
        self._username = username

    @abstractmethod
    def get_menu(self):
        """this returns the CUI menu for the given user"""

class Admin(User):
    """User with administrative privilege"""

    def get_menu(self):
        """this returns the CUI menu for the given user"""

        return [
            "1. Add Vehicle",
            "2. Delete Vehicle",
            "3. View All Bookings",
            "4. Logout"
        ]

class Customer(User):
    """User who access the system for booking"""

    def get_menu(self):
        return [
            "1. View Vehicles",
            "2. Book Vehicle",
            "3. Logout"
        ]

class AuthService:
    def __init__(self, db: DatabaseHandler):
        self.db = db

    def register(self, fullname, username, password, mobile, role):
        try:
            self.db.execute(
                "INSERT INTO users (fullname,username, password, mobile, role) VALUES (?, ?, ?, ?, ?)",
                (fullname, username, password, mobile, role)
            )
            logger.info("User %s registered successfully", fullname)
        except Exception as e:
            print("Error has occurred while registering")
            logger.error("Error occurred while registering user %s, error: %s", fullname, e)
            raise 

    def login(self, username, password):
        cursor = self.db.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = cursor.fetchone()

        if not result:
            print("Invalid credentials")
            return None

        role = int(result[0])
        if role == UserRole.ADMIN.value:
            return Admin(username)
        else:
            return Customer(username)
