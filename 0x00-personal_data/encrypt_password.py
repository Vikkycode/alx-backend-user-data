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
