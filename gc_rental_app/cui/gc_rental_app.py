"""CUI for the car rental app"""

import sys
import configs.strings
from services.auth_service import AuthService
from services.vehicle_service import VehicleService
from services.bookings_service import BookingService
from cui.cui_helper import get_valid_input, draw_box, clear_screen
from utils.exceptions import InvalidLogin, UserRegistrationError
from configs.app_constants import USER_NAME_POLICY_STRING, MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH, PASSWORD_POLICY_STRING, UserRole
from .session import Session
from .cui_factory import CUIFactory

class GCRentalApp:
    """Responsible to generate the UI"""

    def __init__(
            self,
            session: Session,
            auth_service: AuthService,
            vehicle_service: VehicleService,
            booking_service: BookingService
        ):
        self.__session = session
        self.__auth_service = auth_service
        self.__vehicle_service = vehicle_service
        self.__booking_service = booking_service
        

    def show_menu(self):
        """Main menu"""
        draw_box("Main Menu")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        print()

    def start(self):
        """Main loop"""
        try:
            while True:
                clear_screen()

                self.show_menu()
                choice = get_valid_input(
                    prompt="Your choice:",
                    cast_func=int,
                    validator=lambda x: 1 <= x <= 3,
                )

                if choice == 1:
                    self.show_login_screen()
                elif choice == 2:
                    self.show_register_screen()
                elif choice == 3:
                    clear_screen()
                    print(configs.strings.EXIT_MESSAGE)
                    print()
                    sys.exit(0)
        except KeyboardInterrupt:
            print("\n")
            print(configs.strings.EXIT_MESSAGE)
            print()

    def show_login_screen(self):
        """show login flow"""

        clear_screen()
        draw_box("Login")
        username = get_valid_input(
                prompt="Username: ",
                validator= lambda x: len(x) > 0
            )
        password = get_valid_input(
            prompt="Password: ",
            validator= lambda x: len(x) > 0
        )
        try:
            user = self.__auth_service.login(username, password)
            self.__session.login(user)
            cui = CUIFactory.create(
                user,
                self.__session,
                self.__auth_service,
                self.__vehicle_service,
                self.__booking_service
                )
            cui.show_menu()
        except InvalidLogin:
            print("\n",configs.strings.INVALID_CREDENTIALS, sep="")
            input("Press ENTER to continue...")

    def show_register_screen(self):
        """Register screen"""

        try:
            clear_screen()
            draw_box("Register")
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
            self.__auth_service.register(fullname, username, password, mobile, UserRole.USER.value)
            print("User Registration completed!")
        except UserRegistrationError:
            print(configs.strings.REGISTRATION_FAILED)
        finally:
            input("Press ENTER to continue...")
