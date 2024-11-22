#!/usr/bin/env python3
"""Auth module
"""
from db import DB, NoResultFound
from user import User
import bcrypt
import os
import uuid  # Import the uuid module


def _hash_password(password: str) -> bytes:
    """Hashes a given password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid():
    """Generates a new UUID.

    Returns:
         A string representation of the UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to manage user authentication.
    """

    def __init__(self):
        """Initializes an Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the provided email and password match a registered user."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False


