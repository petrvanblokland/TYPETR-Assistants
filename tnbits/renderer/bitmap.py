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
#    bitmap.py
#
from PIL import Image

def bitmapToPNG(bitmap, folder, fileName):
    """Converts a two-dimensional bitmap array with values in range 0-255 to a
    PNG file."""
    tuples = []

    if len(bitmap) == 0:
        return

    for row in bitmap:
        for value in row:
            tuples.append((value, value, value))

    newimage = Image.new('RGB', (len(bitmap[0]), len(bitmap)))
    newimage.putdata(tuples)
    newimage.save("%s/%s.png" % (folder, fileName))
