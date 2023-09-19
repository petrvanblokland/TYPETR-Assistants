# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    mnemonic.py
#
class Mnemonic(object):
    """
    Wraps a TrueType hinting opcode instance, implemented in the Instruction class.
    """

    def __init__(self, id, code, attrs, skip, popTypes, pushTypes, method, vtt, base, freeName, comment):
        """
        id | code | attrs | skip | pop | push | method | vtt | base | freename | comment

        Mnemonic(C.NPUSHB, 0x40, [], None, None, None, 'npushb', 'NPUSHB[]', 'NPUSHB[]', '...', 'Push N Bytes'),
        Mnemonic(C.NPUSHW, 0x41, [], None, None, None, 'npushw', 'NPUSHW[]', 'NPUSHW[]', '...', 'Push N Words'),
        """
        self.id = id
        self.code = code
        self.attrs = attrs
        self.skip = skip
        self.popTypes = popTypes
        self.pushTypes = pushTypes
        self.method = method
        self.vtt = vtt
        self.base = base # TTX
        self.freeName = freeName
        self.comment = comment

    def __repr__(self):
        return '[Mnemonic id: %s, code: %s, skip: %s, pop types: %s, push types: %s]\n\n %s\n ** %s **\n\n'\
             % (self.id, self.code, self.skip, self.popTypes, self.pushTypes, self.freeName.upper(), self.comment)

    def isPush(self):
        return 'PUSH' in self.id.upper()

    def isCall(self):
        return 'CALL' in self.id.upper()

    def asTemplate(self):
        """
        TODO: what is this for? Used / deprecated?
        """
        s = [self.freeName]

        if self.popTypes:
                s += self.popTypes

        if self.comment or self.pushTypes:
                s.append('# ')
                if self.pushTypes:
                        s.append('Push:')
                        s += self.pushTypes
                if self.comment:
                        s.append(self.comment)

        return ' '.join(s)

    def getAttribute(self, index):
        return self.attrs[index]
