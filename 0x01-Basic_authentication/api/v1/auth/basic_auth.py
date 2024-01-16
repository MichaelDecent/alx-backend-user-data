#!/usr/bin/env python3
"""
This Module contains a class that manages basic authentication for the API
"""
from .auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    This class inherites from Auth Base class and handle basic authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """
        Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None or type(
                authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Returns the decoded value of a Base64
        string base64_authorization_header which the username and password
        """
        if (
            base64_authorization_header is None
            or type(base64_authorization_header) is not str
        ):
            return None
        try:
            decoded_string = base64.b64decode(
                base64_authorization_header, validate=True
            )
            return decoded_string.decode("utf-8")
        except binascii.Error:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value.
        """
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) is not str
        ):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """
        Returns the the User instance based on his email and password
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        user_credentials = {"email": user_email}
        current_user = User.search(user_credentials)
        if len(current_user) <= 0:
            return None
        if not current_user[0].is_valid_password(user_pwd):
            return None
        return current_user[0]
    
    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieves the current user object
        """
        header = self.authorization_header(request)
        encoded_string  = self.extract_base64_authorization_header(header)
        user_credentials = self.decode_base64_authorization_header(encoded_string)
        user_email, user_pwd = self.extract_user_credentials(user_credentials)
        return self.user_object_from_credentials(user_email, user_pwd)
