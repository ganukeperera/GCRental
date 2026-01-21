"""Bookings Repository"""

from database.database_handler import DatabaseHandler

class BookingsRepository:
    """Methods related to vehicle repo"""
    def __init__(self, db: DatabaseHandler):
        self.__db = db