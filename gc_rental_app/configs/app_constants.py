"""This file contains constants used use for the app"""

from enum import Enum

# Application
APP_NAME = "GC Rentals"
APP_VERSION = "1.0.0"

# Database
DB_FILE_NAME = "gc_rentals.db"

# Input Rules
MIN_USERNAME_LENGTH = 3
USER_NAME_POLICY_STRING = f"Minimum length of the username is {MIN_USERNAME_LENGTH}"
MIN_PASSWORD_LENGTH = 4
PASSWORD_POLICY_STRING = f"Minimum length of the password is {MIN_PASSWORD_LENGTH}"

class UserRole(Enum):
    """Define the enum for the user roles"""
    SUPER_ADMIN = 0
    ADMIN = 1
    USER = 2

class BookingStatus(Enum):
    """Define the enum for the booking statuses"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
