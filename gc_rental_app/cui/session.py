"""Session"""

from repositories.entities.user import User

class Session:
    """This class help to manage the user session"""
    def __init__(self):
        self.__current_user = None

    def login(self, user: User):
        """Mange login"""
        self.__current_user = user

    def logout(self):
        """Manage logout"""
        self.__current_user = None

    @property
    def current_user(self):
        """The getter method for current_user attribute"""
        return self.__current_user

    def is_authenticated(self):
        """Is user authenticated"""
        return self.__current_user is not None
