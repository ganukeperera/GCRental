"""Authentication and User based things"""

class User():
    """Represents a User entity in the car rental system"""
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
        """return fullname"""
        return self.__fullname

    @property
    def username(self):
        """return username"""
        return self.__username

    @property
    def password(self):
        """return username"""
        return self.__password

    @property
    def mobile(self):
        """return mobile number"""
        return self.__mobile

    @property
    def role(self):
        """return role"""
        return self.__role
