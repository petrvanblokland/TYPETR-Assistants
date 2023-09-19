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
#    preferencemodel.py
#

from tnbits.base.c import *
from tnbits.bites.qatool.constants import *
from tnbits.bites.qatool.transformer import *
from tnbits.qualityassurance.qamessage import getTitle

preferenceModel = dict()
sort = 10

for category, fs in allFunctions.items():
    for function in fs:
        flagName = getFlagName(category, function)
        title = getTitle(function)
        preferenceModel[flagName] = dict(label=title, default=False,
                type=PREFTYPE_BOOL, sort=sort)
        sort += 10

