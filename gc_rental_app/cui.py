"""CUI for the car rental app"""

import os
import sys
from user import AuthService, Admin
from utils import get_valid_input
import configs.strings
from configs.app_constants import USER_NAME_POLICY_STRING, MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH, PASSWORD_POLICY_STRING


class CUI:
    """Responsible to generate the UI"""

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_main_menu(self):
        """Main menu"""

        print("\n1. Login")
        print("2. Register")
        print("3. Exit")

    def show_home_screen(self, auth_service: AuthService):
        """Main loop"""
        try:
            while True:
                self.clear_screen()

                self.show_main_menu()
                choice = get_valid_input(
                    prompt="Your choice:",
                    cast_func=int,
                    validator=lambda x: 1 <= x <= 3,
                )

                if choice == 1:
                    self.show_login_screen(auth_service)
                elif choice == 2:
                    self.show_register_screen(auth_service)
                elif choice == 3:
                    self.clear_screen()
                    print(configs.strings.EXIT_MESSAGE)
                    sys.exit(0)
        except KeyboardInterrupt:
            print("\n")
            print(configs.strings.EXIT_MESSAGE)

    def show_login_screen(self, auth_service: AuthService):
        """show login flow"""

        self.clear_screen()

        username = get_valid_input(
                prompt="Username: ",
                validator= lambda x: len(x) > 0
            )
        password = get_valid_input(
            prompt="Password: ",
            validator= lambda x: len(x) > 0
        )
        user = auth_service.login(username, password)
        if user is None:
            print(configs.strings.LOGIN_WRONG_CREDENTIALS)
        elif isinstance(user, Admin):
            self.show_admin_menu()
        else:
            self.show_user_menu()

        
    def show_admin_menu(self):
        """Shows menu for admin login"""

        while True:
            self.clear_screen()
            admin_menu = [
                "1. Add car", 
                "2. Remove car",
                "3. Update car",
                "4. View car",
                "5. Back",
            ]
            for val in admin_menu:
                print(val)
            selected = get_valid_input(
                prompt="Choose: ",
                cast_func=int,
                validator=lambda x: 1<=x<=len(admin_menu)
            )
            if selected == len(admin_menu):
                break


    def show_user_menu(self):
        """Shows menu for user login"""

        self.clear_screen()
        print("User menu")
        input()

    def show_register_screen(self, auth_service: AuthService):
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
                validator= lambda x: len(x) >= 10,
                error_message= configs.strings.LOGIN_WRONG_CREDENTIALS
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
        except Exception:
            print("User Registration failed!. Please enter to continue")
            input()
        return None

    def user_menu(self, user):
        while True:
            print("\n--- Menu ---")
            for option in user.get_menu():
                print(option)

            choice = input("Select option: ")

            if choice == "4" or choice == "3":
                print("Logging out...")
                break
