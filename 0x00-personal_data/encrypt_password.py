#!/usr/bin/env python3
"""This Module contains a function that encrypts a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """This function returns an hashed password"""
    hashed = bcrypt.hashpw(b"password", bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates an hashed password and returns a boolean"""
    if bcrypt.checkpw(b"password", hashed_password):
        return True
    return False
