"""Authorization Service"""

from configs.app_constants import UserRole
from repositories.entities.user import User

class AuthorizationService:
    """This class help to handle the authorization based on the user's role"""

    @staticmethod
    def require_super_admin(user: User):
        """To be used with super admin level authorization"""
        if user.role != UserRole.SUPER_ADMIN.value:
            raise PermissionError("Super Admin required")

    @staticmethod
    def require_admin(user: User):
        """To be used with admin level authorization"""
        if user.role != UserRole.ADMIN.value:
            raise PermissionError("Admin required")
        
    @staticmethod
    def require_user(user: User):
        """To be used with user level authorization"""
        if user.role != UserRole.USER.value:
            raise PermissionError("Super Admin required")