"""Auth Service"""

import logging
from user import User
from repositeries.user_repositery import UserModel, UserRepo
from exceptions import UserRegistrationError, InvalidLogin, LoginError

class AuthService():
    """Class responsible to handle login and register user"""

    logger = logging.getLogger(__name__)

    def __init__(self, repo: UserRepo):
        self.__repo = repo

    def register(self, fullname, username, password, mobile, role):
        """Register new User"""

        try:
            user = UserModel(fullname, username, password, mobile, role)
            self.__repo.add_user(user)
            self.logger.info("User %s registered successfully", fullname)
        except Exception as e:
            self.logger.error("Error occurred while registering user %s, error: %s", fullname, e)
            raise UserRegistrationError("Error occurred while registering user") from e

    def login(self, username, password):
        """Authenticate a user"""
        try:
            print(username)
            user = self.__repo.select_user(username)
            if user.password != password:
                raise InvalidLogin("Wrong Credentials")

            return User.get_user_from(user)
        except Exception as e:
            self.logger.error("Error occurred while login in to the app, username: %s, error: %s", username, e)
            raise LoginError("Error occurred while login in to the app") from e
