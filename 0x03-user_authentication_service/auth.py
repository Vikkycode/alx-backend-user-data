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
        """Checks if the provided email and
        password match a registered user.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str | None:
        """Creates a new session for the user with the given email.

        Args:
            email: The email of the user.

        Returns:
            The session ID as a string, or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            # Use update_user
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None


def get_user_from_session_id(self, session_id: str) -> User | None:
    """Retrieves a user based on the given session ID.

    Args:
        session_id: The session ID to search for.

    Returns:
        The User object if found, otherwise None.
    """
    if session_id is None:
        return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None


def destroy_session(self, user_id: int) -> None:
    """Destroys the session for the user with the given ID.

    Args:
            user_id: The ID of the user whose session should be destroyed.
    """
    try:
        self._db.update_user(user_id, session_id=None)
    except NoResultFound:
        # User not found, nothing to do. Error is already being caught
        pass
