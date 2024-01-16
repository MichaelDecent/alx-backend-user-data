#!/usr/bin/env python3
"""
This module contain a functions that handles personal data filters and
returns the log message obfuscated
"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "ssn", "password", "phone")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    returns the log message obfuscated
    """
    for pii_data in fields:
        message = re.sub(rf"{pii_data}=([^{separator}]*)",
                         f"{pii_data}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the instance with logging.Formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filter values in incoming log records using filter_datum
        and return a sring in a specifed format
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """creates a logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """creates a database connection"""
    try:
        db_connection = mysql.connector.connect(
            host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
            user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
            password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
            database=os.getenv("PERSONAL_DATA_DB_NAME", ""),
        )
        return db_connection
    except Exception as error:
        print(error)


def main() -> None:
    """
    obtain a database connection using get_db and retrieve
    all rows in the users table and display each row
    """
    db_connection = get_db()
    logger = get_logger()

    with db_connection.cursor() as cursor:
        cursor.excute('SELECT * FROM users;')
        rows = cursor.fetchall()

        for row in rows:
            each_row = RedactingFormatter(PII_FIELDS)
