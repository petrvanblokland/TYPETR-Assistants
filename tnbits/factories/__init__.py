# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    __init__.py
#
from tnbits.factories.bezierpathfactory import NSBezierPathFactory
from tnbits.factories.outlineinformationfactory import OutlineInformationFactory
from defconAppKit.representationFactories.glyphCellFactory import GlyphCellFactory

"""
    "defconAppKit.GlyphCellDetail" : GlyphCellDetailFactory,
    "defconAppKit.OutlineInformation" : DefconOutlineInformationFactory,
    "defconAppKit.MenuImage" : MenuImageRepresentationFactory,

    "doodle.GlyphCell" : GlyphCellFactory,
    "doodle.GlyphSelection" : SelectionDataFactory,
    "doodle.CurveLength" : CurveLengthDataFactory,
    "doodle.Beam" : BeamFactory,
    "doodle.SpaceCenterBeam" : SpaceCenterBeamFactory,
    "doodle.AngledControlBounds" : AngledControlBoundsFactory,
    "doodle.AngledBounds" : AngledBoundsFactory,
    "doodle.Bitmap" : BitmapFactory,
    "doodle.Type2CharString" : Type2CharStringFactory,
    "doodle.lineStraightnessErrors" : LineStraightnessFactory,
    "doodle.closestPoint" : ClosestPointFactory,
    "doodle.componentOutlineInformation" : ComponentInformationFactory,
    "doodle.preCompiledGlyph" : PreCompileGlyphFactory,
"""

FACTORIES = {
    "defconAppKit.NSBezierPath": NSBezierPathFactory,
    "defconAppKit.NoComponentsNSBezierPath": NSBezierPathFactory, #NoComponentsNSBezierPathFactory,
    "defconAppKit.OnlyComponentsNSBezierPath": NSBezierPathFactory, #OnlyComponentsNSBezierPathFactory,
    "defconAppKit.OutlineInformation" : OutlineInformationFactory,
    "defconAppKit.GlyphCell" : GlyphCellFactory,
}
