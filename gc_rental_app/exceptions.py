"""This file contains the custom exceptions defined for the Rental app"""

class GCRentalException(Exception):
    """Base exception for the app"""

class ValidationError(GCRentalException):
    """Validation error"""

class VehicleNotFoundError(GCRentalException):
    """Vehicle not found"""
