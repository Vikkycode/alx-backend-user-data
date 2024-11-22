#!/usr/bin/env python3
"""Auth module
"""
from db import DB, NoResultFound
from user import User
import bcrypt
import os

def _hash_password(password: str) -> bytes:
    """Hashes a given password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The bcrypt hash of the password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password



class Auth:
    """Auth class to manage user authentication.
    """

    def __init__(self):
        """Initializes an Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email: The user's email address.
            password: The user's password.

        Returns:
            The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # Hash the password
            hashed_password = _hash_password(password)

            # Create and save the user
            user = self._db.add_user(email, hashed_password)
            return user





