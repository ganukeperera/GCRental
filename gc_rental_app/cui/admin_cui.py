"""Admin CUI"""

from utils import get_valid_input, print_table, draw_box, clear_screen
from repositories.entities.vehicle import Vehicle
from repositories.entities.user import User
import configs.strings
from services.vehicle_service import VehicleService
from services.bookings_service import BookingService
import exceptions

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

    def __init__(
            self,
            user: User,
            vehicle_service: VehicleService,
            bookings_service: BookingService
        ):
        self.__user = user
        self.__vehicle_service = vehicle_service
        self.__booking_service = bookings_service

    def show_admin_menu(self):
        """Main menu for the Admin"""
        clear_screen()
        draw_box("Admin Menu")
        while True:
            for item in self.__menu:
                print(item)
            print()
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(self.__menu)
            )
            if choose == 1:
                self.__show_manage_cars()
            elif choose == 2:
                self.__show_manage_bookings()
            elif choose == 3:
                break
            else:
                print(configs.strings.INVALID_INPUT)

    def __show_manage_cars(self):
        """Show manage cars menu"""
        clear_screen()
        draw_box("Manage Vehicles")
        while True:
            for item in self.__cars_menu:
                print(item)
            print()
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(self.__cars_menu)
            )
            if choose == 1:
                self.__show_add_car()
            elif choose == 2:
                self.__show_update_car()
            elif choose == 3:
                self.__show_remove_vehicle()
            elif choose == 4:
                self.__show_all_vehicles()
            elif choose == 5:
                break
    
    def __show_add_car(self):
        "Adding Cars to the inventory"
        clear_screen()
        draw_box("Add Vehicles")
        try:
            vehicle = self.__collect_vehicle_input()
            self.__vehicle_service.add_vehicle(self.__user, vehicle)
        except PermissionError:
            print("User not authorized")
        except exceptions.VehicleAlreadyExist:
            print("Vehicle Already exist")
        except Exception:
            print("Add vehicle failed! Please try again later")

    def __show_update_car(self):
        """Update vehicles"""
        clear_screen()
        draw_box("Update Vehicles")
        try:
            plate = get_valid_input(
                prompt="Enter plate number of vehicle to update: ",
                validator=lambda x: len(x) > 0
            )
            existing_vehicle = self.__vehicle_service.get_vehicle_by_plate(plate)
            print("Press Enter to keep existing values")
            updated_vehicle = self.__collect_vehicle_input(existing_vehicle)
            print(updated_vehicle.year)
            self.__vehicle_service.update_vehicle(self.__user, updated_vehicle)
            print("Vehicle updated successfully")

        except PermissionError:
            print("User not authorized")

        except exceptions.VehicleNotFound:
            print("Vehicle not found")

        except Exception as e:
            print("Update vehicle failed! Please try again later:", e)

    def __show_remove_vehicle(self):
        clear_screen()
        draw_box("Remove Vehicles")
        try:
            plate = get_valid_input(
                prompt="Enter plate number of vehicle to Remove: ",
                validator=lambda x: len(x) > 0
            )
            existing_vehicle = self.__vehicle_service.get_vehicle_by_plate(plate)

            if not existing_vehicle:
                return

            self.__vehicle_service.remove_vehicle(self.__user, plate_number=plate)
            print("Vehicle removed successfully")

        except PermissionError:
            print("User not authorized")

        except exceptions.VehicleNotFound:
            print("Vehicle not found")

        except Exception:
            print("Remove vehicle failed! Please try again later")

    def __show_all_vehicles(self):
        clear_screen()
        draw_box("View All Vehicles")
        try:
            vehicles = self.__vehicle_service.view_vehicles(self.__user)
            headers = [
                "ID", "Plate", "Brand", "Model",
                "Year", "Mileage", "Rate($)",
                "Max Period", "Min Period"
            ]

            rows = [
                [
                    v.vehicle_id,
                    v.plate_number,
                    v.make,
                    v.model,
                    v.year,
                    v.mileage,
                    f"{v.daily_rate:.2f}",
                    v.max_rent_period,
                    v.min_rent_period
                ]
                for v in vehicles
            ]

            print_table(headers, rows)
        except Exception:
            print("Remove vehicle failed! Please try again later!")

    def __collect_vehicle_input(self, existing_vehicle=None):
        plate = get_valid_input(
                prompt="Enter Plate Number: ",
                default=existing_vehicle.plate_number if existing_vehicle else None,
                validator=lambda x: len(x) > 0,
        )

        make = get_valid_input(
            prompt="Enter Make: ",
            default=existing_vehicle.make if existing_vehicle else None,
            validator=lambda x: len(x) > 0
        )

        model = get_valid_input(
            prompt="Enter Model: ",
            default=existing_vehicle.model if existing_vehicle else None,
            validator=lambda x: len(x) > 0
        )

        year = get_valid_input(
            prompt="Enter year: ",
            cast_func=int,
            default=existing_vehicle.year if existing_vehicle else None,
            validator=lambda x: 1900 <= x <= 2100
        )

        mileage = get_valid_input(
            prompt="Enter mileage: ",
            cast_func=int,
            default=existing_vehicle.mileage if existing_vehicle else None,
            validator=lambda x: x >= 0
        )

        rate = get_valid_input(
            prompt="Enter rate (Daily): ",
            cast_func=float,
            default=existing_vehicle.daily_rate if existing_vehicle else None,
            validator=lambda x: x > 0
        )

        min_period = get_valid_input(
            prompt="Enter minimum rent period: ",
            cast_func=int,
            default=existing_vehicle.min_rent_period if existing_vehicle else None,
            validator=lambda x: x > 0
        )

        max_period = get_valid_input(
            prompt="Enter max rent period: ",
            cast_func=int,
            default=existing_vehicle.max_rent_period if existing_vehicle else None,
            validator=lambda x: x >= min_period
        )

        return Vehicle(
            plate_number=plate,
            make=make,
            model=model,
            year=year,
            mileage=mileage,
            daily_rate=rate,
            min_rent_period=min_period,
            max_rent_period=max_period,
            vehicle_id=existing_vehicle.vehicle_id if existing_vehicle else None
    )


    def __show_manage_bookings(self):
        """Show manage bookings menu"""
        clear_screen()
        draw_box("Manage Bookings")
        while True:
            for item in self.__bookings_menu:
                print(item)
            print()
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(self.__bookings_menu)
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
