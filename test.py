#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pprint import pprint
from validator_plugins import regex_validator

class SearchPossibleObjects:

    def _search(self, _object, _sequence):
        """
        main worker
        """
        for pattern in _sequence:
            object_keys = self._get_object_keys(_object)
            # [[ :keys of object:]]
            matched_keys = self._search_keys_by_pattern(object_keys, pattern)
            # [[ :keys that match the pattern: ]]
            subsequent_objects = [_object[key] for key in matched_keys]
            # [[ :list of matched object on this layer: ]]
            # process these object with _sequence[1:]
            # pprint('DEBUG: Turn: {c};\nsubsequent_objects: {subsequent_objects}'.format(**vars()))
            if len(_sequence) > 1:
                result = []
                for _sub_object in subsequent_objects:
                    result.append(self._search(_sub_object, _sequence[1:]))
                    # print('DEBUG4: positive')
            else:
                result = subsequent_objects
                # print('DEBUG4: negative; ' + str(subsequent_objects))
            # print('DEBUG5: returning result: ' + str(result))
            return result

    def run(self):
        return self._search(self._object, self._sequence)


    def _get_object_keys(self, _object):
        """
        get a list of keys that object contains
        _object - collection
        return  - list
        """
        try:
            keys = list(_object.keys())
        except AttributeError:
            keys = [i for i in range(len(_object))]
        return keys

    def _search_keys_by_pattern(self, _list, pattern):
        """
        search a pattern in a list of strings or ints
        _list   - list with strings or ints
        pattern - regex (str)
        return  - list of matched values
        """
        result = []
        # print('DEBUG1: list = ' + str(_list))
        for i in _list:
            _string = str(i)
            # print('DEBUG1: key = ' + _string)
            # print('DEBUG1: pattern = ' + pattern)
            if self.regex_checker(_string, pattern):
                result.append(i)
                # print('DEBUG2: matched')
        # pprint('DEBUG3: result = ' + str(result))
        return result

    def __init__(self, _object, _sequence):
        self._object = _object
        self._sequence = _sequence

    _object = None
    _sequence = None
    regex_checker = regex_validator.validate_by_regex


if __name__ == '__main__':

    d = {
            'foo': {
                'foo1': [
                    'foo11',
                    'foo12',
                ],
                'foo2': {
                    'foo21': [
                        {
                            'bar211': 'val211',
                            'foo212': 'val212',
                        },
                        {
                            'bar213': [
                                'val213a',
                                'val213b',
                            ]
                        }
                    ]
                }
            }
        }

    tree = [
        d['foo'],
        d['foo']['foo1'],
        d['foo']['foo1'][0],
        d['foo']['foo1'][1],
        d['foo']['foo2'],
        d['foo']['foo2']['foo21'][0],
        d['foo']['foo2']['foo21'][0]['bar211'],
        d['foo']['foo2']['foo21'][0]['foo212'],
        d['foo']['foo2']['foo21'][1],
        d['foo']['foo2']['foo21'][1]['bar213'],
    ]


    sequence = ['foo','f.*2', 'foo21', '\d+', 'bar.*']

    import pdb
    search = SearchPossibleObjects(d, sequence)
    # pdb.set_trace()
    result = search.run()
    print('RESULT:')
    pprint(result)