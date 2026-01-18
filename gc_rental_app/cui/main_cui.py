"""CUI for the car rental app"""

import os
import sys
import configs.strings
from services.auth_service import AuthService
from utils import get_valid_input
from exceptions import InvalidLogin, LoginError, UserRegistrationError
from configs.app_constants import USER_NAME_POLICY_STRING, MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH, PASSWORD_POLICY_STRING
from cui.admin_cui import AdminCUI
from cui.user_cui import UserCUI

class MainCUI:
    """Responsible to generate the UI"""

    @classmethod
    def clear_screen(cls):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @classmethod
    def show_main_menu(cls):
        """Main menu"""

        print("\n1. Login")
        print("2. Register")
        print("3. Exit")

    @classmethod
    def show_home_screen(cls, auth_service: AuthService):
        """Main loop"""
        try:
            while True:
                cls.clear_screen()

                cls.show_main_menu()
                choice = get_valid_input(
                    prompt="Your choice:",
                    cast_func=int,
                    validator=lambda x: 1 <= x <= 3,
                )

                if choice == 1:
                    cls.show_login_screen(auth_service)
                elif choice == 2:
                    cls.show_register_screen(auth_service)
                elif choice == 3:
                    cls.clear_screen()
                    print(configs.strings.EXIT_MESSAGE)
                    sys.exit(0)
        except KeyboardInterrupt:
            print("\n")
            print(configs.strings.EXIT_MESSAGE)

    @classmethod
    def show_login_screen(cls, auth_service: AuthService):
        """show login flow"""

        cls.clear_screen()

        username = get_valid_input(
                prompt="Username: ",
                validator= lambda x: len(x) > 0
            )
        password = get_valid_input(
            prompt="Password: ",
            validator= lambda x: len(x) > 0
        )
        try:
            user = auth_service.login(username, password)
            if user.is_admin():
                AdminCUI.show_admin_menu()
            else:
                UserCUI.show_user_menu()
        except LoginError:
            print(configs.strings.LOGIN_FAILED)
        except InvalidLogin:
            print(configs.strings.INVALID_CREDENTIALS)

    @classmethod
    def show_register_screen(cls, auth_service: AuthService):
        """Register screen"""

        try:
            fullname = get_valid_input(
                prompt = "Fullname :",
                validator= lambda x: len(x) > 0
            )
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
            mobile = get_valid_input(
                prompt = "Mobile Number :",
                validator= lambda x: len(x) > 0,
                error_message= configs.strings.INVALID_INPUT
            )
            role = get_valid_input(
                prompt = "Role (1. Admin, 2. User) :",
                validator= lambda x: 1 <= x <= 2,
                cast_func=int,
                error_message= configs.strings.INVALID_INPUT
            )
            auth_service.register(fullname, username, password, mobile, role)
            print("User Registration completed!")
            input()
        except UserRegistrationError:
            print(configs.strings.REGISTRATION_FAILED)
            input()
