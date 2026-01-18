"""User Repository"""

import logging
from database.database_handler import DatabaseHandler

class UserModel():
    """User data model"""
    def __init__(self, fullname, username, password, mobile, role, user_id = 0):
        self.__user_id = user_id
        self.__fullname = fullname
        self.__username = username
        self.__password = password
        self.__mobile = mobile
        self.__role = role
    
    @property
    def user_id(self):
        """Getter for user id"""
        return self.__user_id

    @property
    def fullname(self):
        """Getter for fullname"""
        return self.__fullname

    @property
    def username(self):
        """Getter for username"""
        return self.__username

    @property
    def password(self):
        """Getter for username"""
        return self.__password

    @property
    def mobile(self):
        """Getter for mobile"""
        return self.__mobile

    @property
    def role(self):
        """Getter for role"""
        return self.__role

class UserRepo():
    """Repository class to deal with data in the User table"""

    logger = logging.getLogger(__name__)

    def __init__(self, db: DatabaseHandler):
        self.__db = db

    def add_user(self, user: UserModel):
        """Add user"""
        try:
            self.__db.execute(
                "INSERT INTO users (fullname,username, password, mobile, role) VALUES (?, ?, ?, ?, ?)",
                (user.fullname, user.username, user.password, user.mobile, user.role)
            )
            self.logger.info("User %s registered successfully", user.fullname)
        except Exception as e:
            self.logger.error("Error occurred while registering user %s, error: %s", user.fullname, e)
            raise

    def select_user(self, username):
        """select user with given username"""
        try:
            print(username)
            cursor = self.__db.execute("SELECT * FROM users WHERE username=?", (username,))
            row = cursor.fetchone()

            if not row:
                print("Invalid credentials")
                return None

            return UserModel(row[1], row[2], row[3], row[4], row[5], row[0])
        except Exception as e:
            self.logger.error("Error occurred while searching for user %s, error: %s", username, e)
            raise
