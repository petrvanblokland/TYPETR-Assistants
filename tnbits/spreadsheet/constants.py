# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    constants.py
#

SHOWDRAWTILES = False
COLUMN_ID = "%s.%d"
#CELL_ID = "cell.%d.%d"

ORIGIN_X = 0
ORIGIN_Y = 16

SCALEFACTOR = 1.1
INITIAL_SCALE = 1

DEFAULT_TEXT_SIZE = 10
DEFAULT_LEADING_FACTOR = 1.4

MENU_WIDTH = 150
MENU_HEIGHT = 100
BUTTON_HEIGHT = 20

UPDATE_WINDOWTITLE = 'windowTitle'
UPDATE_CELL = 'cell'
UPDATE_CELLS = 'cells'
UPDATE_ROW = 'row'
UPDATE_ROWS = 'rows'
UPDATE_SELECTION = 'selection'

UPDATERS = (
    # Update action name,   method name.
    (UPDATE_WINDOWTITLE, 'updateWindowTitle'),
    (UPDATE_CELLS, 'updateCells'),
)
