"""Admin CUI"""

from utils import get_valid_input
import configs.strings

class AdminCUI:
    """CUI related to Admin"""

    __menu = [
                "1. Manage Cars",
                "2. Manage Booking",
                "3. Logout",
            ]

    __cars_menu = [
                "1. Add Cars", 
                "2. Update Cars", 
                "3. Remove Cars", 
                "4. View All Cars",
                "5. Go Back",
            ]

    __bookings_menu = [
                "1. View All Bookings", 
                "2. View Pending Bookings",
                "3. Approve/Reject Booking",
                "4. Complete Booking",
                "5. Go Back",
            ]

    @classmethod
    def show_admin_menu(cls):
        """Main menu for the Admin"""
        while True:
            for item in cls.__menu:
                print(item)
            
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(cls.__menu)
            )
            if choose == 1:
                cls.show_manage_cars()
            elif choose == 2:
                cls.show_manage_bookings()
            elif choose == 3:
                break
            else:
                print(configs.strings.INVALID_INPUT)


    @classmethod
    def show_manage_bookings(cls):
        """Show manage bookings menu"""

        while True:
            for item in cls.__bookings_menu:
                print(item)
            
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(cls.__bookings_menu)
            )
            if choose == 1:
                #View All Bookings
                print("View All Bookings")
            elif choose == 2:
                #Approve Reject Booking
                print("")
            elif choose == 3:
                print("Approve/Reject Booking")
            elif choose == 4:
                print("Complete Booking")
            elif choose == 5:
                break


    @classmethod
    def show_manage_cars(cls):
        """Show manage cars menu"""
        while True:
            for item in cls.__cars_menu:
                print(item)

            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(cls.__cars_menu)
            )
            if choose == 1:
                print("Add Cars")
            elif choose == 2:
                print("Update Cars")
            elif choose == 3:
                print("Remove Cars")
            elif choose == 4:
                print("Remove Cars")
            elif choose == 5:
                break
