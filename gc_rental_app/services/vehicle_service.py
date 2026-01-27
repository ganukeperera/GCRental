"""Vehicle Service"""

import logging
from datetime import date
from repositories.vehicle_repository import VehicleRepository
from repositories.entities.vehicle import Vehicle
from repositories.entities.user import User
from utils.exceptions import VehicleAlreadyExist, VehicleNotFound
from .authorization_service import AuthorizationService

logger = logging.getLogger(__name__)

class VehicleService:
    """
    Business logics related to vehicles,
    including adding, removing, updating and viewing
    """

    def __init__(self, repo: VehicleRepository):
        self.__vehicle_repo = repo

    def add_vehicle(self, user: User, vehicle: Vehicle):
        """Service used for add vehicles"""
        try:
            AuthorizationService.require_admin(user)

            existing = self.__vehicle_repo.get_by_plate(vehicle.plate_number)
            if existing:
                raise VehicleAlreadyExist("Vehicle with this plate number already exists")

            self.__vehicle_repo.add(vehicle)
        except PermissionError as e:
            logger.error("Add vehicle failed!. %s", e)
            raise
        except VehicleAlreadyExist:
            logger.error("Add vehicle failed. Already exists. Plate number: %s", vehicle.plate_number)
            raise
        except Exception as e:
            logger.error("Add vehicle failed!. %s", e)
            raise

    def update_vehicle(self, user: User, vehicle: Vehicle):
        """Service used to update details of a existing vehicle"""
        try:
            AuthorizationService.require_admin(user)

            existing = self.__vehicle_repo.get_by_plate(vehicle.plate_number)
            if not existing:
                raise VehicleNotFound(f"Vehicle with plate number not found: {vehicle.plate_number}")

            self.__vehicle_repo.update(vehicle)
        except PermissionError as e:
            logger.error("Update vehicle failed!. %s", e)
            raise
        except VehicleNotFound as e:
            logger.error("Update vehicle failed: %s", e)
            raise
        except Exception as e:
            logger.error("Update vehicle failed!. %s", e)
            raise

    def remove_vehicle(self, user, plate_number):
        """Service used to remove a vehicle"""
        try:
            AuthorizationService.require_admin(user)

            existing = self.__vehicle_repo.get_by_plate(plate_number=plate_number)
            if not existing:
                raise VehicleNotFound(f"Vehicle with plate number not found: {plate_number}" )

            self.__vehicle_repo.remove(existing.vehicle_id)
        except PermissionError as e:
            logger.error("Remove vehicle failed!. %s", e)
            raise
        except VehicleNotFound as e:
            logger.error("Remove vehicle failed: %s", e)
            raise
        except Exception as e:
            logger.error("Remove vehicle failed!. %s", e)
            raise

    def view_vehicles(self, user: User):
        """Service used to View all vehicles"""
        try:
            AuthorizationService.require_admin(user)

            return self.__vehicle_repo.get_all()
        except PermissionError as e:
            logger.error("Remove vehicle failed!. %s", e)
            raise
        except Exception as e:
            logger.error("Remove vehicle failed!. %s", e)
            raise

    def get_vehicle_by_plate(self, plate_number):
        """Service to check the existence of a vehicle"""

        try:
            vehicle = self.__vehicle_repo.get_by_plate(plate_number)
            if vehicle is None:
                raise VehicleNotFound(f"Vehicle with plate number not found: {plate_number}" )
            return vehicle
        except VehicleNotFound as e:
            logger.error("Search vehicle Failed!: %s", e)
            raise
        except Exception as e:
            logger.error("Search vehicle Failed!. %s", e)
            raise
    
    def get_vehicle_by_id(self, vehicle_id) -> Vehicle:
        """Service to check the existence of a vehicle"""

        try:
            vehicle = self.__vehicle_repo.get_by_id(vehicle_id)
            if vehicle is None:
                raise VehicleNotFound(f"Vehicle with id not found: {vehicle_id}" )
            return vehicle
        except VehicleNotFound as e:
            logger.error("Search vehicle Failed!: %s", e)
            raise
        except Exception as e:
            logger.error("Search vehicle Failed!. %s", e)
            raise

    def list_available_vehicles(self, start_date: date, end_date: date):
        """List vehicles available for booking in the given date range"""
        try:
            if start_date > end_date:
                raise ValueError("Start date must be before end date")

            requested_days = (end_date - start_date).days + 1

            # Get available vehicles from repo
            vehicles = self.__vehicle_repo.get_available_vehicles(start_date, end_date)

            # Filter by min/max rent period
            filtered = [
                v for v in vehicles
                if v.min_rent_period <= requested_days <= v.max_rent_period
            ]

            return filtered

        except ValueError as e:
            logger.exception(
                "Invalid date range: %s - %s. Error: %s", start_date, end_date, e
            )
            raise

        except Exception as e:
            logger.exception(
                "Failed to retrieve available vehicles for dates: %s - %s. Error: %s",
                start_date, end_date, e
            )
            raise

    def check_vehicle_availability(self, vehicle: Vehicle, start_date: date, end_date: date) -> bool:
        """
        Returns True if vehicle is available for booking given date range
        considering existing bookings and min/max rent period.
        """
        try:
            # Validate date range
            if start_date > end_date:
                raise ValueError("Start date must be before end date")

            requested_days = (end_date - start_date).days + 1

            # Check min/max rent period
            if requested_days < vehicle.min_rent_period or requested_days > vehicle.max_rent_period:
                logger.info("Min max rent period violated for vehicle %s from %s to %s. Allowed max period: %s, min period: %s",
                vehicle.plate_number, start_date, end_date, vehicle.max_rent_period, vehicle.min_rent_period)
                return False

            # Check overlapping bookings
            if self.__vehicle_repo.is_vehicle_booked(vehicle.vehicle_id, start_date, end_date):
                logger.info("Vehicle %s is already booked and not available for the period from %s to %s.",
                vehicle.plate_number, start_date, end_date)
                return False

            return True

        except Exception as e:
            logger.exception(
                "Failed to check availability for vehicle %s from %s to %s. Error: %s",
                vehicle.plate_number, start_date, end_date, e
            )
            raise
