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
