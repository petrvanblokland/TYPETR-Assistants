#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    log.py
#

class Log(object):
    """
    Logging and errors.
    """

    def fails(self, test, text=None):
        """
        The @fails@ method tests *test* to be @True@. If not, then the *text*
        is printed to the error output. The negated *test* value is answered as
        “error” value.
        """
        if not test is True and text is not None:
            self.message('Fail: ' + text, isError=True)
        return not test # Test id error is True

    def invalidate(self):
        self.valid = False

    def isValid(self):
        return self.valid

    def message(self, msg, isError=False):
        msg = '' + self.gstate.conditionalLevel * '\t' + msg
        self.log(msg)
        if isError is True:
            self.error(msg)

    def resetLogs(self):
        self.i = 0
        self.lastInstructions = []
        self._log = []
        self._errors = []
        self.loopIndices = {}

    def log(self, msg):
        """
        Keeps track of log.
        """
        self._log.append(str(self.i).rjust(4).ljust(7) + msg)
        self.i += 1

    def error(self, msg):
        """
        Keeps track of errors.
        """
        if self.valid is True:
            self.valid = False
            self._errors.append('An error occured:')

        print(msg)
        self._errors.append(msg)

    def getLog(self):
        return '\n'.join(self._log)

    def getError(self):
        if len(self._errors) > 0:
            return '\n'.join(self._errors)
        else:
            return ''

