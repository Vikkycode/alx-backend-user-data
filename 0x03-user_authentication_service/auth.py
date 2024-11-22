#!/usr/bin/env python3
"""Auth module
"""
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
