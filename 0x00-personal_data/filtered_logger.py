#!/usr/bin/env python3
"""
This module contain a function filter_datum that
returns the log message obfuscated:
"""
from typing import List
import re


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
