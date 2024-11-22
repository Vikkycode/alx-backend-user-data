#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        # Drop existing tables for testing
        Base.metadata.drop_all(self._engine)
        # Create tables
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's emails address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user by the given keyword arguments.

        Args:
            **kwargs: Keyword arguments to filter the user by.

        Returns:
            User: The first user found matching the criteria.

        Raises:
            NoResultFound: If no user matching the criteria is found.
            InvalidRequestError: If the query arguments are invalid.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            raise

    
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Keyword arguments representing the attributes to update.

        Raises:
            ValueError: If an invalid attribute is provided in kwargs.
            NoResultFound: If no user with the given ID is found.
        """
        try:
            user = self.find_user_by(id=user_id)

            valid_attributes = ["email", "hashed_password"]  # List of updatable attributes
            for key, value in kwargs.items():
                if key not in valid_attributes:
                    raise ValueError("Invalid attribute provided")
                setattr(user, key, value)

            self._session.commit()

        except NoResultFound:
            raise