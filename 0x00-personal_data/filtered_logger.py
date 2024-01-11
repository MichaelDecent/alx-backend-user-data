#!/usr/bin/env python3
"""
This module contain a function filter_datum that
returns the log message obfuscated:
"""
from typing import List, Sequence
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "ssn", "password", "phone")


def filter_datum(fields: List[str],
                 redaction: str,
                 message: List[str],
                 separator: str) -> str:
    """
    returns the log message obfuscated
    """
    for pii_data in fields:
        message = re.sub(rf'{pii_data}=([^{separator}]*)',
                         f'{pii_data}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Sequence[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    creates a logger
    """
    logger = logging.getlogger('user_data')
    logger.setlevel(logging.INFO)

    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    creates a database connection
    """
    db_connection = mysql.connector.connect(
          host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
          user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
          password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
          database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connection
