# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#     opentype.py
#

import os
import subprocess
from tnbits.qualityassurance.qamessage import addHeader

def sanitiser(stylesDict, ots_path=None, **kwargs):
    """
    Passes binary font file to OpenType Sanitiser.
    #FIXME: use different path for app version.
    """
    messages = []

    for styleId, style in stylesDict.items():
        m =[]

        if styleId.endswith('.ufo'):
            msg = 'ot-sanitise does not accept the UFO format.'
            m.append((msg, 'warning'))
        else:
            path = style.path.replace(' ', '\ ')
            cmd = '%s %s' % (ots_path, path)
            p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()

            if len(err) > 0:
                m.append((err, 'error'))
            elif len(out) > 0:
                m.append((err, 'warning'))

        addHeader("Sanitiser", styleId, m, messages)

    return messages
