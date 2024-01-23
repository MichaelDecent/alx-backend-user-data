import bcrypt

def _hash_password(password: str):
    """takes in a password string arguments and returns bytes
    """
    return bcrypt.hashpw(b"password", bcrypt.gensalt())
