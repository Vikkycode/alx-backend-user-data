#!/usr/bin/env python3
""" filter datum """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns the log message obfuscated

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
