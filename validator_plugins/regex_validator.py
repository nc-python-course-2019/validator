#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
provides function to check if a string matches a regular expression
"""

from re import match

@staticmethod
def validate_by_regex(string, regex):
    """
    checks if a string matches the regular expression
    validate_by_regex(string, regex) -> (True|False)
    string     - some text string (str)
    regex       - regular expression (str)
    :return:
    """
    return bool(match(regex, string))