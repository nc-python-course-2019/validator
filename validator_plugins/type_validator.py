#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
provides set of functions to check if some object represents some class
"""

def validate_type(instance, reference):
    """
    validate_type(instance, reference) -> (True|False)
    instance - some object
    reference - literal reference to a class (str)

    validate_type - determines whether 'instance' is an instance of the specified
                    'reference' class or not
    """
    return type(instance).__name__ == reference

def get_reference(caller):
    """
    get_reference(caller) -> string
    get_reference returns literal reference to the caller's (class) name
    """
    reference = type(caller).__name__
    if type(caller).__name__ == 'type':
        reference = type(caller()).__name__
    return reference
