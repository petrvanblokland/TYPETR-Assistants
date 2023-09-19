# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#            writer.py
#
#    Behaves like s cStringIO write buffer, but we need it to check for
#    normal an unicode strings.
#    The stringIO buffer will automatically close when the instance is deleted.
#
from cStringIO import StringIO
import codecs, gzip

class Writer(object):

    def __init__(self):
        self.reset()

    def __del__(self):
        self.close()

    def reset(self):
        """
        The `reset` method resets the data of the writer. This can be used
        to reset the content of a shared (through cloning) builder, where the output
        stream is divided into parts, such as the export of PHP files.
        """
        self.buffer = StringIO()
        self.writer = codecs.getwriter("utf-8")(self.buffer)

    def getValue(self, decode=None):
        if decode is not None:
            return self.writer.getvalue().decode(decode)
        return self.writer.getvalue()

    def getCompressedValue(self, decode=None):

        zbuf = StringIO()
        zfile = gzip.GzipFile(fileobj=zbuf,mode='wb')

        if decode is not None:
            zfile.write(self.writer.getvalue().decode(decode))
        else:
            zfile.write(self.writer.getvalue())

        zfile.close()

        content = zbuf.getvalue()
        zbuf.close()

        return content


    def binary(self, obj):
        if obj is not None:
            if not isinstance(obj, str):
                obj = str(obj)
            self.buffer.write(obj)

    def write(self, s):
        """
        Write the object s.
        """
        if s is not None:
            if not isinstance(s, str):
                s = str(s)
            try:
                self.writer.write(s)
            except:
                s = s.decode('utf-8')
                self.writer.write(s)

    def close(self):
        if self.writer is not None:
            self.buffer.close()
            self.buffer = None
            self.writer = None

