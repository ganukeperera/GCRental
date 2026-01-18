"""Authentication and User based things"""

from configs.app_constants import UserRole
from repositeries.user_repositery import UserModel

class User():
    """The base class for all the user types"""
    def __init__(self, fullname, username, mobile, role):
        self.__fullname = fullname
        self.__username = username
        self.__mobile = mobile
        self.__role = role

    @property
    def fullname(self):
        """return fullname"""
        return self.__fullname

    @property
    def username(self):
        """return username"""
        return self.__username

    @property
    def mobile(self):
        """return mobile number"""
        return self.__mobile

    @property
    def role(self):
        """return role"""
        return self.__role

    def is_admin(self):
        """Method to check the user is Admin or User"""
        if int(self.__role) == UserRole.ADMIN.value:
            return True
        else:
            return False

    @classmethod
    def get_user_from(cls, user: UserModel):
        """Convert UserModel object to a User"""
        return User(user.fullname, user.username, user.mobile, user.role)
