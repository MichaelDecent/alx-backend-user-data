#!/usr/bin/env python3
"""
This Module handles authtentication functions 
"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str):
    """Takes in a password string arguments and returns bytes"""
    return bcrypt.hashpw(b"password", bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Regitsers a user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(
                email=email, hashed_password=hashed_password)
