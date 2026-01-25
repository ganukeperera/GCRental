"""CUIFactory"""

from configs.app_constants import UserRole
from services.auth_service import AuthService
from services.vehicle_service import VehicleService
from services.bookings_service import BookingService
from repositories.entities.user import User
from .admin_cui import AdminCUI
from .super_admin_cui import SuperAdminCUI
from .user_cui import UserCUI
from .session import Session
from .cui import CUI

class CUIFactory:
    """Factory class to create cui based on the user role"""
    @staticmethod
    def create(user: User,
            session: Session,
            auth_service: AuthService=None,
            vehicle_service: VehicleService=None,
            booking_service: BookingService=None
            ) -> CUI:
        """Create CUI based on the user role"""

        role = user.role

        if role == UserRole.SUPER_ADMIN.value:
            return SuperAdminCUI(session, auth_service)

        elif role == UserRole.ADMIN.value:
            return AdminCUI(session, vehicle_service, booking_service)

        elif role == UserRole.USER.value:
            return UserCUI(session, vehicle_service, booking_service)

        else:
            raise ValueError("Unsupported user role")
