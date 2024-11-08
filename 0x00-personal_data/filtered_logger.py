#!/usr/bin/env python3
"""Filtering log messages."""
import re
import logging
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = None) -> None:
        """Initialize Redacting Formatter."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields or PII_FIELDS

    def format(self, record: logging.LogRecord) -> str:
        """Format log records."""
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message, (
            self.SEPARATOR)
        )


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Return the log message obfuscated.

    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
        fields in the log line (message)

    Returns:
        The log message obfuscated
    """
    regex_fields = "|".join(fields)
    regex = rf"(?<=[{separator}])({regex_fields})=.*?(?=[{separator}]|$)"
    return re.sub(regex, rf"\1={redaction}", message)
