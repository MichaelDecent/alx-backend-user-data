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
    """Connect to database and return its connector"""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pass = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    connection = mysql.connector.connect(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_pass,
            database=db_name
    )
    return connection


def main() -> None:
    """
    obtain a database connection using get_db and retrieve
    all rows in the users table and display each row
    """
    db_connection = get_db()
    logger = get_logger()
    filtered_field = "name,email,phone,ssn,password,ip,last_login,user_agent"
    field_titles = filtered_field.split(',')
    sql_query = f'SELECT {filtered_field} FROM users;'
    with db_connection.cursor() as cursor:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        for row in rows:
            msg = map(
                lambda title, value: f"{title}={value}; ", field_titles, row)
            message = ''.join(list(msg))
            args = ("user_data", logging.INFO, None, None, message, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)


if __name__ == ('__main__'):
    main()
