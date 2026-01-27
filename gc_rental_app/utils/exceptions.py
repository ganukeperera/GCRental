"""This file contains the custom exceptions defined for the Rental app"""

class GCRentalException(Exception):
    """Base exception for the app"""

class ValidationError(GCRentalException):
    """Validation error"""

class VehicleNotFoundError(GCRentalException):
    """Vehicle not found"""

class UserRegistrationError(GCRentalException):
    """User registration failed"""

class LoginError(GCRentalException):
    """User Login failed"""

class InvalidLogin(GCRentalException):
    """User Login failed"""

class VehicleAlreadyExist(GCRentalException):
    """Vehicle Already exist"""

class VehicleNotFound(GCRentalException):
    """Vehicle Not Found"""

class BookingNotFound(GCRentalException):
    """Booking Not Found"""

class ViolateAllowedRentPeriod(GCRentalException):
    """Rent Min Max Period Violation"""

class UserNameNotAvailable(GCRentalException):
    """Vehicle Already exist"""
