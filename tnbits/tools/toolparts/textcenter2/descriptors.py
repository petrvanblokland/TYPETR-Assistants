# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    descriptors.py
#
from tnbits.vanillas.listcell import SmallTextListCell, SmallRightAlignTextListCell

class Descriptors:

    def getLeftGroupListDescriptor(self):
        sampleSize = 10 #int(self.getPreference('sampleSize'))

        return [
            # profile is added for easy retrieval
            #dict(title=self.LABEL_HEX, key='hex', width=40,
            #cell=SmallTextListCell(editable=True), editable=True),
            #dict(title="Base", key="base", width=30,
            #    cell=SmallTextListCell(editable=False, size=16),
            #    editable=False), # This is base glyph if showing marker
            dict(title='Name', key='name', width=100,
                cell=SmallTextListCell(editable=True), editable=True),
            dict(title='Glyphs', key='size', width=48,
                cell=SmallRightAlignTextListCell(editable=False),
                editable=False),
            dict(title='Lsb', key='sb', width=32,
                cell=SmallRightAlignTextListCell(editable=False),
                editable=True),
            # 'magic' kludgy column so we'll get edit callbacks even though
            # none of our columns are editable
            dict(title="Dummy", key="dummy", width=0, editable=True),

            #dict(title='Lerr', key='lerr', width=32,
            #cell=SmallRightAlignTextListCell(editable=False), editable=False),
        ]

    def getRightGroupListDescriptor(self):
        sampleSize = 10 #int(self.getPreference('sampleSize'))
        return [
            # profile is added for easy retrieval
            #dict(title=self.LABEL_HEX, key='hex', width=40,
            # cell=SmallTextListCell(editable=True), editable=True),
            #dict(title="Base", key="base", width=30,
            #    cell=SmallTextListCell(editable=False, size=16),
            #    editable=False), # This is base glyph if showing marker
            dict(title='Name', key='name', width=100,
                cell=SmallTextListCell(editable=True), editable=True),
            dict(title='Glyphs', key='size', width=48,
                cell=SmallRightAlignTextListCell(editable=False),
                editable=False),
            dict(title='Rsb', key='sb', width=32,
                cell=SmallRightAlignTextListCell(editable=False),
                editable=True),
            # 'magic' kludgy column so we'll get edit callbacks even though
            # none of our columns are editable
            dict(title="Dummy", key="dummy", width=0, editable=True),

            #dict(title='Rerr', key='rerr', width=32,
            #cell=SmallRightAlignTextListCell(editable=False), editable=False),
        ]

    def getKerningListDescriptor(self):
        sampleSize = 10 #int(self.getPreference('sampleSize'))
        return [
            # profiles are added for easy retrieval
            #dict(title=self.LABEL_HEX, key='hex', width=40,
            #cell=SmallTextListCell(editable=True), editable=True),
            #dict(title="Base", key="base", width=30,
            #    cell=SmallTextListCell(editable=False, size=16),
            #    editable=False), # This is base glyph if showing marker
            dict(title=self.LABEL_CHR, key='chr1',  width=sampleSize*1.8,
                cell=SmallTextListCell(editable=False, size=sampleSize),
                editable=False),
            dict(title=self.LABEL_NAME, key='name1', width=100,
                cell=SmallTextListCell(editable=False), editable=False),
            dict(title='K', key='kerning', width=36,
                cell=SmallRightAlignTextListCell(editable=False),
                editable=False),
            dict(title=self.LABEL_NAME, key='name2', width=80,
                cell=SmallTextListCell(editable=False), editable=False),
            dict(title=self.LABEL_CHR, key='chr2',  width=sampleSize*2,
                cell=SmallTextListCell(editable=False, size=sampleSize),
                editable=False),
            # 'magic' kludgy column so we'll get edit callbacks even though
            # none of our columns are editable
            dict(title="Dummy", key="dummy", width=0, editable=True),
            #dict(title='Lerr', key='lerr', width=32,
            #cell=SmallRightAlignTextListCell(editable=False), editable=False),
            #dict(title='Rerr', key='rerr', width=32,
            #cell=SmallRightAlignTextListCell(editable=False), editable=False),
        ]
