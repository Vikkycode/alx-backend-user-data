#!/usr/bin/env python3
"""
This module defines the User class, mapping to the 'users' table
in a SQL database using SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): Unique identifier for the user.
        email (str): User's email address.
        hashed_password (str): User's hashed password.
        session_id (str): User's session ID for authentication.
        reset_token (str): Token for password reset.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
