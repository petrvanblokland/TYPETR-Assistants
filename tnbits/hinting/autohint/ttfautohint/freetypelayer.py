# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    freetypelayer.py (was previously renderbase.py)
#

import os
from tnbits.base.future import chr
from mojo.roboFont import NewFont
from lib.tools.defaults import getDefault
import freetype

# what are the customizations?
#from tnbits.lib import freetype # Import local customized version of Freetype2.

from tnbits.hinting.autohint.ttfautohint.ttfautohint import TTFAutohint
from tnbits.toolbox.pens.reconvertsplitpen import ReconvertSplinePointPen
from tnbits.compilers.ttxwriter import TTXWriter
from tnbits.compilers.ttxcompiler import TTXCompiler

from tnbits.constants import Constants
from tnbits.toolbox.transformer import TX
from hinting.ttf.objects._legacy.glyph import Glyph

DEBUG = True

class FreeTypeLayer(object):
    """
    Layer between TnBits and Freetype 2.
    """

    C = Constants

    @classmethod
    def drawHintScaledGlyph(cls, glyph, fontSizes=None, ppem=None, skipInsertedPoints=False, progress=None, autohint=False):
        """
        """
        assert glyph is not None
        font = glyph.font
        cls.drawHintScaledGlyphs(font, [glyph.name], fontSizes=fontSizes, ppem=ppem,
            skipInsertedPoints=skipInsertedPoints, progress=progress, autohint=autohint)

    @classmethod
    def drawHintScaledGlyphs(cls, font, glyphNames, fontSizes=None, ppem=None, skipInsertedPoints=False, progress=None, autohint=False):
        """
        The `drawHintdGlyph` method draws the scaled glyphs in a
        separate layer, using the outline scaled by FreeType.
        """
        ppem = ppem or getDefault("glyphViewGridx", 16)
        em = float(font.info.unitsPerEm)
        if fontSizes is None:
            fontSizes = [ppem]

        '''
        Get the scaled glyphs by saving the font with the glyphNames and then
        hand it over to Freetype, which will return a dictionary of sets of
        points with the scaled coordinates and sets of bitmaps.
        In case autohint is True, also call TTFAutohint on the output font first.
        The skipInsertedPoints flag defines if the "inserted" points should be
        skipped on output. This depends on how the current indexing of the hints
        is defined in relation to the points.
        '''

        hintedGlyphPoints, hintedGlyphBitmaps = cls.getScaledGlyphsData(font,
            glyphNames, fontSizes, skipInsertedPoints,
            progress=progress, autohint=autohint)

        # Do something wit the hintedGlyphBitmaps
        # self.drawWaterFall(hintedbitmaps)

        # For now just do the first size of the range...
        # Otherwise we need to make a layer for each size separately.
        fontSize = fontSizes[0]
        scale = em / (fontSize * 64)
        for glyphName in glyphNames:
            glyph = font[glyphName]
            srcGlyph = glyph.getLayer(cls.C.LAYER_FOREGROUND)
            dstGlyph = srcGlyph.copyToLayer(cls.C.LAYER_FREETYPE, clear=True)

            points = Glyph.getPoints(dstGlyph)
            hPoints = hintedGlyphPoints[glyphName].get(fontSize)
            # If not there, then the scaling did not succeed. Skip the drawing
            if hPoints is not None:
                if DEBUG:
                    # print('====', len(points), len(hPoints))
                    # Display difference between original points and scaled points
                    for index in range(max(len(points), len(hPoints))):
                        print(index,)
                        if index >= len(points):
                            print('...',)
                        else:
                            print((points[index].x, points[index].y),)
                        if index >= len(hPoints):
                            print('...',)
                        else:
                            x, y = hPoints[index]
                            print((TX.asRoundedInt(x * scale), TX.asRoundedInt(y * scale)),)
                            print((x, y),)
                        print

                # In case skipping inserted points, the number of hPoints
                # is equal or less to the number of points.
                hIndex = 0
                index = 0
                hContourStart = None
                while index < len(points):
                    point = points[index]
                    if point.start:
                        hContourStart = hIndex # Remember the start, as we may have to run over the end for the next point.
                    if skipInsertedPoints and 'inserted' in (point.name or ''):
                        '''
                        We are not getting the value back from Freetype for the inserted points,
                        so their position needs to be calculated from the neighbors.
                        @@@ Maybe still be a problem if the inserted point is at the start/end of a contour.
                        @@@ Need to check that later.
                        '''

                        if point.segmentType is None:
                            # This is an inserted off-curve. The intersecting position is in the
                            # Freetype point. So we calculate the position of the inserted
                            # and the next off-curve as 1/1.340 positions from that intersection.
                            # hPoints    prevOn                nextOff                nextOn
                            #             O-----------------------O----------------------O
                            # points                point (inserted)     point+1
                            #             O-----------O--------------------O-------------O
                            prevOnX, prevOnY = hPoints[hIndex - 1] # Previous on-curve in FT position
                            nextOffX, nextOffY = hPoints[hIndex] # Actual off-curve in FT position
                            # Take care of the adjusted position of the inserted point
                            # Just divide by 2, not MAGICNUMBER 1.340, since this it Cubic-->Cubic conversion
                            point.x = TX.asRoundedInt((prevOnX + (nextOffX - prevOnX) / 2) * scale)
                            point.y = TX.asRoundedInt((prevOnY + (nextOffY - prevOnY) / 2) * scale)
                            # Take care of the adjusted position of the next off-curve
                            hIndex += 1
                            index += 1
                            # Check if we will be running over the end of the contour, then refer to the
                            # points at the contourStarts instead.
                            if index + 1 >= len(points) or points[index + 1].start or hIndex >= len(hPoints):
                                nextOnX, nextOnY = hPoints[hContourStart] # Next on-curve in FT position
                            else:
                                nextOnX, nextOnY = hPoints[hIndex] # Next on-curve in FT position
                            nextPoint = points[index]
                            nextPoint.x = TX.asRoundedInt((nextOnX + (nextOffX - nextOnX) / 2) * scale)
                            nextPoint.y = TX.asRoundedInt((nextOnY + (nextOffY - nextOnY) / 2) * scale)
                        else:
                            # In case it is an inserted on-curve, it must be between the two adjacent off-curves.
                            # Middle it between them.
                            # hPoints    prevOff                                     nextOff
                            #             O---------------------------------------------O
                            # points                           point (inserted)
                            #             O----------------------O----------------------O
                            prevOffX, prevOffY = hPoints[hIndex - 1]
                            nextOffX, nextOffY = hPoints[hIndex]
                            point.x = TX.asRoundedInt((prevOffX + nextOffX) / 2 * scale)
                            point.y = TX.asRoundedInt((prevOffY + nextOffY) / 2 * scale)
                    else: # This is a normal point, take the position from the scale FT point
                        hx, hy = hPoints[hIndex]
                        point.x = TX.asRoundedInt(hx * scale)
                        point.y = TX.asRoundedInt(hy * scale)
                        hIndex += 1
                    index += 1
                    if hIndex >= len(hPoints):
                        break
                dstGlyph.update()

    @classmethod
    def getScaledGlyphsData(cls, font, glyphNames, fontSizes,
            skipInsertedPoints, progress=None, autohint=False):
        # Apply the freetype scaling on the saved tmp font
        scaledPoints = {}
        renderedBitmaps = {}
        # If autohinting, then add all glyphs the autohinter needs for reference.
        autohintGlyphNames = glyphNames
        if autohint:
            autohintGlyphNames = font.keys()

        path = cls.saveTmpFont(os.path.expanduser('~/Desktop/RoboFlight_tmpfreetypefont.ttf'),
            font, autohintGlyphNames,
            skipInsertedPoints=skipInsertedPoints, progress=progress)

        # Now there is a saved TTF file, that we can autohint.
        if autohint:
            hintPath = path.replace('.ttf', '_hinted.ttf')
            hintPath = TTFAutohint.autohint(path, hintPath, ppemmin=min(fontSizes), ppemmax=max(fontSizes),
                prehinting=False, heights=None, verbose=DEBUG)
            if hintPath is not None: # Successful autohint output.
                path = hintPath
                if DEBUG:
                    TTXWriter.decompile(path)

        # Render the hinted or unhinted font.
        try:
            face = freetype.Face(path)
        except freetype.ft_errors.FT_Exception:
            print('### Font "%s" could not be generated.' % path)

        for size in fontSizes:
            #face.set_char_size(size * 64)
            for glyphName in glyphNames:
                glyph = font[glyphName]
                #face.load_char(chr(glyph.unicode))
                # Run through the scaled point list to filter the double start/end
                # points of the contours, as generated by FreeType
                startPoint = None
                if scaledPoints.get(glyphName) is None:
                    # First size for this glyph, add the dictionaries
                    scaledPoints[glyphName] = {}
                    renderedBitmaps[glyphName] = {}
                # Save the points and bitmap for this size
                #scaledPoints[glyphName][size] = face.glyph.outline.points

                # TODO: display in Cocoa.
                #renderedBitmaps[glyphName][size] = face.glyph.bitmap

        return scaledPoints, renderedBitmaps

    @classmethod
    def saveTmpFont(cls, path, font, glyphNames=None, skipInsertedPoints=False, progress=None):
        """
        Generate a temporary font that holds all info of the original font, with
        a subset of glyphs as defined by glyphNames and the hint tables.

        Note: this is for scaling and rendering bt Freetype only, so no
        kerning and GPOS is copied into it. The font is optimized for
        speed scaling the glyphs, not for completeness of the output font.
        """

        # Create a new font to hold the requested glyph(s) and copy the metrics
        tmpFont = cls.getNewFont(path, 'Normal', font)

        # Initialize the glyphnames if they are not defined
        if glyphNames is None:
            glyphNames = font.keys()

        # Add the composition part glyphs here, in case there are references
        expandedGlyphNames = set()
        for glyphName in glyphNames:
            if glyphName in font.keys():
                expandedGlyphNames.add(glyphName)
                for component in font[glyphName].components:
                    expandedGlyphNames.add(component.baseGlyph)

        # If there is a progress window, set the ticks to the double amount of
        # glyphs we found, so the processing of the Freetype needs only updates.
        if progress is not None:
            progress.setTickCount(len(expandedGlyphNames))
        # Make the glyph order for the new font.
        glyphOrder = sorted(list(expandedGlyphNames))
        # Now copy all the found glyphs into a tmp font.

        for glyphName in glyphOrder:
            if progress is not None:
                progress.update(text='Saving glyph %s' % glyphName)
            glyph = font[glyphName]
            srcGlyph = glyph.getLayer(cls.C.LAYER_FOREGROUND)
            # First make the glyph, so the hints will be copied there too.
            tmpGlyph = tmpFont.newGlyph(glyphName)
            # Copy typical glyph metrics.
            tmpGlyph.width = glyph.width

            '''
            Draw the glyph in the tmp glyph. If the skipInsertedPoints flag is set
            then use a special pen to skip the inserted points.
            This is done to keep the index sync between outlines that were imported
            from raw TTF with off-curve sequences != 2. RoboFont changes the points
            but not the hint indices. If the points are not touched, then they can be
            safely removed in order to match the hint indices again in the exported
            TTF font.
            '''
            pen = tmpGlyph.getPointPen()

            if skipInsertedPoints:
                pen = ReconvertSplinePointPen(pen)
            srcGlyph.drawPoints(pen)
        # Set the glyphOrder of the font
        tmpFont.lib['public.glyphOrder'] = glyphOrder
        # Copy the hints source from the current font to the tmp font.
        # We do this after the definition of the glyph, because we only want
        # the current glyph instruction to be copied.

        # DEPRECATED or missing?
        #HintLib.copyHints(font, tmpFont)

        # Compile the hint sources into font.lib and (single) glyph.lib to
        # the TTF font will be saved with the hint binaries in place.
        TTXCompiler.compileToBinary(tmpFont)

        report = tmpFont.generate(path, format="ttf", glyphOrder=glyphNames)

        if DEBUG:
            print(report)
            TTXWriter.decompile(path)

        return path

    @classmethod
    def getNewFont(cls, name, style, srcfont, showUI=False):
        # Create a new font (for storage of the current glyph(s) and copy
        # the required metrics from the source font.
        font = NewFont(name, style, showUI=showUI)
        font.naked().segmentType = 'qcurve' # Or else the contour will be reversed on save.
        font.info.descender = srcfont.info.descender or 106
        font.info.xHeight = srcfont.info.xHeight or 300
        font.info.ascender = srcfont.info.ascender or 106
        font.info.capHeight = srcfont.info.capHeight or 90
        font.info.unitsPerEm = srcfont.info.unitsPerEm or 512
        return font

