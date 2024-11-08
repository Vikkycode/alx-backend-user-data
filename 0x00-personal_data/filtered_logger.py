#!/usr/bin/env python3
"""Filtering log messages."""
import re
import logging
from typing import List
import mysql.connector
import os


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


def get_logger() -> logging.Logger:
    """Return a logging.Logger object.

    Returns:
        logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a connector to the database.

    Returns:
        mysql.connector.connection.MySQLConnection object
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


def main() -> None:
    """Obtain a database connection and retrieve all rows in the users table.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [field[0] for field in cursor.description]
    logger = get_logger()

    for row in cursor:
        message = ''
        for i, value in enumerate(row):
            message += f'{fields[i]}={value}; '
        logger.info(message.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
