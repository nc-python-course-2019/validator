#!/usr/bin/env python
# -*- coding: utf-8 -*-


from validator_plugins import type_validator
from validator_plugins import regex_validator
from pprint import pprint


class ValidateConfig:
    """
    ValidateConfig(config, specification) -> (True|(False + Exception))
    config - config object (any)
    specification - config specification (dict)

    ValidateConfig checks if the config meets the specification
    Specification should represent the following structure:
        {
                'type': 'dict',
                'allow_extended': False,
                'keys': {
                    'key_description1': key_specification1,
                    'key_description2': key_specification2,
                    ... etc ...
                }
        }

        type - str
        allow_extended - bool
        keys - list
        key_specificationN - dict

    Key_specificationN should represent the following structure:
        'key_description1': {
            'name': 'keys',
            'mandatory': True,
            'name_strict': True,
            'type': 'dict',
            'has_children': True,
            'parent': None,
        }

        'key_description2': {
            'name': 'type',
            'mandatory': True,
#            'name_strict': True,         obsolete?
            'type': 'str',
            'has_children': False,
            'parent': ('keys', 'fields'),
        },

    Fields explanation:
        type -  literal representation of object that the config is expected
                to be
                Allowed values: 'list', 'dict', 'tuple' etc

        allow_extended - is the config allowed to contain non-described keys
                Allowed values: bool

        keys - specification list, that contains specification for keys in
                config
                Allowed values: list with key specifications inside

        key_specificationN - specification of a key that config is expected to
                contain
                Allowed values: dict with a key specification inside

        name - name of a key that config is expected to contain (can be a regex).
                In case that key is part of non-named collection
                (list, tuple etc) it should represent sequential number of
                element
                Allowed values: string

        key_description - key description. This value is used in the
                key 'parent' in key specifications to represent key hierarchy.
                Allowed values: string

        mandatory - indicates whether a key existence is required
                Allowed values: bool

 #       name_strict - indicates whether field 'name' represents the real name
 #               of a key
 #               Allowed values: bool

        has_children - indicates whether the key has substitute keys
                Allowed values: bool

        parent - tuple, that specifies key's location in the config tree
                Allowed values: tuple
    """

    def check_config(self):
        """
        checks if the specification has a proper skeleton
        :return: bool
        """
        pass

    def _check_keys(self):
        """
        main worker for check_keys
        """
        for spec in self.specification['keys']:
            self._check_key(spec)

    def _check_key(self, key_specification):
        """
        check key in self.config using it's specification
        key_specification:  - dict
        return              - bool
        """
        hierarchy = key_specification['parent']
        possible_elements = self
        pass

    def _get_keys_from_hierarchy(self, hierarchy):
        """
        search keys in self.config using hierarchy specification
        hierarchy    - list
        return       - list
        """
        layer0 = self._get_keys_from_object(self.config)
        if not hierarchy:
            return layer0
        keys = self.specification['keys']
        for layer in hierarchy:
            key_pattern = keys[layer]['name']
            self._get_keys_from_object(self.config)

    def _get_keys_from_object(self, _object):
        try:
            keys = list(_object.keys())
        except AttributeError:
            keys = [i for i in rage(len(_object))]
        return keys

    def _search_pattern(self, _list, pattern):
        """
        search for pattern in _list
        _list   - list
        pattern - regex pattern
        return  - list of matched elements
        """
        result = []
        for element in _list:
            _str = str(element)
            if self._check_name(_str, pattern)
                result.append(element)
        return result

    def _check_name(self, name, template):
        result = self.regex_checker(name, template)
        # if not result:
        #     message = 'Name {name} does not meet the pattern {template}'
        #     self._set_error(ValueError, message.format(**vars()))
        return result

    def _check_type(self, _object, expected_type):
        result = self.type_checker(_object, expected_type)
        if not result:
            message = 'Object {_object} is not {expected_type'
            self._set_error(TypeError, message.format(**vars()))
        return result

    def _set_flags(self):
        self.flags['allow_extended'] = self.specification['allow_extended']
        return True

    def _set_error(self, exception, message):
        """
        set the state to Error
        exception   - class Exception
        message    - error message
        """
        self.current_status['error'] = True
        self.current_status['error_out'] = message
        raise exception(message)

    def __init__(self, config, specification):
        self.config = config
        self.specification = specification

    current_status = {
        'error': None,
        'error_out': '',
        'specification_checked': False,
        'config_checked': False,
    }

    regex_checker = regex_validator.validate_by_regex
    type_checker = type_validator.validate_type

    flags = {
        'allow_extended': None,
    }

    master_specification = {
        'type': 'dict',
        'allow_extended': False,
        'keys': {
            'config_type': {
                'name': 'type',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'str',
                'has_children': False,
                'parent': None,
            },
            'allow_extended': {
                'name': 'allow_extended',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'bool',
                'has_children': False,
                'parent': None,

            },
            'keys': {
                'name': 'keys',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'list',
                'has_children': True,
                'parent': None,

            },
            'key_specification': {
                'name': '\d+',
                'mandatory': True,
                # 'name_strict': False,
                'type': 'dict',
                'has_children': True,
                'parent': ('keys',),
            },
            'description': {
                'name': 'description',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'string',
                'has_children': False,
                'parent': ('keys', 'key_specification')
            },
            'name': {
                'name': 'name',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'string',
                'has_children': False,
                'parent': ('keys', 'key_specification')
            },
            'mandatory': {
                'name': 'mandatory',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'bool',
                'has_children': False,
                'parent': ('keys', 'key_specification')
            },
            'name_strict': {
                'name': 'name_strict',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'bool',
                'has_children': False,
                'parent': ('keys', 'key_specification')
            },
            'key_type': {
                'name': 'type',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'string',
                'has_children': False,
                'parent': ('keys', 'key_specification')
            },
            'has_children': {
                'name': 'has_children',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'bool',
                'has_children': False,
                'parent': ('keys', 'key_specification')
            },
            'parent': {
                'name': 'parent',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'tuple',
                'has_children': False,
                'parent': ('keys', 'key_specification')
            },

        }
    }

    specification = None
    config = None

if __name__ == '__main__':
    a = ValidateConfig({}, {})
    pprint(type(a.type_checker))

    correct_config = {
        "keys": {
            "var1": {type: "int", "is_optional": True},
            "var2": {type: "str", "is_optional": False},
            "var3": {type: "bool", "is_optional": True},
            "var4": {type: "bool", "is_optional": False},
            "var5": {type: "int", "is_optional": True},
            "var6": {type: "str", "is_optional": False},
            "var7": {type: "bool", "is_optional": True}
        },
        "allow_extended": True
    }

    config_specification = {
        'type': 'dict',
        'allow_extended': False,
        'keys': [
            {
                'description': 'keys',
                'name': 'keys',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'dict',
                'has_children': True,
                'parent': None,
            },
            {
                'description': 'allow_extended',
                'name': 'allow_extended',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'bool',
                'has_children': False,
                'parent': None,

            },
            {
                'description': 'fields',
                'name': 'fields',
                'mandatory': False,
                # 'name_strict': False,
                'type': 'dict',
                'has_children': True,
                'parent': ('keys',),
            },
            {
                'description': 'type',
                'name': 'type',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'str',
                'has_children': False,
                'parent': ('keys', 'fields'),
            },
            {
                'description': 'is_optional',
                'name': 'is_optional',
                'mandatory': True,
                # 'name_strict': True,
                'type': 'bool',
                'has_children': False,
                'parent': ('keys', 'fields'),
            },
        ]
    }

    def validate_config(config, specification):
        """
        validate_config(config, specification) -> (True|(False + Exception))
        config - config object (any)
        specification - config specification (dict)

        validate_config checks if the config meets the specification
        """
