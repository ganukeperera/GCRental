"""User Repository"""

import logging
from database.database_handler import DatabaseHandler
from .entities.user import User

logger = logging.getLogger(__name__)

class UserRepo():
    """Repository class to deal with data in the User table"""

    def __init__(self, db: DatabaseHandler):
        self.__db = db

    def add_user(self, user: User):
        """Add user"""
        self.__db.execute(
                "INSERT INTO users (fullname,username, password, mobile, role) VALUES (?, ?, ?, ?, ?)",
                (user.fullname, user.username, user.password, user.mobile, user.role)
            )
        logger.info("User %s registered successfully", user.fullname)

    def select_user(self, username):
        """select user with given username"""
        cursor = self.__db.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        if not row:
            print("Invalid credentials")
            return None

        return User(row[1], row[2], row[3], row[4], row[5], row[0])
