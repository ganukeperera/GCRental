"""User CUI"""

import logging
from utils import get_valid_input, clear_screen, draw_box, get_date_input, print_table
import configs.strings
from repositories.entities.booking import Booking
from services.vehicle_service import VehicleService
from services.bookings_service import BookingService
from cui.session import Session
from .cui import CUI

logger = logging.getLogger(__name__)

class UserCUI(CUI):
    """CUI related to User"""

    __menu = [
                "1. Book a Car",
                "2. View My Bookings",
                "3. Logout",
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
        """Main menu for the User"""

        while True:
            clear_screen()
            draw_box("User Menu")
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
                self.show_book_car()
            elif choose == 2:
                self.view_my_bookings()
            elif choose == 3:
                self.__session.logout()
                break

    def show_book_car(self):
        """List all the cars available for given period and allow booking"""

        clear_screen()
        draw_box("Book a Car")

        print("Enter booking period to see available cars:")

        start_date = get_date_input("Start date (YYYY-MM-DD): ")
        end_date = get_date_input("End date (YYYY-MM-DD): ")

        if start_date > end_date:
            print("Start date cannot be after end date!")
            input("Press Enter to continue...")
            return

        requested_days = (end_date - start_date).days + 1

        try:
            vehicles = self.__vehicle_service.list_available_vehicles(start_date, end_date)
            if not vehicles:
                print("\nNo vehicles available for the selected period.")
            else:
                headers = ["ID", "Plate", "Make", "Model", "Year", "Rate($/day)", "Min Days", "Max Days"]
                rows = [
                    [
                        v.id,
                        v.plate_number,
                        v.make,
                        v.model,
                        v.year,
                        v.daily_rate,
                        v.min_rent_period,
                        v.max_rent_period
                    ]
                    for v in vehicles
                ]
                print_table(headers, rows)

                print()
                # Ask to continue booking
                cont = input("Do you want to continue booking? (Y/N): ").strip().lower()
                if cont != "y":
                    print("Booking cancelled.")
                    logger.info("User cancel booking")
                    return
                
                # Select vehicle
                vehicle_id = int(input("Enter Vehicle ID to book: ").strip())
                selected_vehicle = next((v for v in vehicles if v.id == vehicle_id), None)
                if not selected_vehicle:
                    print("Invalid vehicle ID selected.")
                    input("Press Enter to continue...")
                    return
                
                # Confirm booking period
                print(f"You selected {selected_vehicle.make} {selected_vehicle.model}")
                print(f"Booking period: {start_date} to {end_date} ({requested_days} days)")
                total_cost = selected_vehicle.daily_rate * requested_days
                print(f"Total cost: ${total_cost:.2f}")

                confirm = input("Confirm booking? (Y/N): ").strip().lower()
                if confirm != "y":
                    print("Booking cancelled.")
                    return
                
                # Create booking
                booking = Booking(
                    user_id=self.__session.current_user.id,
                    vehicle_id=selected_vehicle.id,
                    start_date=start_date,
                    end_date=end_date,
                    status="pending",
                    total_cost=total_cost
                )
                self.__booking_service.add_booking(self.__session.current_user, booking)
                print(f"Booking successful! Booking ID: {booking.id}")
                input("Press Enter to continue...")
                
        except Exception:
            print("Failed to retrieve available vehicles. Please try again later.")
        finally:
            input("Press Enter to continue...")

    def view_my_bookings(self):
        """Return all bookings for the logged-in user"""

        clear_screen()
        draw_box("View My Bookings")
        try:
            bookings = self.__booking_service.get_bookings_for_user(self.__session.current_user)

            if not bookings:
                print("You have no bookings.")
                return

            headers = [
                "Booking ID",
                "Vehicle ID",
                "Start Date",
                "End Date",
                "Status",
                "Total Cost"
            ]

            rows = [
                [
                    b.id,
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
            print("You are not authorized to view bookings.")
            input("Press Enter to continue...")
        except Exception as e:
            print("Failed to load bookings. Please try again later.", e)
            input("Press Enter to continue...")
        finally:
            input("Press Enter to continue...")
            
