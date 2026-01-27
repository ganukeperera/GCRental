"""PasswordHasher"""

import bcrypt

class PasswordHasher:
    """Utility class developed for password hashing using bcrypt and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the given password using bcrypt"""

        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string to store in sqlite database
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password is correct"""
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(password_bytes, hashed_bytes)