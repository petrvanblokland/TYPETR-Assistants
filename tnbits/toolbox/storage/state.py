# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     state.py
#
import json
from tnbits.toolbox.transformer import TX

class State(dict):
    """
    The `State` class implements the function of a generic storage class, that has key/value pairs
    available as keyed item and as attribute. The only restriction is that keys should never start with an underscore
    (to make them different from the main instance and class methods). Usage as state[myKey] = 123 or as state.myKey =
    123.
    """
    @classmethod
    def _fromDict(cls, d):
        dd = cls()
        for key, item in d.items():
            dd[key] = item
        return dd

    @classmethod
    def _fromObject(cls, o):
        """
        Recursively transform the dictionaries into a state and leave other objects untouched.
        """
        if isinstance(o, (list, tuple)):
            result = []  # Answer a list of states
            for d in o:
                result.append(cls._fromObject(d))
        elif isinstance(o, dict):
            result = cls()  # Answer a single state
            for key, value in o.items():
                result[key] = cls._fromObject(value)
        else:
            result = o
        return result

    @classmethod
    def _asObject(cls, o):
        """
        Recursively transform states into dictionaries. Convert all other object to standard Python classes.
        """
        if isinstance(o, str):
            result = o
        elif isinstance(o, (list, tuple)):
            result = []
            for oo in o:
                result.append(cls._asObject(oo))
        elif isinstance(o, (cls, dict)):
            result = {}
            for key, item in o.items():
                result[TX.asString(key)] = cls._asObject(item)
        elif isinstance(o, (int, float)):
            result = o
        elif o is None:
            result = 'None'
        else:
            result = repr(o)
        return result

    @classmethod
    def _fromJson(cls, s):
        """
        If ‘s’ evaluates to a list, then assume that the content consists of dictionaries, which all convert to a
        # single state. If ‘s’ evaluates to a dict, then create a single state.
        """
        assert isinstance(s, str)
        return cls._fromObject(json.loads(s))

    def _asJson(self):
        """
        Converts self to an object consisting of standard Python instances, so it can be dumped by JSON.
        """
        return json.dumps(self._asObject(self))

    def _copyFrom(self, data):
        """
        Data can be a State instance or a dict. Only keys without an initial "_" are copied into self. Any existing
        value in self with the same key is overwritten. Other key values are untouched.
        """
        if isinstance(data, State):
            data = self._asObject(data)
        if isinstance(data, dict):
            for key, item in data.items():
                data[key] = item

    def _asDict(self):
        """
        Answers the self attributes as a dictionary.
        """
        return self._asObject(self)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        return self.get(key)

    def get(self, key, default=None):
        """
        Special case, don’t allow attributes named “get” to be compatible with dict, but there is not a reason for
        this otherwise, since non-existing attributes always answer None anyway.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def set(self, key, value):
        # Special case, don’t allow attributes named “set”
        # To be compatible with dictionaries.
        self[key] = value
