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
#    constants.py
#

# TODO: add fontMake and fontTools version to outputs.
#
fontmake_folders = ['master_ttf_interpolatable', 'variable_ttf']

# TODO: autohint, subset, mark_writer_class, kern_writer_class,
# conversion_error

options = {
        'use_production_names': False,
        'remove_overlaps': True,
        'reverse_direction': True,
        'subroutinize': True
    }

example_gsub = ([{"wght": (0.5, 1.0)}], {"dollar": "dollar.rvrn"}), ([{"wdth": (0.5, 1.0)}], {"cent": "cent.rvrn"})
