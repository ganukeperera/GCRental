"""User Repository"""

import logging
from utils.password_hasher import PasswordHasher
from database.database_handler import DatabaseHandler
from .entities.user import User

logger = logging.getLogger(__name__)

class UserRepo():
    """Repository class to deal with data in the User table"""

    def __init__(self, db: DatabaseHandler):
        self.__db = db

    def add_user(self, user: User):
        """Add user"""
        # Hashing password before storing in the DB

        hashed_password = PasswordHasher.hash_password(user.password)

        self.__db.execute(
                "INSERT INTO user (fullname,username, password, mobile, role) VALUES (?, ?, ?, ?, ?)",
                (user.fullname, user.username, hashed_password, user.mobile, user.role)
            )
        logger.info("User %s registered successfully", user.fullname)

    def select_user(self, username):
        """select user with given username"""
        cursor = self.__db.execute("SELECT * FROM user WHERE username=?", (username,))
        row = cursor.fetchone()
        if not row:
            return None

        return User(row[1], row[2], row[3], row[4], row[5], row[0])
    
    def authenticate(self, username, plain_password):
        """Verify the username and password and return true if password matches"""

        user = self.select_user(username)
        if user is None:
            logger.info("Authentication failed")
            return None
        
        if PasswordHasher.verify_password(plain_password, user.password):
            logger.info("Authentication Success")
            return user
        else:
            logger.info("Authentication failed")
            logger.debug("Password enter for the username %s is incorrect", user.username)
            return None

