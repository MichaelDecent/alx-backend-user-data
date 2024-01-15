#!/usr/bin/env python3
""" This Module contains a class that manages authentication for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True
        path = path.rstrip("/") + "/"
        excluded_paths = [path.rstrip("/") + "/" for path in excluded_paths]

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Return
        """
        if request is None or not request.headers.get("Authorization"):
            return None
        return request  .headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns the current user"""
        return None
