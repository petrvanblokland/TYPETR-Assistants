# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    graphicsstate.py
#

import weakref
import traceback

from tnbits.constants import Constants
from tnbits.toolbox.storage.stack import Stack
from tnbits.objects.point import Point
from tnbits.hinting.ttf.objects.zone import Zone
from tnbits.hinting.ttf.function import Function
from tnbits.hinting.ttf.errors.exceptions import *

class GraphicsState(object):
    """
    From the documentation:

    The graphics state variables establish the context in which TrueType
    instructions are executed. This chapter provides an alphabetical listing
    of the variables that make up the graphics state along with a brief
    description of their purpose and the essential facts needed to understand
    their role. In particular it provides information on each variable's
    default value, the instruction used to set its value and a list of
    instructions affected by its setting. An overall discussion of the role of
    the graphics state variables can be found in Chapter 2, "The Font
    Engine."

    Most of the graphics state variables have a default value as shown below.
    That value is established the first time a particular font is accessed and
    again at the start of interpretation of any glyph.

    It is possible to change the default values of the graphics state variables
    using instructions. If the value is changed in the control value program,
    that value becomes the new default value.  If the value of a state variable
    is changed by instructions associated with a particular glyph, the new
    value is not a new default value and will hold only for that glyph.

    http://developer.apple.com/fonts/TTRefMan/RM07/appendixA.html
    """
    C = Constants

    def __init__(self, cvt=None, glyph=None, metrics=None, maxp=None, simulator=None, verbose=False):
        """
        http://developer.apple.com/fonts/TTRefMan/RM04/Chap4.html#projection%20vector
        """
        self.simulator = simulator
        self.verbose = verbose

        # Instructions
        self.maxp = maxp  # Maxp dictionary from font.
        self.metrics = metrics  # Hold external metrics about the requested render
        self.conditionalLevel = 0  # Level of indent of current program state
        self.functionLevel = 0

        # cvt is assumed to be a list.
        self.cvt = cvt

        self.storage = {}
        self.stack = Stack()
        self.ifskip = Stack()  # Keep track of the status to skip the if or else instructions.
        self.functionDef = None  # If set, then all instruction pour into this function id.

        self.isGrayScale = True

        self.autoFlip = True  # Default auto flip is True
        self.glyph = glyph
        self._contours = None  # Converted and cached if needed

        # Initialize zones of points sets.
        zone1 = Zone()

        if not glyph is None and hasattr(glyph, 'coordinates'):
            # Glyph points zone to work on.
            for i, p in enumerate(glyph.coordinates):
                type = glyph.flags.tolist()[i]
                start = i - 1 in glyph.endPtsOfContours
                zone1.append(Point(p[0], p[1], type=type, start=start))

        zone0 = Zone() # Free points for intermediate storage.

        # Initialize the twilight points to origin.
        for _ in range(self.maxp[self.C.MAXTWILIGHTPOINTS]):
            zone0.append(Point(0, 0))

        self.zones = {self.C.ZONE0: zone0, self.C.ZONE1: zone1}

        # Zone pointers 0, 1, 2 all initialized to zone 1.
        self.zonePointers = [zone1, zone1, zone1]

        # Reference points 0,1,2 initialized to None.
        self.referencePoints = [None, None, None]

        # Focus points, to let getCvtValue calculate the distance to guess
        # contextual CvtValue.
        self.focusPoints = (None, None)

        # Storage of reference points and winglabels as we pass through the
        # program.
        self.passedReferencePoints = set()
        self.passedWingLabels = []

        self.freedomVector = None  # Default is initially not to show
        self.projectionVector = None  # Default is initially not to show
        self.dualProjectionVector = None  # Default is initially not to show

        self.currentRatio = None  # To be calculated from projection vector and metrics.ratio
        self.instructControl = 0  # Default 0
        self.loop = 1  # Default loop count
        self.minimumDistance = self.C.HUNITS  # Default 1 pixel --> 64 hUnits

        # Default control value cut-in 17/16 pixels in hUnits.
        self.cvtCutIn = self.C.HUNITS * 17 / 16
        self.deltaBase = 9  # Default 9
        self.deltaShift = 3  # Default 3
        self.angleWeight = 0  # Deprecated use of AA also makes that SANGW is no longer needed.
        self.singleWidthCutIn = 0  # Default 0
        self.singleWidthValue = 0  # Default 0

        # Run-time storage of function instances as they get defined. Their
        # name/index is key.
        self.functions = {}

        # Rounding-related fields.
        self.roundState = self.C.ROUND_GRID  # Default round grid
        self.roundPeriod = 0
        self.roundPhase = 0
        self.roundThreshold = 0

        '''
        From Freetype:

        The default value for `scan_control' is documented as FALSE in the
        TrueType specification. This is confusing since it implies a
        Boolean value. However, this is not the case, thus both the
        default values of our `scan_type' and `scan_control' fields (which
        the documentation's `scan_control' variable is split into) are
        zero.
        '''

        self.scanControl = 0  # Default False
        self.scanType = 0  # ??

        self.inhibitGridFitting = None
        self.ignoreSetCVTValues = False

    def __repr__(self):
        """
        Pretty-prints current state.
        """
        t = ['\tSTATUS Stack:\n\n']
        showStackTop = self.getShowStackTop(self.C.SHOWSTACKSIZE)

        if showStackTop:
            s = '(%s' % showStackTop
            if len(self.stack) > self.C.SHOWSTACKSIZE:
                s += ',...'
            s += ') length = %d\n' % len(self.stack)
            t.append(s)
        else:
            t.append('Empty\n')

        t.append('Functions: %d\n' % len(self.functions))
        t.append('FreedomVector: %s\n' % self.freedomVector)
        t.append('ProjectionVector: %s\n' % self.projectionVector)
        t.append('DualProjectionVector: %s\n' % self.dualProjectionVector)

        t.append('CVT: %s values\n' % len(self.cvt))
        t.append('Loop: %s' % self.loop)
        t.append('MinDistance: %s/64\n' % self.minimumDistance)
        t.append('CvtCutIn: %s/64\n' % self.cvtCutIn)
        t.append('IsSkip: %s\n' % self.isSkip())
        t.append('Level:  %d\n' % self.level)

        zp = []

        for index, zonePointer in enumerate(self.zonePointers):
            if zonePointer == self.zones[self.C.ZONE0]:
                zone = 'zone0'    # Glyph
            else:
                zone = 'zone1'    # TwilightZone
            zp.append('zp%d: %s' % (index, zone))

        t.append('ZonePointers: [%s]\n' % (' '.join(zp)))
        rp = []

        for index, referencePoint in enumerate(self.referencePoints):
            if referencePoint < len(self.zones[self.C.ZONE1]):
                pass
                #p = self.zones[self.C.ZONE1][referencePoint]
                #rp.append('#%s: z1(%s,%s)' % (referencePoint, p.x, p.y))
            else:
                rp.append('#%s' % referencePoint)

        t.append('ReferencePoints: [%s]\n' % (','.join(rp)))
        return ' '.join(t)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def increaseLevel(self, i=1, origin='conditional'):
        """
        Keeps track of conditional nesting and function calls. Increases by
        one.
        """
        if origin == 'conditional':
            self.conditionalLevel += i
            return self.conditionalLevel
        elif origin == 'function':
            self.functionLevel += i
            return self.functionLevel

    def decreaseLevel(self, i=1, origin='conditional'):
        """
        Keeps track of conditional nesting and function calls. Decreases by
        one.
        """
        if origin == 'conditional':
            assert self.conditionalLevel > 0
            self.conditionalLevel -= i
            return self.conditionalLevel
        elif origin == 'function':
            assert self.functionLevel > 0
            self.functionLevel -= i
            return self.functionLevel

    def boundsCvt(self, icvt):
        """
        Answers if the icvt is in cvt.
        """
        if icvt < len(self.cvt):
            return True
        if self.verbose is True:
            print('[GraphicsState.boundsCvt] cvt "%s" index out of range in CVT.' % icvt)

        return False

    def boundsZone(self, zp, ip):
        """
        Determines if the point index (ip) is within the boundaries of the zone
        the zone pointer points at.
        """
        return ip is not None and 0 <= ip and ip < len(self.getZonePointer(zp))

    def getShowStackTop(self, amount=None):
        """Answer the top of the stack to show in debug mode."""
        if not self.stack:
            return None
        stacktop = []
        for s in self.stack.top(amount or self.C.SHOWSTACKSIZE):
            stacktop.append(str(s))
        stacktop.reverse()
        return ','.join(stacktop)

    def getPixelSize(self):
        return 1.0 * self.em / self.ppem

    #   self.scale      Answer the metrics scale vector

    def _get_scale(self):
        return self.metrics.scale

    scale = property(_get_scale)

    #   self.em

    def _get_em(self):
        return self.metrics.em

    em = property(_get_em)

    #   self.ppem

    def _get_ppem(self):
        return self.metrics.ppem

    ppem = property(_get_ppem)

    def resetLoop(self):
        """
        The *resetLoop* method resets the *self.getstate.resetLoop()* if any of
        the instruction that use *SLOOP* were looping by the *SLOOP*
        instruction. If they just had a set of parameters without preceding *SLOOP*,
        then the call is ignored. In that case the output an automatic *SLOOP*
        will be inserted.
        """
        self.loop = 0

    #  self.points

    def getPoints(self, zone):
        # Answer the (modified) points.
        return self.zones[zone]

    def setPoints(self, points, zone):
        # Set the (modified) points.
        self.zones[zone] = points

    def _get_points(self):
        return self.getPoints(self.C.ZONE1)

    def _set_points(self, points):
        self.setPoints(points, self.C.ZONE1)

    points = property(_get_points, _set_points)

    #   self.contours   Answer list of cached contours of Zone 1 (original points)

    @classmethod
    def getContoursFromPoints(cls, points):
        contours = []
        contour = None # Counting the current contour index
        for p in points:
            if p.isSpace():
                continue
            if p.start:
                contour = []
                contours.append(contour)
            if contour is not None:
                contour.append(p)
        return contours

    def getContours(self, zone):
        if self._contours is None:
            # Convert the list of points to a list of contours.
            self._contours = contours = []
            points = self.getPoints(zone)
            if points is None:
                points = self.getPoints(zone)
            self._contours = self.getContoursFromPoints(points)
        return self._contours

    def _get_contours(self):
        return self.getContours(self.C.ZONE1)

    contours = property(_get_contours)

    def setZonePointer(self, zpn, value):
        # The zone pointer name (zpn) stores the actual zone
        assert isinstance(zpn, int)
        assert isinstance(value, int)
        self.zonePointers[zpn] = self.zones[value]

    def getZonePointer(self, zpn):
        return self.zonePointers[zpn]

    def getZonePoint(self, zpn, i):
        assert isinstance(zpn, int)
        assert isinstance(i, int)

        try:
            return self.zonePointers[zpn][i - 1]
        except IndexError as e:
            msg = 'Incorrect index %d for zone pointer %d.' % (i, zpn)
            #msg += traceback.format_exc()
            self.simulator.message(msg, isError=True)

    def setReferencePoint(self, index, value):
        """Set the reference point instance in the current zone."""
        self.referencePoints[index] = value
        self.passedReferencePoints.add(value) # Save passed point, so we can draw them.

    def getReferencePoint(self, index):
        # The reference point stored at index, is the index of the point in the current zone.
        return self.referencePoints[index]

    #   self.referencePoint0

    def _get_referencePoint0(self):
        return self.getReferencePoint(0)

    def _set_referencePoint0(self, point):
        if self.verbose is True:
            print('Reference point type %s, point is %d' % (type(point), point))
        self.setReferencePoint(0, point)

    referencePoint0 = property(_get_referencePoint0, _set_referencePoint0)

    #   self.referencePoint1

    def _get_referencePoint1(self):
        return self.getReferencePoint(1)

    def _set_referencePoint1(self, point):
        self.setReferencePoint(1, point)

    referencePoint1 = property(_get_referencePoint1, _set_referencePoint1)

    #   self.referencePoint2

    def _get_referencePoint2(self):
        return self.getReferencePoint(2)

    def _set_referencePoint2(self, point):
        self.setReferencePoint(2, point)

    referencePoint2 = property(_get_referencePoint2, _set_referencePoint2)

    def setWingLabel(self, p1, p2, instruction):
        """
        The *storeWingLabel* stores the point pair *(p1, p2, instruction)*
        and the label type as the program passes, to draw the references later.
        DEPRECATED?
        """
        self.passedWingLabels.append((p1, p2, instruction))

    def getPassedWingLabels(self):
        #DEPRECATED?
        return self.passedWingLabels

    #   self.sRoundState

    def _set_sRoundState(self, params):
        self.roundPeriod, self.roundPhase, self.roundThreshold = params

    def _get_sRoundState(self):
        return self.roundPeriod, self.roundPhase, self.roundThreshold

    sRoundState = property(_get_sRoundState, _set_sRoundState)

    def clearSRoundState(self):
        self.sRoundState = 0,0,0 # For display purposed, clear the SROUND values

    def getCompensation(self, index):
        """
        Answers in real pixels, not 1/64th as self.C.HUNITS.
        """
        if index is None:
            return 0
        assert 0 <= index < len(self.metrics.compensations)
        return self.metrics.compensations[index] / self.C.HUNITS

    #    I F - E L S E

    def isSkip(self):
        """
        Checks if there is a level skipping.
        """
        for skip in self.ifskip.getAll():
            if skip:
                return True
        return False

    def isParentSkip(self):
        """
        Checks if there is a parent level (excluding the current one) skipping.
        """
        for skip in self.ifskip.getAll()[:-1]:
            if skip:
                return True
        return False

    def pushSkip(self, value):
        self.ifskip.push(value)

    def popSkip(self):
        return self.ifskip.pop()

    def peekSkip(self):
        return self.ifskip.peek()

    def cntSkip(self):
        """
        Answers the amount of current skip levels, show on the dashboard.
        """
        return len(self.ifskip)

    def getCvt(self, index, default):
        """
        The *getCvt* method returns the value for *key* in the CVT table.
        """
        if index < len(self.cvt):
            return self.cvt[index]
        return default

    def setCvt(self, index, value):
        """
        The *setCvt* method sets the value for `index` to `value` in the CVT table.
        """
        try:
            self.cvt[index] = value
        except Exception as e:
            msg = traceback.format_exc()
            self.simulator.message(msg, isError= True)

    def addFunctionInstruction(self, instruction):
        """
        Add instructions to current function.
        """
        if not self.functionDef in self.functions:
            self.functions[self.functionDef] = Function(self.functionDef)
        function = self.functions[self.functionDef]
        function.append(instruction)

    def pop(self, amount=1):
        if amount == 1:
            if self.verbose is True:
                print('Stack peek %d, length %d' % (self.stack.peek(), len(self.stack)))

            if self.stack.peek() is None:
                raise HintingPopException('Failed to pop() from an empty stack!')

            return self.stack.pop()

        values = []

        for _ in range(amount):
            if self.stack.peek() is None:
                raise HintingPopException('Failed to pop() from an empty stack!')
                values.append(None)
            else:
                values.append(self.stack.pop())
        return values

    def push(self, value, mode=None):
        """
        Pushes an integer value onto the stack.
        """
        assert(isinstance(value, int))
        self.stack.push(value)

    def slice(self, start=0, end=-1):
        return self.stack.slice(start, end)

    def peek(self, amount=1):
        return self.stack.peek(amount)

    def hasStack(self):
        return len(self.stack) > 0

    def delete(self, index):
        return self.stack.delete(index)

    def set(self, key, value):
        self.storage[key] = value

    def get(self, key):
        return self.storage.get(key)

    def clear(self):
        self.stack = Stack()
