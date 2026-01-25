"""Super Admin CUI"""

from utils import get_valid_input, draw_box, clear_screen
import configs.strings
from configs.app_constants import USER_NAME_POLICY_STRING, MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH, PASSWORD_POLICY_STRING, UserRole
from services.auth_service import AuthService
from exceptions import UserRegistrationError

class SuperAdminCUI:
    """CUI related to Super Admin"""

    __menu = [
                "1. Create Admin",
                "2. Logout",
            ]
    
    def __init__(self, auth_service: AuthService):
        self.__auth_service = auth_service
    
    def show_super_admin_menu(self):
        """Main menu for the Admin"""
        while True:
            clear_screen()
            draw_box("Super Admin Menu")
            for item in self.__menu:
                print(item)
            print()
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(self.__menu)
            )
            if choose == 1:
                self.__show_add_admin()
            elif choose == 2:
                break
            else:
                print(configs.strings.INVALID_INPUT)
    
    def __show_add_admin(self):
        """Add admin screen"""

        try:
            clear_screen()
            draw_box("Add Admin")

            username = get_valid_input(
                prompt= f"Username ({USER_NAME_POLICY_STRING}): ",
                validator= lambda x: len(x) >= MIN_USERNAME_LENGTH,
                error_message= f"Username must be at least {MIN_USERNAME_LENGTH} characters"
            )
            password = get_valid_input(
                prompt=f"Password ({PASSWORD_POLICY_STRING}): ",
                validator= lambda x: len(x) >= MIN_PASSWORD_LENGTH,
                error_message= f"Username must be at least {MIN_PASSWORD_LENGTH} characters"
            )
            self.__auth_service.register(username, username, password, "", UserRole.ADMIN.value)
            print("User Registration completed!")
        except UserRegistrationError:
            print(configs.strings.REGISTRATION_FAILED)
        finally:
            input("Press ENTER to continue...")
