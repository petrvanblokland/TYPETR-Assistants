# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    TnBits
#    (c) 2010+ buro@petr.com, www.petr.com
#
#    T N  B I T S
#    No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    console.py
#

import datetime
from AppKit import NSFontAttributeName, NSForegroundColorAttributeName,\
NSAttributedString, NSColor, NSFont #NSFontWeightLight, NSFontWeightBold
from vanilla import Group, TextEditor, CheckBox
from vanilla.dialogs import putFile
from tnbits.base.constants.colors import *
from tnbits.base.constants.tool import *
from tnbits.base.future import chr

class Console(object):
    """Provides a text editor with a terminal look and feel. Features:

    * different font weights and colors using attributed strings,
    * Unicode support,
    * prefixed indentation for nested list,
    * summation of errors / warinings,
    * optionally saves contents to file.

    Lines are collected through te message() and messageList() functions, or
    directly using addLine(). After text data has been collected lines are
    executed by setLines().

    TODO: add more line types.
    """

    # Colors, fonts & formatting.

    prefixes =['*', '+', '-']
    fontSize = 11

    # TODO: auto install mono font and set up for bold, emphasis, &c (#479).
    f = NSFont.fontWithName_size_("Andale Mono", fontSize)
    fb = NSFont.fontWithName_size_("Andale Mono", fontSize)

    if not f:
        f = NSFont.systemFontOfSize_(fontSize)

    if not fb:
        fb = NSFont.boldSystemFontOfSize_(fontSize)

    # System fonts.
    fonts = {
        'regular': f,
        'bold': fb
    }

    def __init__(self, controller, pos=(0, 0, -0, -0), doVerbose=True,
            suppressWarnings=False, verboseCallback=None, showFlags=True,
            suppressCallback=None, preferencesCallback=None, addDateTime=False):
        """Stores reference to controller, sets up console text area plus
        buttons.

        TODO: pass controller variables as callbacks to constructor.
        """
        self._doVerbose = doVerbose
        self._doSuppressWarnings = suppressWarnings
        self.showFlags = showFlags
        self.verboseCallback = verboseCallback
        self.suppressCallback = suppressCallback
        self.preferencesCallback = preferencesCallback
        self.addDateTime = addDateTime
        self.controller = controller
        self.lines = []
        self.stackTrace = ''
        self.view = Group(pos)
        x, y, w, h = pos
        self.view.console = TextEditor((x, y, w, h), '')
        textView = self.view.console.getNSTextView()
        textView.setRichText_(True)
        textView.setBackgroundColor_(NSColor.blackColor())


    def getView(self):
        """Returns top view object (is a group)."""
        return self.view

    def show(self, doShow=True):
        hidden = not doShow
        self.view.getNSView().setHidden_(hidden)

    # Messages and lines.

    def dateTimeMessage(self, message):
        if self.addDateTime:
            dt = datetime.datetime.now().strftime("%d-%m '%y %H:%M ")
            message = dt + message
        return message

    def setLines(self, clear=False, numberOfLines=None):
        """Main function, sets stored lines to text area."""
        textView = self.getView().console.getNSTextView()
        numberOfWarnings = 0
        numberOfErrors = 0
        self.doLine(textView, '', clear=True)

        if clear:
            return

        if numberOfLines is None:
            lines = self.lines

        else:
            if numberOfLines < len(self.lines):
                lines = self.lines[-numberOfLines:]
            else:
                lines = self.lines


        # Verbose report of collected results.
        # TODO: set lines all at once, should be much faster. How to set
        # different types of attributed strings at the same time?
        for message, lineType in lines:
            message = self.dateTimeMessage(message)

            if lineType != 'error' and lineType != 'warning':
                if self._doVerbose:
                    self.doLine(textView, message, lineType)

            if lineType == 'warning':
                if self._doVerbose and not self._doSuppressWarnings:
                    self.doLine(textView, message, lineType)

                numberOfWarnings += 1

            if lineType == 'error':
                if self._doVerbose:
                    self.doLine(textView, message, lineType)

                numberOfErrors += 1

        if self.stackTrace != '':
            # Got a traceback, report!
            attrs = self.getAttributes(lineType='error')
            t = self.stackTrace
            a = NSAttributedString.alloc().initWithString_attributes_(t, attrs)
            textView.textStorage().appendAttributedString_(a)

        if self.showFlags:
            message = '\n%d flags\n' % numberOfErrors
            self.doLine(textView, message, 'error')

            message = '%d warnings\n' % numberOfWarnings
            self.doLine(textView, message, 'warning')

    def message(self, msg, lineType='plaintext', debug=False, prefixes=None):
        """Stores new message in console lines to show them after QA has
        finished. Recursive treatement through messageList in case of lists.
        """
        if msg is None:
            return
        elif isinstance(msg, tuple):
            self.addLine(msg)
        elif isinstance(msg, list):
            self.messageList(msg, prefixes=prefixes)
        elif isinstance(msg, str):
            self.addLine((msg, lineType))

    def messages(self, msgs):
        for msg in msgs:
            self.message(msg)

    def messageList(self, messages, numberOfIndents=0, prefixes=None):
        """Adds indentation to lists of messages while handling line type
        formats. Rotates over prefix types when indenting."""
        newline = '\n'
        tab = '\t'
        indent = numberOfIndents * tab
        p = numberOfIndents % 3

        if prefixes is None:
            prefixes = self.prefixes
        prefix = prefixes[p]

        for msg in messages:
            if msg is None:
                return
            elif isinstance(msg, list):
                self.messageList(msg, numberOfIndents=numberOfIndents+1)
                continue
            elif isinstance(msg, tuple):
                msg, lineType = msg
                msg = '%s%s %s%s' % (indent, prefix, msg, newline)
                self.addLine((msg, lineType))
            elif isinstance(msg, str):
                msg = '%s%s %s%s' % (indent, prefix, msg, newline)
                self.addLine((msg, 'plaintext'))

    def addLine(self, msg):
        """Add a message as a line to output later."""
        self.lines.append(msg)

    def getLines(self):
        return self.lines

    def getUnicodeText(self):
        txt = u''
        lines = self.getLines()

        for line, lineType in lines:
            txt += '%s\n' % line

        return txt

    def doLine(self, textView, message, lineType='plaintext', clear=False):
        """Gets corresponding attributes for line and sets the text or adds
        the text to the area."""
        a = self.getAttributedString(message, lineType)

        if clear:
            textView.textStorage().setAttributedString_(a)
        else:
            textView.textStorage().appendAttributedString_(a)

    def clearLines(self):
        """Resets everything to nothing."""
        self.lines = []
        self.stackTrace = ''
        self.setLines(clear=True)

    # Stack trace.

    def setStackTrace(self, msg):
        self.stackTrace = msg

    def showError(self, e, msg, clear=True):
        if clear is True:
            self.clearLines()

        emsg = 'Encountered %s: %s' % ((e.__class__.__name__, str(e)))
        self.message((emsg, 'error'))
        self.message('\n\n')
        self.setStackTrace(msg)
        self.setLines()

    # Attributed strings.

    def getAttributedString(self, message, lineType):
        """Combined message text and line type to form an
        NSAttributedString."""
        attrs = self.getAttributes(lineType)
        return NSAttributedString.alloc().initWithString_attributes_(message, attrs)

    def getAttributes(self, lineType='plaintext'):
        """Returns color and font for line type."""
        if lineType == 'plaintext':
            font = self.fonts['regular']
            color = grayColor
        elif lineType == 'error':
            font = self.fonts['bold']
            color = redColor
        elif lineType == 'warning':
            font = self.fonts['regular']
            color = greenColor
        elif lineType == 'highlight':
            font = self.fonts['bold']
            color = yellowColor
        elif lineType == 'header':
            font = self.fonts['bold']
            color = cyanColor
        elif lineType == 'system':
            font = self.fonts['bold']
            color = magentaColor

        return {NSFontAttributeName: font, NSForegroundColorAttributeName: color}

    # Callbacks.

    def clear(self):
        self.setLines(clear=True)

    def save(self, fileName='console.txt'):
        size = (600, 300)
        window = self.controller.getTool().getWindow()
        putFile(messageText='Save console file', title='Save console as...',
                fileName=fileName, parentWindow=window,
                resultCallback=self.saveDoCallback)

    def saveDoCallback(self, path, mode='plaintext'):
        """Writes console lines to plain text.

        TODO: implement other formats, such as RTF, HTML.
        """
        f = open(path, 'w')

        for message, _ in self.getLines():
            f.write(message.encode('utf-8'))

        f.close()
