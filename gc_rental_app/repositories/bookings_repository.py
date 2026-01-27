"""Bookings Repository"""

from datetime import date
from decimal import Decimal
from database.database_handler import DatabaseHandler
from configs.app_constants import BookingStatus
from .entities.booking import Booking

class BookingsRepository:
    """Methods related to vehicle repo"""
    def __init__(self, db: DatabaseHandler):
        self.__db = db

    def add(self, booking: Booking):
        """Add booking into DB"""
        sql = """
        INSERT INTO bookings (user_id, vehicle_id, start_date, end_date, status, total_cost)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor = self.__db.execute(
            sql,
            (
                booking.user_id,
                booking.vehicle_id,
                booking.start_date.isoformat(),
                booking.end_date.isoformat(),
                booking.status,
                booking.total_cost
            )
        )
        booking.id = cursor.lastrowid  # set the generated booking ID
        return booking

    def get_bookings_by_status(self, status: BookingStatus) -> list[Booking]:
        """This returns all the bookings with give booking status"""
        cursor = self.__db.execute(
            """
            SELECT id, user_id, vehicle_id, start_date, end_date, status, total_cost
            FROM bookings
            WHERE status = ?
            """,
            (status.value,)
        )

        rows = cursor.fetchall()

        bookings = []
        for row in rows:
            bookings.append(
                Booking(
                    booking_id=row["id"],
                    user_id=row["user_id"],
                    vehicle_id=row["vehicle_id"],
                    start_date=date.fromisoformat(row["start_date"]),
                    end_date=date.fromisoformat(row["end_date"]),
                    status=row["status"],
                    total_cost=Decimal(row["total_cost"]) if row["total_cost"] else None
                )
            )

        return bookings

    def update(
        self,
        booking: Booking,
    ) -> bool:
        """Update the booking into a different status"""

        cursor = self.__db.execute(
            """
            UPDATE bookings
            SET status = ?,
            total_cost = ?
            WHERE id = ?
            """,
            (booking.status, booking.total_cost, booking.id)
        )

        return cursor.rowcount > 0
    
    def update_booking_status(
            self,
            booking_id: int,
            new_status: BookingStatus
        ) -> bool:
        """Update the booking into a different status"""

        cursor = self.__db.execute(
            """
            UPDATE bookings
            SET status = ?
            WHERE id = ?
            """,
            (new_status.value, booking_id)
        )

        return cursor.rowcount > 0
    
    def get_by_booking_id(self, booking_id: int) -> Booking | None:
        """Get booking by booking id"""
        sql = """
            SELECT id,
                user_id,
                vehicle_id,
                start_date,
                end_date,
                status,
                total_cost
            FROM bookings
            WHERE id = ?
        """
        cursor = self.__db.execute(sql, (booking_id,))
        row = cursor.fetchone()

        if not row:
            return None

        return Booking(
            booking_id=row[0],
            user_id=row[1],
            vehicle_id=row[2],
            start_date=row[3],
            end_date=row[4],
            status=row[5],
            total_cost=row[6]
        )

    def get_by_user_id(self, user_id: int) -> list[Booking]:
        """Get all bookings for a given user"""
        sql = """
        SELECT id, user_id, vehicle_id, start_date, end_date, status, total_cost
        FROM bookings
        WHERE user_id = ?
        ORDER BY start_date DESC
        """
        cursor = self.__db.execute(sql, (user_id,))
        rows = cursor.fetchall()

        bookings = []
        for row in rows:
            bookings.append(
                Booking(
                    booking_id=row[0],
                    user_id=row[1],
                    vehicle_id=row[2],
                    start_date=row[3],
                    end_date=row[4],
                    status=row[5],
                    total_cost=row[6]
                )
            )
        return bookings

    def get_all(self) -> list[Booking]:
        """Get all bookings"""
        sql = """
        SELECT id, user_id, vehicle_id, start_date, end_date, status, total_cost
        FROM bookings
        ORDER BY id DESC
        """
        cursor = self.__db.execute(sql)
        rows = cursor.fetchall()
        bookings = []
        for row in rows:
            bookings.append(
                Booking(
                    booking_id=row[0],
                    user_id=row[1],
                    vehicle_id=row[2],
                    start_date=row[3],
                    end_date=row[4],
                    status=row[5],
                    total_cost=row[6]
                )
            )
        return bookings
