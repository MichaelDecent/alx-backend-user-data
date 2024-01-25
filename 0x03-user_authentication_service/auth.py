#!/usr/bin/env python3
"""
This Module handles authtentication functions
"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """Takes in a password string arguments and returns bytes"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str):
        """Regitsers a user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(
                email=email, hashed_password=hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """validated a user"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode("utf-8"), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """creates a database session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """finds and retrieves user by session ID"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """destroys the session"""
        try:
            self._db.update_user(user_id, id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError

        reset_token = _generate_uuid()
        try:
            self._db.update_user(user.id, reset_token=reset_token)
        except Exception:
            return None

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None)
