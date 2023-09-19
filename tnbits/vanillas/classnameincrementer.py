# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     classnameincrementer.py
#

"""Ever been annoyed by this when reloading a module?

   error: MyNSObject is overriding existing Objective-C class

This is a hack that allows modules that contain NSObject subclasses to be
reloaded after all. All that's need is a little metaclass hook/hack:


from Foundation import NSObject

from tnbits.vanillas.classnameincrementer import ClassNameIncrementer

class MyNSObject(NSObject):
    __metaclass__ = ClassNameIncrementer
    # your stuff

print(MyNSObject)
# first time this prints MyNSObject, then MyNSObject1, then MyNSObject2, etc.


The way this works is that it is being checked whether the class already exists,
and if so, look for the next <classname><number> that is free. Internally, the
class will be called that (hence what you see when you print(the class), but the)
variable name in the module is still the "normal" one, so external code doesn't
have to deal with this.

This is handy during development. No more restarting RF, DB, whatever environment
you're working in, just reload(module) like you would otherwise do with a module.

** WARNING **
I *strongly* advise you to **NOT** use this in production in **main scripts** (a
new class will be created every single time you run the script, which is
ridiculous), but only in modules that you intend to reload while developing.
It's harmless if you don't reload, the class will then even internally have
its "proper" name.
"""


def ClassNameIncrementer(clsName, bases, dct):
    import objc
    orgName = clsName
    counter = 0
    while True:
        try:
            objc.lookUpClass(clsName)
        except objc.nosuchclass_error:
            break
        counter += 1
        clsName = orgName + str(counter)
    return type(clsName, bases, dct)
