#!/usr/bin/env python3
"""This Module contains a function that encrypts a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """This function returns an hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates an hashed password and returns a boolean"""
    return bcrypt.checkpw(b"password", hashed_password)
