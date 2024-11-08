#!/usr/bin/env python3
""" Hash password. """
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the given password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted and hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validates if a given password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The password to check.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
