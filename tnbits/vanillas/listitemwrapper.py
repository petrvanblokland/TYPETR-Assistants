from Foundation import NSObject


class ListItemWrapper(NSObject):

    def __new__(cls, obj, dependencies=None):
        return cls.alloc().init()

    def __init__(self, obj, dependencies=None):
        self._obj = obj
        self._dependencies = dependencies

    def wrappedObject(self):
        return self._obj

    def setValue_forKey_(self, value, key):
        setattr(self._obj, key, value)
        if self._dependencies is not None:
            for depKey in self._dependencies.get(key, []):
                self.willChangeValueForKey_(depKey)
                self.didChangeValueForKey_(depKey)

    def valueForKey_(self, key):
        try:
            return getattr(self._obj, key)
        except AttributeError:
            return super(ListItemWrapper, self).valueForKey_(key)

    def __getattr__(self, key):
        value = getattr(self._obj, key)
        def _getter():
            return value
        return _getter
