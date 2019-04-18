#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Validate:
    mapping = {
        "int": "check_int",
        "str": "check_string",
        "bool": "check_bool"
    }

    @staticmethod
    def check_int(value):
        if type(value) is int:
            return True
        return False

    @staticmethod
    def check_string(value):
        if type(value) is str:
            return True
        return False

    @staticmethod
    def check_bool(value):
        if type(value) is bool:
            return True
        return False

    def check(self, config, request):
        for key, value in request.items():
            if key not in config.keys():
                return {"error": "Unknown field {}".format(key)}
            if config[key] not in self.mapping.keys():
                return {"error": "Unknown type of field {}".format(key)}

            func = getattr(self, self.mapping[config[key]])

            if func(value) is False:
                return {"error": "Field {} should be {}".format(key, config[key])}

        return {"status": "success"}


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

correct_request = {
    "var1": 10,
    "var2": "str",
    "var3": True,
    "var4": True,
    "var5": 5,
    "var6": "True"

}


validator = Validate()
print(validator.check(correct_config, correct_request))