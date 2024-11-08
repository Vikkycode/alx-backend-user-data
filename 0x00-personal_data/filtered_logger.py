#!/usr/bin/env python3
""" filter datum """
import re


def filter_datum(fields, redaction, message, separator):
    regex_fields = "|".join(fields)
    regex = rf"(?<=[{separator}])({regex_fields})=.*?(?=[{separator}]|$)"
    return re.sub(regex, rf"\1={redaction}", message)
