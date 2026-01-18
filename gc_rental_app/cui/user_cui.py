"""User CUI"""

from utils import get_valid_input
import configs.strings

class UserCUI:
    """CUI related to Admin"""

    __menu = [
                "1. View All Available Cars",
                "2. Book Car",
                "3. My Bookings",
                "4. Logout",
            ]

    @classmethod
    def show_user_menu(cls):
        """Main menu for the User"""
        while True:
            for item in cls.__menu:
                print(item)

            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(cls.__menu),
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
