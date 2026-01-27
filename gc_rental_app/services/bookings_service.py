"""Booking Service"""

import logging
from datetime import date
from repositories.entities.user import User
from repositories.entities.vehicle import Vehicle
from repositories.entities.booking import Booking
from repositories.bookings_repository import BookingsRepository
from repositories.vehicle_repository import VehicleRepository
from configs.app_constants import BookingStatus, ANALYTICS_DEMAND_PERIOD
from exceptions import BookingNotFound
from .authorization_service import AuthorizationService
from .booking_analytics_service import BookingAnalyticsService

logger = logging.getLogger(__name__)

class BookingService:
    """Service responsible to handle Booking related business logics"""

    def __init__(self,
                 booking_repo: BookingsRepository,
                 vehicle_repo: VehicleRepository,
                 analytics_service: BookingAnalyticsService
                 ):
        self.__booking_repo = booking_repo
        self.__vehicle_repo = vehicle_repo
        self.__analytics_service = analytics_service

    def add_booking(self, user: User, booking: Booking):
        """Service method to add a booking"""
        try:
            # Only allow user to book (admin can’t book vehicles with this version)
            # Later this feature can enable this even for admin if require
            AuthorizationService.require_user(user)

            # Check vehicle availability for given period
            available = self.__check_vehicle_availability(
                self.__vehicle_repo.get_by_id(booking.vehicle_id),
                booking.start_date,
                booking.end_date
            )
            if not available:
                raise ValueError("Vehicle not available for the selected dates or rental period.")

            # Insert booking into DB
            self.__booking_repo.add(booking)
            logger.info(
                "Booking created: user_id=%s, vehicle_id=%s, booking_id=%s",
                booking.user_id, booking.vehicle_id, booking.id
            )

        except PermissionError:
            logger.exception("Booking failed")
            raise

        except ValueError:
            logger.exception("Booking failed")
            raise

        except Exception:
            logger.exception(
                "Unexpected error while creating booking for user_id=%s, vehicle_id=%s",
                booking.user_id, booking.vehicle_id
            )
            raise
    
    def get_bookings_for_user(self, user: User) -> list[Booking]:
        """Return all bookings for the logged-in user"""
        try:
            AuthorizationService.require_user(user)

            return self.__booking_repo.get_by_user_id(user.user_id)

        except PermissionError:
            logger.exception("View bookings failed.")
            raise

        except Exception:
            logger.exception(
                "Failed to retrieve bookings for user_id=%s", user.user_id
            )
            raise

    def __check_vehicle_availability(self, vehicle: Vehicle, start_date: date, end_date: date) -> bool:
        """Check if a vehicle is available for booking considering min/max rent period"""
        requested_days = (end_date - start_date).days + 1

        if requested_days < vehicle.min_rent_period or requested_days > vehicle.max_rent_period:
            return False

        # Repo method checks overlapping bookings
        return not self.__vehicle_repo.is_vehicle_booked(vehicle.vehicle_id, start_date, end_date)

    def get_pending_bookings(self, user: User):
        """Service method to return pending bookings"""
        AuthorizationService.require_admin(user)

        return self.__booking_repo.get_bookings_by_status(BookingStatus.PENDING)

    def get_approved_bookings(self, user: User):
        """Service method to return approved bookings"""
        AuthorizationService.require_admin(user)

        return self.__booking_repo.get_bookings_by_status(BookingStatus.APPROVED)

    def approve_booking(self, user: User, booking_id: int):
        """Approve a pending booking"""
        self.__change_status_of_pending_booking(user, booking_id, BookingStatus.APPROVED)

    def reject_booking(self, user: User, booking_id: int):
        """Reject a pending booking"""
        self.__change_status_of_pending_booking(user, booking_id, BookingStatus.REJECTED)

    def __change_status_of_pending_booking(
            self,
            user: User,
            booking_id: int,
            status: BookingStatus
            ):
        """Used to approve or reject of a pending booking"""
        try:
            AuthorizationService.require_admin(user)

            booking = self.__booking_repo.get_by_booking_id(booking_id)
            if not booking:
                raise BookingNotFound("Booking not found")

            if booking.status != BookingStatus.PENDING.value:
                raise ValueError(
                    f"Cannot {status.value} booking with status: {booking.status}"
                )

            self.__booking_repo.update_booking_status(
                booking_id,
                status
            )

        except PermissionError:
            logger.exception(
                "Changing booking status to %s failed. User not authorized. user_id=%s",
                status.value, user.user_id
            )
            raise

        except ValueError:
            logger.exception(
                "Changing booking status to %s failed. booking_id=%s",
                status.value, booking_id
            )
            raise

        except Exception:
            logger.exception(
                "Unexpected error while changing booking status to %s. booking_id=%s",
                status.value, booking_id
            )
            raise

    def get_all_bookings(self, user: User) -> list[Booking]:
        """view all bookings"""
        try:
            AuthorizationService.require_admin(user)
            
            return self.__booking_repo.get_all()

        except PermissionError:
            logger.exception("View all bookings failed.")
            raise

        except Exception:
            logger.exception("Failed to retrieve all bookings")
            raise

    def get_booking_by_id(self, user, booking_id) -> Booking:
        """view all bookings"""
        try:
            AuthorizationService.require_admin(user)
            
            return self.__booking_repo.get_by_booking_id(booking_id=booking_id)

        except PermissionError:
            logger.exception("View all bookings failed.")
            raise

        except Exception:
            logger.exception("Failed to retrieve all bookings")
            raise

    def complete_booking(self, admin_user, booking_id, new_mileage, additional_charge):
        """Complete booking"""
        try:
            AuthorizationService.require_admin(admin_user)

            booking = self.__booking_repo.get_by_booking_id(booking_id)
            if not booking:
                raise ValueError("Booking not found")

            if booking.status != BookingStatus.APPROVED.value:
                raise ValueError("Only approved bookings can be completed")

            vehicle = self.__vehicle_repo.get_by_id(booking.vehicle_id)
            if not vehicle:
                raise ValueError("Vehicle not found")

            # Mileage validation
            if new_mileage < vehicle.mileage:
                raise ValueError("New mileage cannot be less than current mileage - {vehicle.mileage}")

            # Calculate final total
            final_total = booking.total_cost + additional_charge

            # Complete booking
            booking.total_cost = final_total
            booking.status = BookingStatus.COMPLETED.value
            self.__booking_repo.update(booking)

            # Update vehicle mileage
            self.__vehicle_repo.update_vehicle_mileage(
                vehicle.vehicle_id,
                new_mileage
            )

        except PermissionError:
            logger.exception("Complete booking failed: %s")
            raise
        except ValueError:
            logger.exception("Complete booking validation failed: %s")
            raise
        except Exception:
            logger.exception("Complete booking failed: %s")
            raise

    def calculate_price(self, vehicle: Vehicle, start_date, end_date):
        """Calculate the price dynamically based on the analysis of booking data"""

        base_price = vehicle.daily_rate
        days = (end_date - start_date).days + 1

        demand_multiplier = self.__analytics_service.calculate_demand_factor(vehicle.vehicle_id, start_date, ANALYTICS_DEMAND_PERIOD)

        final_price = base_price * days * demand_multiplier

        return final_price
    
    def get_monthly_revenue(self, user: User):
        """Calculate Monthly Revenue"""
        try:
            AuthorizationService.require_admin(user)
            revenue = self.__analytics_service.get_monthly_revenue()
            if not revenue:
                raise ValueError("No valid data found to generate the report!")
            return revenue
        except PermissionError:
            logger.exception("Complete booking failed: %s")
            raise
        except ValueError:
            logger.exception("Complete booking validation failed: %s")
            raise
        except Exception:
            logger.exception("Complete booking failed: %s")
            raise
