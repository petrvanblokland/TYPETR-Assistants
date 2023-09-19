# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    handler.py

from logging import Handler, ERROR, WARNING

class BitsHandler(Handler):
    """Custom handler object to connect logging output to a console."""

    def __init__(self, console):
        Handler.__init__(self)
        self.console = console

    def emit(self, record):
        """
        * name – The name of the logger used to log the event represented by
        this LogRecord. Note that this name will always have this value, even
        though it may be emitted by a handler attached to a different
        (ancestor) logger.
        * level – The numeric level of the logging event (one of DEBUG, INFO
        etc.) Note that this is converted to two attributes of the LogRecord:
        levelno for the numeric value and levelname for the corresponding level
        name.
        * pathname – The full pathname of the source file where the logging call
        was made.
        * lineno – The line number in the source file where the logging call was
        made.
        * msg – The event description message, possibly a format string with
        placeholders for variable data.
        * args – Variable data to merge into the msg argument to obtain the event
        description.
        * exc_info – An exception tuple with the current exception information,
        or None if no exception information is available.
        * func – The name of the function or method from which the logging call
        was invoked.

        """
        msg = '> %s\n' % record.getMessage()

        if record.levelno == ERROR:
            self.console.message((msg, 'error'))
        elif record.levelno == WARNING:
            self.console.message((msg, 'warning'))
        else:
            self.console.message(msg)
