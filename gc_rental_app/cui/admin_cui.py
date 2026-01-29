"""Admin CUI"""

import logging
from cui.cui_helper import get_valid_input, print_table, draw_box, clear_screen
from repositories.entities.vehicle import Vehicle
import configs.strings
from services.vehicle_service import VehicleService
from services.bookings_service import BookingService
import utils.exceptions as exceptions
from .session import Session
from .cui import CUI

logger = logging.getLogger(__name__)

class AdminCUI(CUI):
    """CUI related to Admin"""

    __menu = [
                "1. Manage Cars",
                "2. Manage Bookings",
                "3. Reports",
                "4. Logout",
            ]

    __cars_menu = [
                "1. Add New Cars", 
                "2. Update Car Details", 
                "3. Remove Car", 
                "4. View All Cars",
                "5. Go Back",
            ]

    __bookings_menu = [
                "1. View All Bookings", 
                "2. Manage Pending Bookings",
                "3. Complete Booking",
                "4. Go Back",
            ]
    
    __report_menu = [
            "1. Revenue Report",
            "2. Go Back"
        ]

    def __init__(
            self,
            session: Session,
            vehicle_service: VehicleService,
            bookings_service: BookingService
        ):
        self.__session = session
        self.__vehicle_service = vehicle_service
        self.__booking_service = bookings_service

    def show_menu(self):
        """Main menu for the Admin"""
        while True:
            clear_screen()
            draw_box("Admin Menu")
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
                self.__show_reports()
            elif choose == 4:
                self.__session.logout()
                break
            else:
                print(configs.strings.INVALID_INPUT)

    def __show_manage_cars(self):
        """Show manage cars menu"""
        while True:
            clear_screen()
            draw_box("Manage Vehicles")
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

    def __show_reports(self):
        """Show manage cars menu"""
        while True:
            clear_screen()
            draw_box("Reports")
            for item in self.__report_menu:
                print(item)
            print()
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(self.__cars_menu)
            )
            if choose == 1:
                self.__show_monthly_revenue()
            elif choose == 2:
                break

    def __show_monthly_revenue(self):
        "Show monthly revenue report"
        clear_screen()
        draw_box("Revenue Report")
        try:
            headers = ["Month", "Revenue ($)"]
            rows = self.__booking_service.get_monthly_revenue(self.__session.current_user)
            print_table(headers, rows)
            
        except PermissionError:
            print("User not authorized")
        except ValueError as e:
            print(e)
        except Exception as e:
            logging.exception("Unexpected error occurred!!! error = %s", e)
            print("Add vehicle failed! Please try again later")
        finally:
            input("Press Enter to continue...")
    
    def __show_add_car(self):
        "Adding Cars to the inventory"
        clear_screen()
        draw_box("Add Vehicles")
        try:
            vehicle = self.__collect_vehicle_input()
            self.__vehicle_service.add_vehicle(self.__session.current_user, vehicle)
            print("Vehicle added successfully")
        except PermissionError:
            print("User not authorized")
        except exceptions.VehicleAlreadyExist:
            print("Vehicle Already exist")
        except Exception as e:
            logging.exception("Unexpected error occurred!!! error = %s", e)
            print("Add vehicle failed! Please try again later")
        finally:
            input("Press Enter to continue...")

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
            self.__vehicle_service.update_vehicle(self.__session.current_user, updated_vehicle)
            print("Vehicle updated successfully")

        except PermissionError:
            print("User not authorized")
        except exceptions.VehicleNotFound:
            print("Vehicle not found")
        except Exception as e:
            logging.exception("Unexpected error occurred!!! error = %s", e)
            print("Update vehicle failed! Please try again later!!!")
        finally:
            input("Press Enter to continue...")

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

            self.__vehicle_service.remove_vehicle(self.__session.current_user, plate_number=plate)
            print("Vehicle removed successfully")

        except PermissionError:
            print("User not authorized")
        except exceptions.VehicleNotFound:
            print("Vehicle not found")
        except Exception as e:
            logging.exception("Unexpected error occurred!!! error = %s", e)
            print("Remove vehicle failed! Please try again later")
        finally:
            input("Press Enter to continue...")

    def __show_all_vehicles(self):
        clear_screen()
        draw_box("View All Vehicles")
        try:
            vehicles = self.__vehicle_service.view_vehicles(self.__session.current_user)
            if vehicles is None or len(vehicles) == 0:
                print("No vehicles found!")
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
        except Exception as e:
            logging.exception("Unexpected error occurred!!! error = %s", e)
            print("Remove vehicle failed! Please try again later!")
        finally:
            input("Press Enter to continue...")

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
        while True:
            clear_screen()
            draw_box("Manage Bookings")
            for item in self.__bookings_menu:
                print(item)
            print()
            choose = get_valid_input(
                prompt="Choose : ",
                cast_func=int,
                validator= lambda x: 1<=x<=len(self.__bookings_menu)
            )
            if choose == 1:
                self.__show_all_bookings()
            elif choose == 2:
                self.__show_manage_pending_bookings()
            elif choose == 3:
                self.__show_complete_booking()
            elif choose == 4:
                break

    def __show_all_bookings(self):
        """View all booking"""

        clear_screen()
        draw_box("View All Bookings")
        try:
            bookings = self.__booking_service.get_all_bookings(self.__session.current_user)
            if not bookings:
                print("No bookings found.")
                return

            headers = [
                "Booking ID",
                "User ID",
                "Vehicle ID",
                "Start Date",
                "End Date",
                "Status",
                "Total Cost"
            ]

            rows = [
                [
                    b.id,
                    b.user_id,
                    b.vehicle_id,
                    b.start_date,
                    b.end_date,
                    b.status,
                    f"${b.total_cost:.2f}" if b.total_cost else "-"
                ]
                for b in bookings
            ]

            print_table(headers, rows)

        except PermissionError:
            print("You are not authorized to view all bookings.")
        except Exception as e:
            logging.exception("Unexpected error occurred!!! error = %s", e)
            print("Failed to load bookings. Please try again later!")
        finally:
            input("Press Enter to continue...")

    def __show_manage_pending_bookings(self):
        """View Pending bookings and manage them"""
        clear_screen()
        draw_box("View And Manage Pending Bookings")
        try:
            # Get pending bookings
            pending_bookings = self.__booking_service.get_pending_bookings(self.__session.current_user)

            if not pending_bookings:
                print("No pending bookings.")
                return

            # Display pending bookings
            headers = [
                "Booking ID",
                "User ID",
                "Vehicle ID",
                "Start Date",
                "End Date",
                "Total Cost"
            ]

            rows = [
                [
                    b.id,
                    b.user_id,
                    b.vehicle_id,
                    b.start_date,
                    b.end_date,
                    f"${b.total_cost:.2f}" if b.total_cost else "-"
                ]
                for b in pending_bookings
            ]

            print_table(headers, rows)

            # Ask admin if they want to take action
            choice = get_valid_input(
                "Do you want to approve or reject a booking? (y/n): ",
                validator=lambda x: x in ("y", "n", "Y", "N")
            )
            if choice.lower() != "y":
                return
            # Get booking ID
            booking_id = get_valid_input(
                "Enter Booking ID: ",
                int
            )

            selected_booking = next(
                (b for b in pending_bookings if b.id == booking_id), None
            )
            if not selected_booking:
                print("Invalid Booking ID selected.")
                return

            # Approve or reject
            action = get_valid_input(
                "Do you want to Approve or Reject selected booking? (a/r): ",
                validator= lambda x: x in ("a", "r", "A", "R")
            )
            if action.lower() == "a":
                self.__booking_service.approve_booking(self.__session.current_user, booking_id)
                print(f"Booking {booking_id} approved successfully.")

            elif action == "r":
                self.__booking_service.reject_booking(self.__session.current_user, booking_id)
                print(f"Booking {booking_id} rejected successfully.")

            else:
                print("Invalid action selected.")

        except PermissionError:
            print("You are not authorized to manage bookings.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            logging.exception("Unexpected error occurred!!! error = %s", e)
            print("Failed to update booking. Please try again later.")
        finally:
            input("Press Enter to continue...")

    def __show_complete_booking(self):
        """Complete the booking once Vehicle is returned"""

        clear_screen()
        draw_box("Complete Booking")
        try:
            # Step 1: Get approved bookings with user details
            bookings = self.__booking_service.get_approved_bookings(self.__session.current_user)

            if not bookings:
                print("No approved bookings available to complete.")
                return

            # Step 2: Display bookings
            headers = [
                "Booking ID",
                "User ID",
                "Vehicle ID",
                "Start Date",
                "End Date",
                "Total Cost"
            ]

            rows = [
                [
                    b.id,
                    b.user_id,
                    b.vehicle_id,
                    b.start_date,
                    b.end_date,
                    f"${b.total_cost:.2f}"
                ]
                for b in bookings
            ]

            print_table(headers, rows)
            print()

            # Step 4: Select booking
            booking_id = get_valid_input(
                "Enter Booking ID you want to complete: ",
                int
            )

            booking = next((b for b in bookings if b.id == booking_id), None)
            if not booking:
                print("Invalid Booking ID.")
                return

            # Step 5: Additional charges

            additional_charge = get_valid_input(
                "Enter additional charge amount if applicable: ",
                float,
                default=0.0
            )
            if additional_charge < 0:
                print("Additional charge cannot be negative.")
                return
            
            # Step 6: Get new mileage
            new_mileage = get_valid_input(
                "Enter new mileage of the car: ",
                int
            )

            # Step 7: Complete booking
            self.__booking_service.complete_booking(
                self.__session.current_user,
                booking_id,
                new_mileage,
                additional_charge
            )

            updated_booking = self.__booking_service.get_booking_by_id(self.__session.current_user, booking.id)

            print(
                f"\nBooking {booking_id} completed successfully.\n"
                f"Total Rental Charges = ${updated_booking.total_cost:.2f}"
            )

        except PermissionError:
            print("You are not authorized to complete bookings.")
        except ValueError:
            print("Cannot complete booking. Please try again later!")
        except Exception as e:
            logging.exception("Unexpected error occurred!!! error = %s", e)
            print("Failed to complete booking. Please try again later.")
        finally:
            input("Press Enter to continue...")
