"""Auth Service"""

import logging
from repositories.entities.user import User
from repositories.user_repository import UserRepo
from utils.exceptions import UserRegistrationError, InvalidLogin, LoginError, UserNameNotAvailable

logger = logging.getLogger(__name__)

class AuthService():
    """Service responsible to handle login and register user related business logics"""

    def __init__(self, repo: UserRepo):
        self.__repo = repo

    def register(self, fullname, username, password, mobile, role):
        """Register new User"""

        try:
            check_available = self.__repo.select_user(username)
            if check_available is not None:
                raise UserNameNotAvailable("Username already exist in the system")
            user = User(fullname, username, password, mobile, role)
            self.__repo.add_user(user)
            logger.info("User %s registered successfully", fullname)
        
        except UserNameNotAvailable:
            logger.error("Username not available. username = %s", username)
            raise
        except Exception as e:
            logger.error("Error occurred while registering user %s, error: %s", fullname, e)
            raise UserRegistrationError("Error occurred while registering user") from e

    def login(self, username, password):
        """Authenticate a user"""
        try:
            user = self.__repo.authenticate(username, password)
            if user is None:
                raise InvalidLogin("Wrong Credentials")
            
            return user
        except InvalidLogin:
            raise
        except Exception as e:
            logger.error("Error occurred while login in to the app, username: %s, error: %s", username, e)
            raise LoginError("Error occurred while login in to the app") from e
