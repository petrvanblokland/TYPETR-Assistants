#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#       from https://github.com/fonttools/fonttools/
#                                   blob/master/Lib/fontTools/varLib/mutator.py
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#    dstest.py
#
from tnbits.model.objects.dsmodel import Model, DesignSpace

default = 'Amstelvar-Roman.ufo'

ds = DesignSpace(path='Amstelvar-Roman.designspace')
for tag, axis in ds.axes.items():
    print(tag, axis)
