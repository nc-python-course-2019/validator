#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from validator_plugins import type_validator


class ValidateConfigSilly:
    """
    ValidateConfigSilly(config).validate() -> (True|False)
    Silly validator for configuration structure using hard-coded specification
    main algorithm: start -> check_config_type (config_type_ok) ->
        check_1st_lvl (1st_lvl_ok) -> [check_2nd_lvl] (2nd_lvl_ok) -> finish
    check_2nd_lvl algorithm: start -> check_keys_type (keys_type_ok) ->
        check_type_per_key (type_per_key_ok) ->
        check_options_per_key (options_per_key_ok) -> finish
    """

    mapping = {
        'start': '_check_config_type',
        'config_type_ok': '_check_1st_lvl',
        '1st_lvl_ok': '_check_keys_type',
        'keys_type_ok': '_check_type_per_key',
        'type_per_key_ok': '_check_options_per_key',
        'options_per_key_ok': '_finish',
        'finish': '',
    }

    status = {
        'stage': None,
        'error': False,
        'exception': '',
    }

    def validate(self):
        stages = list(self.mapping.keys())
        while not self.status['stage'] == 'finish':
            current = self.status['stage']
            number = stages.index(current)
            print('DEBUG: {}'.format(self.status['stage']))
            if self.status['error']:
                raise self.status['exception']
            step = self.mapping[current]
            getattr(self, step)(self.config)
            self.status['stage'] = stages[number + 1]
        else:
            return True

    def _finish(self, config):
        self.status['stage'] = 'finish'
        return config

    def _check_options_per_key(self, config):
        keys = config['keys']
        assert keys
        result = False
        for key in keys:
            result = self._check_key_options(keys[key])
            if not result:
                break
        return result

    def _check_key_options(self, key):
        required_keys = ['type', 'mandatory']
        result = self._check_keys_in_dict(required_keys, key)
        return result

    def _check_type_per_key(self, config):
        keys = config['keys']
        result = False
        for key in keys:
            result = self._check_type(keys[key], 'dict')
            if not result:
                break
        return result

    def _check_keys_type(self, config):
        keys = config['keys']
        result = self._check_type(keys, 'dict')
        return result

    def _check_1st_lvl(self, config):
        required_keys = ['keys', 'allow_extended']
        result = self._check_keys_in_dict(required_keys, config)
        return result

    def _check_keys_in_dict(self, keys, instance):
        error = 'Missing key "{i}" in object {instance}'
        result = False
        print('DEBUG1: ', keys, instance)
        for i in keys:
            result = i in instance
            if not result:
                self._set_error(KeyError, error.format(**vars()))
                raise KeyError(error.format(**vars()))
        return result

    def _check_config_type(self, config):
        object_type = 'dict'
        result = self._check_type(config, object_type)
        return result

    @staticmethod
    def _check_type(instance, object_type):
        result = type_validator.validate_type(instance, object_type)
        if not result:
            error = 'Object {instance} should be of type {object_type}'
            # self._set_error(TypeError, error.format(**vars()))
            raise TypeError(error.format(**vars()))
        return result

    def _set_error(self, exception, message):
        self.status['error'] = True
        self.status['exception'] = exception(message)

    def __init__(self, config):
        self.config = config
        self.status['stage'] = 'start'


if __name__ == '__main__':
    correct_config = {
        "keys": {
            "var1": {'type': "int", "mandatory": True},
            "var2": {'type': "str", "mandatory": False},
            "var3": {'type': "bool", "mandatory": True},
            "var4": {'type': "bool", "mandatory": False},
            "var5": {'type': "int", "mandatory": True},
            "var6": {'type': "str", "mandatory": False},
            "var7": {'type': "bool", "mandatory": True}
        },
        "allow_extended": True
    }

    validator = ValidateConfigSilly(correct_config)
    validator.validate()
