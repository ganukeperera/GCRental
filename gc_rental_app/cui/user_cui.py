"""User CUI"""

from utils import get_valid_input, clear_screen, draw_box
import configs.strings
from repositories.entities.user import User
from services.vehicle_service import VehicleService
from services.bookings_service import BookingService

class UserCUI:
    """CUI related to Admin"""

    __menu = [
                "1. View All Available Cars",
                "2. Book Car",
                "3. My Bookings",
                "4. Logout",
            ]
    
    def __init__(
            self,
            user: User,
            vehicle_service: VehicleService,
            bookings_service: BookingService
        ):
        self.__user = user
        self.__vehicle_service = vehicle_service
        self.__booking_service = bookings_service

    def show_user_menu(self):
        """Main menu for the User"""
        clear_screen()
        draw_box("Admin Menu")
        while True:
            for item in self.__menu:
                print(item)
            print()
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(self.__menu),
                error_message=configs.strings.INVALID_INPUT
            )
            if choose == 1:
                print("View All Available Cars")
            elif choose == 2:
                print("Book Car")
            elif choose == 3:
                print("My Bookings")
            elif choose == 4:
                break
