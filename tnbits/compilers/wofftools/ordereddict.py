
#first try loading native OrderedDict (requires Python2.7)
try:
    from collections import OrderedDict
except:
    class OrderedDict(dict):
        """A dict that preserves insert order whenever possible."""
        def __init__(self, *args, **kwargs):
            dict.__init__(self,*args,**kwargs)
            self._keys = []
            if args:
                self._keys.extend([x[0] for x in args[0]])
            if kwargs:
                self._keys.extend(kwargs.keys())

        def __repr__(self):
            return 'OrderedDict([' + u', '.join([u'({0}, {1})'.format(repr(k),repr(self[k])) for k in self._keys]) + '])'

        def __setitem__(self, key, value):
            if key not in self:
                self._keys.append(key)
            dict.__setitem__(self,key,value)

        def copy(self):
            return self.__class__(self)

        def __delitem__(self, key):
            dict.__delitem__(self, key)
            self._keys.remove(key)

        def iteritems(self):
            for item in self._keys:
                yield (item, self[item])

        def items(self):
            return list(self.iteritems())

        def itervalues(self):
            for item in self._keys:
                yield self[item]

        def values(self):
            return list(self.itervalues())

        def iterkeys(self):
            return iter(self._keys)

        def keys(self):
            return list(self._keys)

        def popitem(self):
            key = self._keys[-1]
            value = self[key]
            del self[key]
            return (key, value)


#add a convenience method
def OrderedDictInsert(self, key, value, pos=0):
    if key in self._keys:
        self._keys.remove(key)

    self._keys.insert(pos,key)
    self[key] = value

OrderedDict.insert = OrderedDictInsert
