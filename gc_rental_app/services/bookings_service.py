"""Booking Serice"""
from repositories.bookings_repository import BookingsRepository
class BookingService:

    def __init__(self, booking_repo: BookingsRepository):
        print()