# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    instructions.py
#

import math
from tnbits.toolbox.mathematics import *
from tnbits.hinting.ttf.objects.vector import Vector
from tnbits.hinting.ttf.errors.exceptions import *
from tnbits.hinting.ttf.function import Function

class Instructions(object):
    """
    Function calls for all TTF hinting opcodes.

    The following data types are used in the TrueType font file. All TrueType
    fonts use Motorola-style byte ordering (Big Endian):

    BYTE: 8-bit unsigned integer.
    CHAR: 8-bit signed integer.
    USHORT: 16-bit unsigned integer.
    SHORT: 16-bit signed integer.
    ULONG: 32-bit unsigned integer.
    LONG: 32-bit signed integer.
    FIXED: 32-bit signed fixed-point number (16.16)
    FUNIT: Smallest measurable distance in the em space.
    FWORD: 16-bit signed integer (SHORT) that describes a quantity in FUnits.
    UFWORD: Unsigned 16-bit integer (USHORT) that describes a quantity in FUnits.
    F2DOT14: 16-bit signed fixed number with the low 14 bits of fraction (2.14).
    """

    def debugInstruction(self, instruction, params=None):
        if self.verbose is False:
            return
        self.message(self.RULER)
        self.message(str(instruction))

        if isinstance(params, dict):
            t = []
            for keyvalue in params.items():
                t.append('%s:%s' % keyvalue)
            self.message('[%s]' % ', '.join(t))
        else:
            self.message(params or '')

        self.message(self.DOTRULER)

    def i_NPUSHB(self, instruction):
        """
        Do nothing, all parameters are already pushed on self.gstate stack by
        the calling instruction dispatcher.
        """
        self.debugInstruction(instruction)
        return True

    i_PUSH = i_NPUSHB
    i_PUSHB = i_NPUSHB
    i_PUSHW = i_NPUSHB
    i_NPUSHW = i_NPUSHB
    i_PUSHW_1 = i_NPUSHB
    i_PUSHW_2 = i_NPUSHB
    i_PUSHW_3 = i_NPUSHB
    i_PUSHW_4 = i_NPUSHB
    i_PUSHW_5 = i_NPUSHB
    i_PUSHW_6 = i_NPUSHB
    i_PUSHW_7 = i_NPUSHB
    i_PUSHW_8 = i_NPUSHB
    i_PUSHB_1 = i_NPUSHB
    i_PUSHB_2 = i_NPUSHB
    i_PUSHB_3 = i_NPUSHB
    i_PUSHB_4 = i_NPUSHB
    i_PUSHB_5 = i_NPUSHB
    i_PUSHB_6 = i_NPUSHB
    i_PUSHB_7 = i_NPUSHB
    i_PUSHB_8 = i_NPUSHB

    def i_SCANCTRL(self, instruction):
        """
        Set ScanControl flags for dropout control
        TODO: How to do this in a more user friendly way?
        """
        flags = self.popParams(instruction)

        if self.fails(flags is not None, '[SCANCTRL] No flags value on stack.'):
            return False

        flags &= 0xFF

        if flags == 0xFF:
            self.gstate.scanControl = True
            return True

        if flags == 0:
            self.gstate.scanControl = True
            return True

        scancontrol = None

        if flags & 0x100 and self.gstate.metrics.ppem <= flags:
            scancontrol = True

        if flags & 0x200 and self.gstate.metrics.rotated:
            scancontrol = True

        if flags & 0x400 and self.gstate.metrics.stretched:
            scancontrol = True

        if flags & 0x800 and self.gstate.metrics.ppem > flags:
            scancontrol = False

        if flags & 0x1000 and self.gstate.metrics.rotated:
            scancontrol = False

        if flags & 0x2000 and self.gstate.metrics.stretched:
            scancontrol = False

        if scancontrol is not None:
            self.gstate.scanControl = scancontrol

        self.debugInstruction(instruction, dict(flags=flags))
        return True

    def i_SCANTYPE(self, instruction):
        """
        TODO: For now store the complete word. Later separate the flags.
        """
        scanType = self.popParams(instruction)

        if self.fails(scanType is not None, '[SCANTYPE] No scanType value on stack.'):
            return False
        self.gstate.scanType = scanType
        self.debugInstruction(instruction, dict(scanType=scanType))
        return True

    def i_INSTCTRL(self, instruction):
        """
        INSTRuction execution ConTRoL
        TODO: For now ignore this value. Later store the flags in self.gstate
        """
        s, v = self.popParams(instruction) # Selector, Value with flags

        if (s & 1):
            '''
            Flag 1 is used to inhibit grid-fitting. It is chosen with a selector value of
            1. If this flag is set to TRUE (v=1), any instructions associated with glyphs
            will not be executed. If the flag is FALSE (v=0), instructions will be
            executed.
            '''
            if (v & 1):
                self.gstate.inhibitGridFitting = True
            elif (v & 0):
                self.gstate.inhibitGridFitting = False
        elif (s & 2):
            '''
            Flag 2 is used to establish that any parameters set in the CVT program should
            be ignored when instructions associated with glyphs are executed. These
            include, for example, the values for scantype and the CVT cut-in. When flag2 is
            set to TRUE the default values of those parameters will be used regardless of
            any changes that may have been made in those values by the preprogram. When
            flag2 is set to FALSE, parameter values changed by the CVT program will be used
            in glyph instructions.
            '''
            if (v & 1):
                self.gstate.ignoreSetCVTValues = True
            elif (v & 0):
                self.gstate.ignoreSetCVTValues = False


        self.debugInstruction(instruction, dict(s=s, n=v))
        return True

    def i_GETINFO(self, instruction):
        """
        GETINFO is used to obtain data about the font scaler version and the
        characteristics of the current glyph. The instruction pops a selector used to
        determine the type of information desired and pushes a result onto the stack.
        A selector value of 1 indicates that the scaler version number is the desired
        information, a value of 2 is a request for glyph rotation status, a value of 4 asks
        whether the glyph has been stretched, a value of 32 asks whether the glyph is
        being rasterized for grayscale. (Looking at this another way, setting bit 0 asks
        for the scaler version number, setting bit 1 asks for the rotation information,
        setting bit 2 asks for stretching information, setting bit 5 asks for grayscale
        information. To request information on two or more of these set the appropriate
        bits.)

        Selector bits 3 and 4 are reserved for Apple Computer.
        The following selectors are for ClearType information. Selector bit 6 indicates
        that ClearType is enabled. Selector bit 7 indicates that “compatible-width”
        ClearType is enabled. Selector bit 8 indicates that symmetrical smoothing
        ClearType is enabled. And, selector bit 9 indicates that ClearType is processing
        the LCD stripes in BGR (Blue, Green, Red) order.

        The result pushed onto the stack contains the requested information. More
        precisely, bits 0 through 7 comprise the Scaler version number. Version 1 is
        Macintosh System 6 INIT, version 2 is Macintosh System 7, version 3 is
        Windows 3.1, version 33 is MS rasterizer v.1.5, version 34 is MS rasterizer
        v.1.6, version 35 is MS rasterizer v.1.7, version 36 is MS rasterizer 1.6+,
        version, version 37 is MS rasterizer 1.8, version 38 is MS rasterizer 1.9).
        Version numbers 0 and 4 through 255 are reserved.

        Note: Before hinting vertical phantom points or asking for grayscale
        information, use GETINFO to check that the rasterizer in use is MS rasterizer
        v.1.7 or later. Before checking if ClearType is enabled, make sure that the
        rasterizer is number is 36 or greater. For the other ClearType bits, make sure
        that the rasterizer is number 37 or greater.

        The TrueType Instruction Set
        Page 438 Revision 1.66
        File Name: ttinst1.doc

        Bit 8 is set to 1 if the current glyph has been rotated. It is 0
        otherwise. Setting bit 9 to 1 indicates that the glyph has been
        stretched. It is 0 otherwise. Bit 12 is set to 1 if the rasterization
        is done for grayscale (for MS rasterizer v.1.7 and later).

        Bit 13 is set to 1 if ClearType is enabled, otherwise it is 0 (for MS
        rasterizer v.1.6+ or MS rasterizer v.1.8 and later).

        Bit 14 is set to 1 if ClearType widths are compatible with bi-level and
        grayscale widths. It is 0 if the widths are the natural ClearType
        widths (for MS rasterizer 1.8 and later).

        Bit 15 is set to 1 if ClearType symmetrical smoothing is being used. It
        is set to zero otherwise (for MS rasterizer 1.8 and later).

        Bit 16 is set to 1 if ClearType is processing the LCD stripes in BGR (Blue,
        Green, Red) order. Otherwise if it is 0, in RGB (Red, Green, Blue) order (for
        MS rasterizer 1.8 and later).

        When the selector is set to request more than one piece of information,
        that information is OR’d together and pushed onto the stack. For example, a
        selector value of 6 requests both information on rotation and stretching and
        will result in the setting of both bits 8 and 9.
        """
        s = self.popParams(instruction) # Selector value
        info = 0;

        # We return MS rasterizer version 1.7 for the font scaler.
        if (s & 1) != 0:
          info = 35

        # Has the glyph been rotated? */
        if (s & 2) != 0 and self.gstate.metrics.rotated:
          info |= 0x80;

        # Has the glyph been stretched? */
        if (s & 4) != 0 and self.gstate.metrics.stretched:
          info |= 1 << 8;

        # Are we hinting for grayscale? */
        if (s & 32) != 0 and self.gstate.isGrayScale:
          info |= 1 << 12;

        self.gstate.push(info)
        self.debugInstruction(instruction, dict(s=s, info=info))
        return True

    def _calcSRound(self, n, gridperiod):
        period = {0:float(gridperiod*0.5), 1:float(gridperiod), 2:float(gridperiod*2)}[(n & 0xC0) >> 6]
        phase = {0:0, 1:period/4, 2:period/2, 3:3.0/4}[(n & 0x30) >> 4]
        threshold = {
            0:period-1,         1:period* -3/8,         2:period* -2/8,         3:period* -1/8,
            4:0,                5:period* 1/8,          6:period* 2/8,          7:period* 3/8,
            8:period* 4/8,      9:period* 5/8,          10:period* 6/8,         11:period* 7/8,
            12:period,          13:period* 9/8,         14:period* 10/8,        15:period* 11/8,
        }[n & 0x0f]

        return period, phase, threshold

    def i_SROUND(self, instruction):
        """
        SROUND allows you fine control over the effects of the round_state variable by allowing you
        to set the values of three components of the round_state: period, phase, and threshold.
        More formally, SROUND maps the domain of 26.6 fixed point numbers into a set of discrete
        values that are separated by equal distances. SROUND takes one argument from the stack, n,
        which is decomposed into a period, phase and threshold.
        The period specifies the length of the separation or space between rounded values in terms of
        grid spacing.
        """
        n = self.popParams(instruction)    # Value with flags

        if n is None:
            return False

        period_phase_threshold = self._calcSRound(n, 1)
        self.gstate.roundState = self.C.ROUND_SUPER
        self.gstate.sRoundState = period_phase_threshold
        self.debugInstruction(instruction, dict(period_phase_threshold=period_phase_threshold))
        return True

    def i_S45ROUND(self, instruction):
        """
        S45ROUND is analogous to SROUND. The gridPeriod is SQRT(2)/2 pixels rather than 1
        pixel. It is useful for measuring at a 45 degree angle with the coordinate axes.
        """
        n = self.popParams(instruction)    # Value with flags

        if n is None:
            return False

        period_phase_threshold = self._calcSRound(n, math.sqrt(2)/2)
        self.gstate.roundState = self.C.ROUND_SUPER45
        self.gstate.sRoundState = period_phase_threshold
        self.debugInstruction(instruction, dict(period_phase_threshold=period_phase_threshold))
        return True

    def i_UTP(self, instruction):
        """
        ``UTP[ ] // UnTouch Point``
        Marks point p as untouched. A point may be touched in the x-direction, the y-direction, both, or
        neither. This instruction uses the current freedom_vector to determine whether to untouch the
        point in the x-direction, the y-direction, or both. Points that are marked as untouched will be
        moved by an IUP (interpolate untouched points) instruction. Using UTP you can ensure that a
        point will be affected by IUP even if it was previously touched.
        """
        fv = self.gstate.freedomVector
        ip = self.popParams(instruction)
        p = self.gstate.getZonePoint(0, ip)
        if fv.x:
            p.touchedX = False
        if fv.y:
            p.touchedY = False
        self.debugInstruction(instruction, dict(ip=ip, p=p))
        return True

    def getLoopCount(self, instruction):
        """
        The ``getLoopCount`` method answers the amount of loops the ``SLOOP``
        using instruction should perform, based on either a preceding ``SLOOP`` instruction
        or just a list of points parameters. (In the latter an automatic ``SLOOP``
        instruction will be inserted in the font output code).
        """
        return len(instruction.params) or self.gstate.loop

    def i_SLOOP(self, instruction):
        """
        Pops a value, n, from the stack and sets the loop variable count to
        that value. The loop variable works with the SHP[a], SHPIX[a], IP[ ],
        FLIPPT[ ], and ALIGNRP[ ]. The value n indicates the number of times the
        instruction is to be repeated. After the instruction executes, the loop
        variable is reset to 1.
        """
        loop = self.popParams(instruction)
        if self.fails(loop >= 0, '[SLOOP] No valid loop count on stack.'):
            return False
        self.gstate.loop = loop
        self.debugInstruction(instruction, dict(loop=loop))
        return True

    def i_LOOPCALL(self, instruction):
        # TODO: What to do here?"""
        return True

    def i_ROUND(self, instruction):
        """
        Rounds a value according to the state variable round_state while compensating for the engine.
        n1 is popped off the stack and, depending on the engine characteristics, is increased or
        decreased by a set amount. The number obtained is then rounded and pushed back onto the
        stack as n2.
        """
        value = self.popParams(instruction)
        rounded = int(M.ftRoundD(value, self.gstate, instruction.mnemonic.getAttribute(0)))
        self.gstate.push(rounded)
        self.debugInstruction(instruction, dict(value=value, rounded=rounded))
        return True

    i_ROUND_gray = i_ROUND
    i_ROUND_black = i_ROUND
    i_ROUND_white = i_ROUND

    def i_SPVTL(self, instruction):
        """
        ``SPVTL[a] // Set Projection_Vector To Line``
        [r] Parallel
        [R] Perpendicular
        Sets the projection_vector to a unit vector parallel or perpendicular
        to the line segment from point p1 to point p2.
        If perpendicular the projection_vector is obtained by rotating the parallel
        vector in a counter clockwise manner as shown.
        """
        ip1, ip2 = self.popParams(instruction)
        if self.fails(self.gstate.boundsZone(2, ip1), '[SPVTL] Point "%s" is outside bounds zone(2).' % ip1) or\
            self.fails(self.gstate.boundsZone(1, ip2), '[SPVTL] Point "%s" is outside bounds zone(1).' % ip2):
            return False
        p1 = self.gstate.getZonePoint(2, ip1)
        p2 = self.gstate.getZonePoint(1, ip2)
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        if instruction.mnemonic.id == self.C.SPVTL_R:
            dx, dy = dy, -dx
        nx, ny = M.normalizedVector(dx, dy)
        self.gstate.projectionVector = Vector(nx, ny)
        self.debugInstruction(instruction, dict(ip1=ip1, ip2=ip2, n=(nx,ny)))
        return True

    i_SPVTL_r = i_SPVTL
    i_SPVTL_R = i_SPVTL

    def i_SFVTL(self, instruction):
        """
        ``SFVTL[a] // Set Freedom_Vector To Line``

        [r] Parallel
        [R] Perpendicular
        Sets the freedom vector to a unit vector parallel or perpendicular
        to the line segment from point p1 to point p2.
        If perpendicular the freedom vector is obtained by rotating the parallel
        vector in a counter clockwise manner as shown.
        """
        ip1, ip2 = self.popParams(instruction)

        if self.fails(self.gstate.boundsZone(2, ip1), '[SFVTL] Point "%s" is outside bounds zone(2).' % ip1) or\
            self.fails(self.gstate.boundsZone(1, ip2), '[SFVTL] Point "%s" is outside bounds zone(1).' % ip2):
            return False

        p1 = self.gstate.getZonePoint(2, ip1)
        p2 = self.gstate.getZonePoint(1, ip2)
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        if instruction.mnemonic.id == self.C.SFVTL_R:
            dx, dy = dy, -dx

        nx, ny = M.normalizedVector(dx, dy)
        self.gstate.freedomVector = Vector(nx, ny)
        self.debugInstruction(instruction, dict(ip1=ip1, ip2=ip2, n=(nx,ny)))
        return True

    i_SFVTL_r = i_SFVTL
    i_SFVTL_R = i_SFVTL

    def i_SDPVTL(self, instruction):
        """
        ``SDPVTL[a] // Set Dual Projection_Vector To Line``
        Pops two point numbers from the stack and uses them to specify a line
        that defines a second, dual_projection_vector. This dual_projection_vector uses
        coordinates from the scaled outline before any grid-fitting took place. It is
        used only with the IP, GC, MD, MDRP and MIRP instructions. Those instructions
        will use the dual_projection_vector when they measure distances between
        ungrid-fitted points. The dual_projection_vector will disappear when any other
        instruction that sets the projection_vector is used.  NOTE: The
        dual_projection_vector is set parallel to the points as they appeared in the
        original outline before any grid-fitting took place.
        """
        ip1, ip2 = self.popParams(instruction)
        if self.fails(self.gstate.boundsZone(2, ip1), '[SDPVTL] Point "%s" is outside bounds zone(2).' % ip1) or\
            self.fails(self.gstate.boundsZone(1, ip2), '[SDPVTL] Point "%s" is outside bounds zone(1).' % ip2):
            return False
        p1 = self.gstate.getZonePoint(2, ip1)
        p2 = self.gstate.getZonePoint(1, ip2)
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        if instruction.mnemonic.id == self.C.SDPVTL_R:
            dx, dy = dy, -dx
        nx, ny = M.normalizedVector(dx, dy)
        self.gstate.dualProjectionVector = Vector(nx, ny)
        self.debugInstruction(instruction, dict(ip1=ip1, ip2=ip2, n=(nx,ny)))
        return True

    i_SDPVTL_r = i_SDPVTL
    i_SDPVTL_R = i_SDPVTL

    def i_SFVTPV(self, instruction):
        """
        ``SFVTPV[] // Set Freedom_Vector To Projection Vector``
        Sets the freedom_vector to be the same as the projection_vector.
        """
        fv = self.gstate.projectionVector
        self.gstate.freedomVector = fv
        self.debugInstruction(instruction, dict(fv=fv))
        return True

    def i_SFVTCA(self, instruction):
        """
        ``SVTCA[a] // Set freedom and projection Vectors To Coordinate Axis``
        Sets the freedom_vector to one of the coordinate axes depending upon the value of the flag a.
        """
        if instruction.mnemonic.id == self.C.SFVTCA_Y:
            v = Vector(0, self.C.AXISUNIT)
        else:
            v = Vector(self.C.AXISUNIT, 0)
        self.gstate.freedomVector = v
        self.debugInstruction(instruction, dict(v=v))
        return True

    i_SFVTCA_X = i_SFVTCA
    i_SFVTCA_Y = i_SFVTCA

    def i_SPVTCA(self, instruction):
        """
        ``SPVTCA[a] // Set Projection_Vector To Coordinate Axis``
        Sets the projection_vector to one of the coordinate axes depending upon the value of the flag a.
        """
        if instruction.mnemonic.id == self.C.SPVTCA_X:
            v = Vector(self.C.AXISUNIT, 0)
        else:
            v = Vector(0, self.C.AXISUNIT)
        self.gstate.projectionVector = v
        self.debugInstruction(instruction, dict(v=v))
        return True

    i_SPVTCA_X = i_SPVTCA
    i_SPVTCA_Y = i_SPVTCA

    def i_SVTCA(self, instruction):
        """
        ``SVTCA[a] // Set freedom and projection Vectors To Coordinate Axis``
        Sets the projection_vector to one of the coordinate axes depending upon the value of the flag a.
        """
        if instruction.mnemonic.id == self.C.SVTCA_X:
            v = Vector(self.C.AXISUNIT, 0)
        else:
            v = Vector(0, self.C.AXISUNIT)
        self.gstate.freedomVector = v
        self.gstate.projectionVector = v
        self.gstate.dualProjectionVector = v
        self.debugInstruction(instruction, dict(v=v))
        return True

    i_SVTCA_X = i_SVTCA
    i_SVTCA_Y = i_SVTCA

    def i_SPVFS(self, instruction):
        """
        ``SPVFS[ ] // Set Projection_Vector From Stack``

        Sets the direction of the projection_vector, using values x and y taken
        from the stack, so that its projections onto the x and y-axes are x and y,
        which are specified as signed (two’s complement) fixed-point (2.14) numbers.
        The square root of (x2 + y2) must be equal to 0x4000 (hex).  If values are to
        be saved and used by a glyph program, font program or preprogram across
        different resolutions, extreme care must be used. The values taken from or put
        on the stack are 2.14 fixed-point values for the x and y components of the
        vector in question. The values are based on the normalized vector lengths. More
        simply, the values must always be set such that (X**2 + Y**2) is 1.  If a
        TrueType program uses specific values for X and Y to set the vectors to certain
        angles, these values will not produce identical results across different aspect
        ratios. Values that work correctly at 1:1 aspect ratios (such as VGA and 8514)
        will not necessarily yield the desired results at a ratio of 1.33:1 (e.g. the
        EGA).  By the same token, if a TrueType program is making use of the values
        returned by GPV and GFV, the values returned for a specific angle will vary
        with the aspect ratio in use at the time.
        """
        vx, vy = self.popParams(instruction)
        dx, dy = M.normalizedVector(vx, vy)
        self.projectionVector = Vector(dx, dy)
        self.debugInstruction(instruction, dict(vx=vx, vy=vy, dx=dx, dy=dy))
        return True

    def i_SFVFS(self, instruction):
        """
        ``SFVFS[ ] // Set Freedom_Vector From Stack``

        Sets the direction of the freedom_vector using the values x and y taken
        from the stack. The vector is set so that its projections onto the x and y
        -axes are x and y, which are specified as signed (two’s complement) fixed-point
        (2.14) numbers. The square root of (x2 + y2) must be equal to 0x4000 (hex).  If
        values are to be saved and used by a glyph program, font program or preprogram
        across different resolutions, extreme care must be used. The values taken from
        or put on the stack are 2.14 fixed-point values for the x and y components of
        the vector in question. The values are based on the normalized vector lengths.
        More simply, the values must always be set such that (X**2 + Y**2) is 1.  If a
        TrueType program uses specific values for X and Y to set the vectors to certain
        angles, these values will not produce identical results across different aspect
        ratios. Values that work correctly at 1:1 aspect ratios (such as VGA and 8514)
        will not necessarily yield the desired results at a ratio of 1.33:1 (e.g. the
        EGA).  By the same token, if a TrueType program is making use of the values
        returned by GPV and GFV, the values returned for a specific angle will vary
        with the aspect ratio in use at the time.
        """
        vx, vy = self.popParams(instruction)
        dx, dy = M.normalizedVector(vx, vy)
        self.freedomVector = Vector(dx, dy)
        self.debugInstruction(instruction, dict(vx=vx, vy=vy, dx=dx, dy=dy))
        return True

    def i_SZP0(self, instruction):
        """
        ``SZP0[ ] // Set Zone Pointer 0``

        Pops a zone number, n, from the stack and sets zp0 to the zone with
        that number. If n is 0, zp0 points to zone 0. If n is 1, zp0 points to
        zone 1. Any other value for n is an error.
        """
        zp0 = self.popParams(instruction)

        if self.fails(zp0 in (0, 1), '[SZP0] No pointer zone(0).'):
            return False
        self.gstate.setZonePointer(0, zp0)
        self.debugInstruction(instruction, dict(zp0=zp0))
        return True

    def i_SZP1(self, instruction):
        """
        ``SZP1[ ] // Set Zone Pointer 1``
        Pops a zone number, n, from the stack and sets zp1 to the zone with that number. If n is 0, zp1
        points to zone 0. If n is 1, zp1 points to zone 1. Any other value for n is an error.
        """
        zp1 = self.popParams(instruction)
        if self.fails(zp1 in (0, 1), '[SZP1] No pointer zone(1).'):
            return False
        self.gstate.setZonePointer(1, zp1)
        self.debugInstruction(instruction, dict(zp1=zp1))
        return True

    def i_SZP2(self, instruction):
        """
        ``SZP2[ ] // Set Zone Pointer 2``

        Pops a zone number, n, from the stack and sets zp2 to the zone with
        that number. If n is 0, zp2 points to zone 0. If n is 1, zp2 points to
        zone 1. Any other value for n is an error.
        """
        zp2 = self.popParams(instruction)
        if self.fails(zp2 in (0, 1), '[SZP2] No pointer zone(2).'):
            return False
        self.gstate.setZonePointer(2, zp2)
        self.debugInstruction(instruction, dict(zp2=zp2))
        return True

    def i_SZPS(self, instruction):
        """
        ``SZP2[ ] // Set Zone Pointer 2``

        Pops a zone number from the stack and sets all of the zone pointers to
        point to the zone with that number. If n is 0, all three zone pointers will
        point to zone 0. If n is 1, all three zone pointers will point to zone 1. Any
        other value for n is an error.
        """
        zp = self.popParams(instruction)
        if self.fails(zp in (0, 1), '[SZPS] No zone pointer(s) defined.'):
            return False
        self.gstate.setZonePointer(0, zp)
        self.gstate.setZonePointer(1, zp)
        self.gstate.setZonePointer(2, zp)
        self.debugInstruction(instruction, dict(zp=zp))
        return True

    def i_SRP0(self, instruction):
        """
        ``SRP0[ ] // Set Reference Point 0``

        Pops a point number from the stack and sets rp0 to that point number.
        """
        irp0 = self.popParams(instruction)

        if self.fails(irp0 is not None, '[SRP0] No valid reference point 0'):
            return False

        self.gstate.referencePoint0 = irp0
        self.debugInstruction(instruction, dict(irp0=irp0))
        return True

    def i_SRP1(self, instruction):
        """
        ``SRP1[ ] // Set Reference Point 1``

        Pops a point number from the stack and sets rp1 to that point number.
        """
        irp1 = self.popParams(instruction)

        if self.fails(irp1 is not None, '[SRP1] No valid reference point 1'):
            return False

        self.gstate.referencePoint1 = irp1
        self.debugInstruction(instruction, dict(irp1=irp1))
        return True

    def i_SRP2(self, instruction):
        """
        ``SRP2[ ] // Set Reference Point 2``

        Pops a point number from the stack and sets rp2 to that point number.
        """
        irp2 = self.popParams(instruction)
        if self.fails(irp2 is not None, '[SRP2] No valid reference point 2'):
            return False
        self.gstate.referencePoint2 = irp2
        self.debugInstruction(instruction, dict(irp2=irp2))
        return True

    def i_RTG(self, instruction):
        # Round to grid
        self.gstate.roundState = self.C.ROUND_GRID
        self.gstate.clearSRoundState() # For display purpose
        self.debugInstruction(instruction, dict(round=self.C.ROUND_GRID))
        return True

    def i_RTHG(self, instruction):
        # Round to half grid
        self.gstate.roundState = self.C.ROUND_HALFGRID
        self.gstate.clearSRoundState() # For display purpose
        self.debugInstruction(instruction, dict(round=self.C.ROUND_HALFGRID))
        return True

    def i_RTDG(self, instruction):
        # Round to double grid
        self.gstate.roundState = self.C.ROUND_DOUBLEGRID
        self.gstate.clearSRoundState() # For display purpose
        self.debugInstruction(instruction, dict(round=self.C.ROUND_DOUBLEGRID))
        return True

    def i_RDTG(self, instruction):
        # Round down to grid
        self.gstate.roundState = self.C.ROUND_DOWNTOGRID
        self.gstate.clearSRoundState() # For display purpose
        self.debugInstruction(instruction, dict(round=self.C.ROUND_DOWNTOGRID))
        return True

    def i_RUTG(self, instruction):
        # Round up to grid
        self.gstate.roundState = self.C.ROUND_UPTOGRID
        self.gstate.clearSRoundState() # For display purpose
        self.debugInstruction(instruction, dict(round=self.C.ROUND_UPTOGRID))
        return True

    def i_ROFF(self, instruction):
        # Round off
        self.gstate.roundState = self.C.ROUND_OFF
        self.gstate.clearSRoundState() # For display purpose
        self.debugInstruction(instruction, dict(round=self.C.ROUND_OFF))
        return True

    def i_IUP(self, instruction):
        """
        ``IUP[a] // Interpolate Untouched Points through the outline``

        [0] Interpolate untouched points in Y direction
        [1] Interpolate untouched points in X direction

        Considers a glyph contour by contour, moving any untouched points in
        each contour that are between a pair of touched points. If the coordinates of
        an untouched point were originally between those of the touched pair, it is
        linearly interpolated between the new coordinates, otherwise the untouched
        point is shifted by the amount the nearest touched point is shifted.  This
        instruction operates on points in the glyph zone pointed to by zp2. This zone
        should almost always be zone 1. Applying IUP to zone 0 is an error.  Consider
        three consecutive points all on the same contour. Two of the three points, p1
        and p3 have been touched. Point p2 is untouched. The effect of an IUP in the
        x-direction is to move point p2 so that is in the same relative position to
        points p1 and p3 before they were moved.  The IUP instruction does not touch
        the points it moves. Thus the untouched points affected by an IUP instruction
        will be affected by subsequent IUP instructions unless they are touched by an
        intervening instruction. In this case, the first interpolation is ignored and
        the point is moved based on its original position.
        """
        fv = self.gstate.freedomVector
        # Scanning for the touched X points?
        isXDirection = instruction.mnemonic.id == self.C.IUP_X
        contours = self.gstate.getContoursFromPoints(self.gstate.getZonePointer(2))
        for contour in contours:

            touched = []

            for index, p in enumerate(contour):
                if (isXDirection and p.touchedX) or (not isXDirection and p.touchedY):
                    if not touched:
                        touched.append([None,(index, p)])
                        touched.append([(index, p),None])
                    else:
                        touched[-1][1] = (index, p)
                        touched.append([(index, p),None])
            if touched:
                touched[0][0] = touched[-1][0]
                touched = touched[:-1]
            # Now we have a list of pairs of touched-(untouched)-touched sequences.
            for (index1, p1), (index2, p2) in touched:
                # Get the inbetween sequences of untouched points. These can be empty
                # if the touched points are neighbours.
                if index1 > index2: # Happens at start and end of the point list
                    untouchedpoints = contour[index1+1:] + contour[:index2]
                else:
                    untouchedpoints = contour[index1+1:index2]
                for point in untouchedpoints:
                    if point.isSpace():
                        # Don't interpolate the space points
                        continue
                    if isXDirection:
                        if (p1.orgX < point.orgX and point.orgX < p2.orgX) or (p2.orgX < point.orgX and point.orgX < p1.orgX):
                            #p2-p1 : point-p1 = p2org-p1org : pointorg-p1org
                            point.x = (point.orgX - p1.orgX) * (p2.x - p1.x) / (p2.orgX - p1.orgX) + p1.x
                        elif abs(point.orgX - p1.orgX) < abs(point.orgX - p2.orgX):
                            point.x += p1.x - p1.orgX
                        else:
                            point.x += p2.x - p2.orgX
                    else: # Interpolate in Y direction
                        if (p1.orgY < point.orgY and point.orgY < p2.orgY) or (p2.orgY < point.orgY and point.orgY < p1.orgY):
                            #p2-p1 : point-p1 = p2org-p1org : pointorg-p1org
                            point.y = (point.orgY - p1.orgY) * (p2.y - p1.y) / (p2.orgY - p1.orgY) + p1.y
                        elif abs(point.orgY - p1.orgY) < abs(point.orgY - p2.orgY):
                            point.y += p1.y - p1.orgY
                        else:
                            point.y += p2.y - p2.orgY

            self.debugInstruction(instruction, dict(fv=fv, touched=touched))
        return True

    i_IUP_Y = i_IUP
    i_IUP_X = i_IUP

    def i_MDAP(self, instruction):
        """
        Sets the reference points rp0 and rp1 equal to point p. If a=1, this
        instruction rounds point p to the grid point specified by the state variable
        round_state. If a=0, it simply marks the point as touched in the direction(s)
        specified by the current freedom_vector. This command is often used to set
        points in the twilight zone.

        From the documentation:

        "Touch and, in some cases, round the specified point. A point that is
        "dapped" will be unaffected by subsequent IUP[ ] instructions and is generally
        intended to serve as a reference point for future instructions. Dapping a point
        with rounding set to grid will cause the point to have an integer valued
        coordinate along the projection vector. If the projection vector is set to the
        x-axis or y-axis, this will cause the point to be grid-aligned."

        "Pops a point number, p, and sets reference points rp0 and rp1 to point p. If
        the Boolean a is set to 1, the coordinate of point p, as measured against the
        projection vector, will be rounded and then moved the rounded distance from its
        current position. If the Boolean a is set to 0, point p is not moved, but
        nonetheless is marked as touched in the direction(s) specified by the current
        freedom vector."
        """
        ip = self.popParams(instruction)

        if self.fails(ip is not None, "[MDAP] No point defined."):
            return False

        irp0 = self.gstate.getReferencePoint(0)
        msg = '[MDAP] Reference point "%s" is outside bounds zone(0).' % irp0

        if self.fails(self.gstate.boundsZone(0, irp0), msg):
            return False

        rp0 = self.gstate.getZonePoint(0, irp0)

        # Move the point
        p = self.gstate.getZonePoint(0, ip)
        orgdistance = M.ftProjectionMeasure(p.x - rp0.x, p.y - rp0.y, self.gstate)

        msg = '[MDAP] No projection vector defined for point "%s"' % ip
        if self.fails(orgdistance is not None, msg):
            return False

        # Freetype XXX: Is there some undocumented feature while in the twilight zone?
        if instruction.mnemonic.id == self.C.MDAP_R:
            distance = M.ftRoundD(orgdistance, self.gstate)
            xy = M.freeMoveTo(p.x, p.y, FT(distance - orgdistance), self.gstate)
            p.shiftTo(xy)

        M.touchP(p, self.gstate)

        self.gstate.referencePoint0 = ip
        self.gstate.referencePoint1 = ip

        self.debugInstruction(instruction, dict(ip=ip, p=p))
        return True

    i_MDAP_r = i_MDAP
    i_MDAP_R = i_MDAP

    def i_SHZ(self, instruction):
        """
        Shift the points in the specified zone (Z1 or Z0) by the same amount
        that the reference point has been shifted. The points in the zone are shifted
        along the freedom_vector so that the distance between the new position of the
        shifted points and their old position is the same as the distance between the
        current position of the reference point and the original position of the
        reference point.  SHZ[a] uses zp0 with rp1 or zp1 with rp2. This instruction is
        similar to SHC, but all points in the zone are shifted, not just the points on
        a single contour.
        """
        fv = self.gstate.freedomVector
        # Get reference point, depending on the flag/zone
        if instruction.mnemonic.id == self.C.SHC_0:
            # 0: uses rp2 in the zone pointed to by zp1
            rp = self.gstate.getZonePoint(1, self.gstate.getReferencePoint(2))
        else:
            # 1: uses rp1 in the zone pointed to by zp0
            rp = self.gstate.getZonePoint(0, self.gstate.getReferencePoint(1))
        dx, dy = rp.getMoved()
        d = M.scalexyByVector(dx, dy, fv)

        # Get index of zone to handle
        ie = self.popParams(instruction)
        for p in self.gstate.getZonePointer(ie): # All points in zone ie
            p.shiftBy(dx, dy)
            M.touchP(p, self.gstate)
        self.debugInstruction(instruction, dict(dx=dx, dy=dy, d=d))
        return True

    i_SHZ_0 = i_SHZ
    i_SHZ_1 = i_SHZ

    def i_SHC(self, instruction):
        """
        Shifts every point on contour c by the same amount that the reference
        point has been shifted.  Each point is shifted along the freedom_vector so that
        the distance between the new position of the point and the old position of that
        point is the same as the distance between the current position of the reference
        point and the original position of the reference point. The distance is
        measured along the projection_vector. If the reference point is one of the
        points defining the contour, the reference point is not moved by this
        instruction.  This instruction is similar to SHP, but every point on the
        contour is shifted.
        """
        fv = self.gstate.freedomVector
        # Get reference point, depending on the flag/zone
        if instruction.mnemonicl.id == self.C.SHC_0:
            # 0: uses rp2 in the zone pointed to by zp1
            rp = self.gstate.getZonePoint(1, self.gstate.getReferencePoint(2))
        else:
            # 1: uses rp1 in the zone pointed to by zp0
            rp = self.gstate.getZonePoint(0, self.gstate.getReferencePoint(1))
        dx, dy = rp.getMoved()
        d = M.scalexyByVector(dx, dy, fv)

        # Get index of contour to handle
        ic = self.popParams(instruction)
        contours = self.gstate.getContoursFromPoints(self.gstate.getZonePointer(2))
        for p in contours[ic]:
            p.shiftBy(dx, dy)
            M.touchP(p, self.gstate)
        self.debugInstruction(instruction, dict(fv=fv, rp=rp, dx=dx, dy=dy, ic=ic, d=d))
        return True

    i_SHC_0 = i_SHC
    i_SHC_1 = i_SHC

    def i_SHP(self, instruction):
        """
        Shift point p by the same amount that the reference point has been
        shifted. Point p is shifted along the freedom_vector so that the distance
        between the new position of point p and the current position of point p is the
        same as the distance between the current position of the reference point and
        the original position of the reference point.  NOTE: Point p is shifted from
        its current position, not its original position. The distance that the
        reference point has shifted is measured between its current position and the
        original position.  Note that both ``SHP[0]`` and ``SHP[2]`` will refer to
        reference point 2.  The ``SHP[1]`` will refer to reference point 1.  In the
        illustration below rp is the original position of the reference point, rp' is
        the current position of the reference point, p is the original position of
        point p, p' is the current position, p" the position after it is shifted by the
        SHP instruction. (White indicates original position, gray is current position,
        black is position to which this instruction moves a point).
        """
        fv = self.gstate.freedomVector

        # Get reference point, depending on the flag/zone
        if instruction.mnemonic.id == self.C.SHP_0:
            # 0: uses rp2 in the zone pointed to by zp1
            rp2 = self.gstate.getReferencePoint(2)

            if self.fails(rp2 is not None, '[SHP] Reference point 2 is not defined'):
                return False

            if self.fails(rp2 < len(self.gstate.getZonePointer(1)), '[SHP] Reference2 index "%s" too large for Zone1' % rp2):
                return False
            rp = self.gstate.getZonePointer(1)[rp2]
        else:
            # 1: uses rp1 in the zone pointed to by zp0
            rp1 = self.gstate.getReferencePoint(1)

            if self.fails(rp1 is not None, '[SHP] Reference point 1 is not defined'):
                return False

            if self.fails(rp1 < len(self.gstate.getZonePointer(0)), '[SHP] Reference1 index "%s" too large for Zone0' % rp1):
                return False
            rp = self.gstate.getZonePoint(0, rp1)

        dx, dy = rp.getShifted()
        sdx, sdy = M.scalexyByVector(dx, dy, fv)
        pointstoshift = []

        # FIXME: Gets None as points.

        for _ in range(self.getLoopCount(instruction)):
            ip = self.popParams(instruction) # Get index of point to handle.
            p = self.gstate.getZonePoint(2, ip) # zp2 with point p.

            if p is None:
                print('i_SHP: error: p is none for index %d' % ip)
            else:
                # Store them first, or else we'll get a "NeedsUpdate warning
                # after the first move
                pointstoshift.append(p)
            self.debugInstruction(instruction, dict(ip=ip, p=p))

        # Now loop through the shifted points to move them.
        for p in pointstoshift:
            p.shiftBy(sdx, sdy)
            M.touchP(p, self.gstate)
            # Remember the winglabels we are passing through, to draw them later
            self.gstate.setWingLabel(rp, p, instruction) # Deprecated?

        self.gstate.resetLoop()
        return True

    i_SHP_0 = i_SHP
    i_SHP_1 = i_SHP

    def i_SHPIX(self, instruction):
        """
        ``SHPIX[ ] // SHift point by a PIXel amount``

        Shifts the points specified by the amount stated. When the loop
        variable is used, the amount to be shifted is put onto the stack only once.
        That is, if loop = 3, then the contents of the top of the stack should be point
        p1, point p2, point p3, amount. The value amount is expressed in sixtyfourths
        of a pixel.

        SHPIX is unique in relying solely on the direction of the
        freedom_vector. It makes no use of the projection_vector. Measurement
        is made in the direction of the freedom_vector.

        Example

        The instruction shifts points 27, 28, and 29 by 80/64 or 1.25 pixels in
        the direction of the freedom vector. The distance is measured in the direction
        of the freedom_vector; the projection vector is ignored.
        """
        d = float(self.popParams(instruction))/64        # Pop shift amount in 1/64 pixel unit
        fv = self.gstate.freedomVector
        dv = self.scaled(d, fv)
        pointstomove = []

        for _ in range(self.getLoopCount(instruction)):
            ip = self.popParams(instruction)
            p = self.gstate.getZonePoint(2, ip)
            pointstomove.append(p)

        # Do not move before we collected them all, since the glyph will complain
        for p in pointstomove:
            p.shiftBy(dv.x, dv.y)
            M.touchP(p, self.gstate)

        self.gstate.resetLoop()
        self.debugInstruction(instruction, dict(fv=fv, d=d))
        return True

    def i_WCVTF(self, instruction):
        """
        ``WCVTF[ ] // Write Control Value Table in Funits``

        Writes a scaled F26Dot6 value to the specified control value table
        location.

        Pops an integer value, n, and a control value table location l from the stack.
        The FUnit value is scaled to the current point size and resolution and put in
        the control value table. This instruction assumes the value is expressed in
        FUnits and not pixels.

        Since the CVT has been scaled to pixel values, the value taken from the stack
        is scaled to the appropriate pixel value before being written to the table.
        """

        value, icvt = self.popParams(instruction)
        value = self.fUnitsToPixels(value)
        self.gstate.setCvt(icvt, value)
        self.debugInstruction(instruction, dict(icvt=icvt, value=value))
        return True

    def i_WCVTP(self, instruction):
        """
        ``WCVTP[ ] // Write Control Value Table in Pixel units``

        Writes the value in pixels into the control value table location specified.

        Pops a value v and a control value table location l from the stack and puts
        that value in the specified location in the control value table. This
        instruction assumes the value taken from the stack is in pixels and not in
        FUnits. The value is written to the CVT table unchanged. The location l must be
        less than the number of storage locations specified in the 'maxp' table in the
        font file.
        """
        value, icvt = self.popParams(instruction)

        '''
        # In theory the popped CVT index should always be smaller than the
        # maximum storage value in the maxp dictionary.
        if self.fails(icvt < self.gstate.maxp['maxStorage'], '[WCVTP] CVT index %d larger than maxstorage %d.' % (icvt, self.gstate.maxp['maxStorage'])):
            return False
        '''

        self.gstate.setCvt(icvt, value)
        self.debugInstruction(instruction, dict(icvt=icvt, value=value))
        return True

    def i_RCVT(self, instruction):
        """
        ``RCVT[ ] // Read Control Value Table``

        Pops a location from the stack and pushes the value in the location
        specified in the Control Value Table onto the stack.
        """
        location = self.popParams(instruction)
        # We have no context here, so the CVT name needs to be specific.
        assert not location in self.C.CVT_TYPES # TODO: This should give a better user warning as popup window.
        value = self.gstate.getCvt(location, 0) # Default is 0
        self.gstate.push(value)
        self.debugInstruction(instruction, dict(value=value))
        return True

    def i_FDEF(self, instruction):
        """
        ``FDEF[ ] // Function DEFinition``

        Marks the start of a function definition. The argument f is a number
        that uniquely identifies this function. A function definition can appear only
        in the Font Program or the CVT program. Functions may not exceed 64K in size.

        """
        functionDef = self.popParams(instruction)
        self.gstate.functionDef = functionDef
        self.debugInstruction(instruction, dict(id=functionDef))
        return True

    def i_ENDF(self, instruction):
        """
        ``ENDF[ ] // END Function definition``

        Marks the end of a function definition or an instruction definition.

        """
        self.gstate.functionDef = None
        self.debugInstruction(instruction)
        return True

    def i_POP(self, instruction):
        """

        ``POP[ ] // POP top stack element``
        Pops the top element of the stack.

        """
        self.popParams(instruction)
        self.debugInstruction(instruction)
        return True

    def i_WS(self, instruction):
        """
        ``WS[ ] // Write Store``

        This instruction writes a 32 bit value into the storage location
        indexed by locations. It works by popping a value and then a location from the
        stack. The value is placed in the Storage Area location specified by that
        address. The number of storage locations is specified in the maxProfile table
        in the font file.
        """
        value, location = self.popParams(instruction)
        self.gstate[location] = value
        self.debugInstruction(instruction, dict(value=value, location=location))
        return True

    def i_RS(self, instruction):
        """
        ``RS[ ] // Read Store``

        This instruction reads a 32 bit value from the Storage Area location
        popped from the stack and pushes the value read onto the stack. It pops an
        address from the stack and pushes the value found in that Storage Area location
        to the top of the stack. The number of available storage locations is specified
        in the maxProfile table in the font file.
        """
        location = self.popParams(instruction)
        value = self.gstate.get(location)

        if self.fails(value is not None, '[RS] Storage value "%s" does not exist.' % location):
            return False

        self.gstate.push(value)
        self.debugInstruction(instruction, dict(location=location, value=value))
        return True

    def i_MPPEM(self, instruction):
        """
        ``MPPEM[ ] // Measure Pixels Per EM``

        This instruction writes a 32 bit value into the storage location
        indexed by locations. It works by popping a value and then a location from the
        stack. The value is placed in the Storage Area location specified by that
        address. The number of storage locations is specified in the maxProfile table
        in the font file.
        """
        # return TT_MULFIX( CUR.tt_metrics.ppem, CURRENT_Ratio() );
        self.gstate.push(self.gstate.ppem)
        self.debugInstruction(instruction, dict(ppem=self.gstate.ppem))
        return True

    def i_ROLL(self, instruction):
        """
        ``ROLL[ ] // ROLL the top three stack elements``

        Performs a circular shift of the top three objects on the stack with
        the effect being to move the third element to the top of the stack and to move
        the first two elements down one position.  ROLL is equivalent to MINDEX[ ] 3.
        """
        a, b, c = self.popParams(instruction)
        self.gstate.push(b)
        self.gstate.push(a)
        self.gstate.push(c)
        self.debugInstruction(instruction, dict(a=a, b=b, c=c))
        return True

    def i_DUP(self, instruction):
        """
        ``DUP[ ] // Duplicate top stack element``

        Duplicates the element at the top of the stack.
        """
        value = self.popParams(instruction)
        self.gstate.push(value)
        self.gstate.push(value)
        self.debugInstruction(instruction, dict(value=value))
        return True

    def i_SWAP(self, instruction):
        """
        ``SWAP[ ] // SWAP the top two elements on the stack``

        Swaps the top two elements of the stack making the old top element the
        second from the top and the old second element the top element.
        """
        value1, value2 = self.popParams(instruction)
        self.gstate.push(value1)
        self.gstate.push(value2)
        self.debugInstruction(instruction, dict(value1=value1, value2=value2))
        return True

    def i_SANGW(self, instruction):
        """
        SANGW is no longer needed because of dropped support to the AA (Adjust
        Angle) instruction.  AA was the only instruction that used angle_weight in the
        global graphics state.  Pops a weight value from the stack and sets the value
        of the angle_weight state variable accordingly.
        """
        self.gstate.angleWeight = self.popParams(instruction)

    def i_SDB(self, instruction):
        """
        Pops a number, n, and sets delta_base to the value n. The default for
        delta_base is 9.
        """
        self.gstate.deltaBase = self.popParams(instruction)

    def i_SDS(self, instruction):
        """
        Sets delta_shift to the value n. The default for delta_shift is 3.
        """
        self.gstate.deltaShift = self.popParams(instruction)

    def i_FLIPPT(self, instruction):
        """
        ``FLIPPT[ ] // FLIP PoinT``

        Flips points that are off the curve so that they are on the curve and
        points that are on the curve so that they are off the curve. The point is not
        marked as touched. The result of a FLIPPT instruction is that the contour
        describing part of a glyph outline is redefined.
        """
        ips = []
        pointstoflip = []
        for _ in range(self.getLoopCount(instruction)):
            ip = self.popParams(instruction)
            ips.append(ip)
            p = self.gstate.getZonePoint(0, ip)
            pointstoflip.append(p)
        # Collect all points first before flipping
        for p in pointstoflip():
            p.flipType()
            # Not marking as touched.
        self.gstate.resetLoop()
        self.debugInstruction(instruction, dict(ip=ips))
        return True

    def i_FLIPRGON(self, instruction):
        """
        ``FLIPRGON[ ] // FLIP RanGe ON``

        Flips a range of points beginning with lowpoint and ending with
        highpoint so that any off the curve points become on the curve points. The
        points are not marked as touched.
        """
        #zp0 = self.gstate.getZonePointerPointer(0)
        iphi, ip = self.popParams(instruction)
        iplo = ip

        while iplo <= iphi:
            p = self.gstate.getZonePoint(0, ip)
            p.type = self.POINTTYPE_ON
            ip += 1

        self.debugInstruction(instruction, dict(iplo=iplo, iphi=iphi))
        return True

    def i_FLIPRGOFF(self, instruction):
        """
        ``FLIPRGOFF[ ] // FLIP RanGe OFF``

        Flips a range of points beginning with lowpoint and ending with
        highpoint so that any on curve points become off the curve points. The points
        are not marked as touched.  NOTE: This instruction changes the curve but the
        position of the points is unaffected.  Accordingly, points affected by this
        instruction are not marked as touched.
        """
        #zp0 = self.gstate.getZonePointerPointer(0)
        iphi, ip = self.popParams(instruction)
        iplo = ip

        while ip <= iphi:
            p = self.gstate.getZonePoint(0, ip)
            p.type = self.POINTTYPE_OFF
            ip += 1

        self.debugInstruction(instruction, dict(iplo=iplo, iphi=iphi))
        return True

    def i_FLIPOFF(self, instruction):
        """
        ``FLIPOFF[ ] // Set the auto_flip Boolean to OFF``

        Set the auto_flip Boolean in the Graphics State to FALSE causing the
        MIRP instructions to use the sign of Control Value Table entries. The default
        auto_flip Boolean value is TRUE.
        """
        self.gstate.autoFlip = False
        self.debugInstruction(instruction)
        return True

    def i_FLIPON(self, instruction):
        """
        ``FLIPON[ ] // Set the auto_flip Boolean to ON``

        Sets the auto_flip Boolean in the Graphics State to TRUE causing the
        MIRP instructions to ignore the sign of Control Value Table entries. The
        default auto_flip Boolean value is TRUE.
        """
        self.gstate.autoFlip = True
        self.debugInstruction(instruction)
        return True

    def i_CALL(self, instruction):
        """
        ``CALL[ ] // CALL function``

        Calls the function identified by the number f.
        """
        functionId = self.popParams(instruction)
        function = self.gstate.functions.get(functionId)

        assert isinstance(function, Function)

        if self.verbose is True:
            self.message('CALLing function %d' % functionId)

        if self.fails(function is not None, '[CALL] Cannot find function "%s".' % functionId):
            return False

        self.debugInstruction(instruction, dict(functionId=functionId))

        # Increase.
        level = self.gstate.increaseLevel(origin='function')
        mode = self.getStepMode()

        # We know the function ID after it is popped, so we need to assign it
        # to the correct level.
        if self.getTopStepIndex(mode) == 0:
            self.setFunctionId(mode, level, functionId)

        # Gets the index for the function.
        stepIndex = self.getFunctionStepIndex(mode, level, functionId)

        try:
            self.runProgram(program=function, stepIndex=stepIndex)
        except Exception as e:
            print(e)

        # End of function after entire run, remove loop index and decrement
        # function level.
        if stepIndex is None or stepIndex == len(function):
            del self.loopIndices[level]
            self.gstate.decreaseLevel(origin='function')
            'Removing level %d from loop indices and decrease' % level

        # Only remove step index if at end and program name is correct.
        if not stepIndex is None and stepIndex == len(function):
            del self.stepIndices[mode][level]
            print('Removed level %d from step indices.' % level)

        return True

    def i_EQ(self, instruction):
        """
        ``EQ[ ] // EQual``

        Pops e1 and e2 off the stack and compares them. If they are equal, 1,
        signifying TRUE is pushed onto the stack. If they are not equal, 0, signifying
        FALSE is placed onto the stack.
        """
        e1, e2 = self.popParams(instruction)
        self.gstate.push(e1 == e2) # Boolean instead of 0/1
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, boolean=e1 == e2))
        return True

    def i_NEQ(self, instruction):
        """
        ``NEQ[ ] // Not EQual``

        Pops e1 and e2 from the stack and compares them. If they are not equal,
        1, signifying TRUE, is pushed onto the stack. If they are equal, 0, signifying
        FALSE, is placed on the stack.
        """
        e1, e2 = self.popParams(instruction)
        self.gstate.push(e1 != e2) # Boolean instead of 0/1
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, boolean=e1 != e2))
        return True

    def i_LT(self, instruction):
        """
        ``LT[ ] // Less Than``

        **First pops e2, then pops e1** off the stack and compares them: if e1
        is less than e2, 1, signifying TRUE, is pushed onto the stack. If e1 is not
        less than e2, 0, signifying FALSE, is placed onto the stack.
        """
        e2, e1 = self.popParams(instruction)
        self.gstate.push(e1 < e2) # Boolean instead of 0/1
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, boolean=e1 < e2))
        return True

    def i_LTEQ(self, instruction):
        """
        ``LTEQ[ ] // Less Than or Equal``

        **Pops e2 and e1** off the stack and compares them. If e1 is less than
        or equal to e2, 1, signifying TRUE, is pushed onto the stack. If e1 is not less
        than or equal to e2, 0, signifying FALSE, is placed onto the stack.
        """
        e2, e1 = self.popParams(instruction)
        self.gstate.push(e1 <= e2) # Boolean instead of 0/1
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, boolean=e1 <= e2))
        return True

    def i_GT(self, instruction):
        """
        ``GT[ ] // Greater Than``

        **First pops e2 then pops e1** off the stack and compares them. If e1 is greater than e2, 1,
        signifying TRUE, is pushed onto the stack. If e1 is not greater than e2, 0, signifying FALSE, is
        placed onto the stack.

        """
        e2, e1 = self.popParams(instruction)
        self.gstate.push(e1 > e2) # Boolean instead of 0/1
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, boolean=e1 > e2))
        return True

    def i_GTEQ(self, instruction):
        """

        ``GTEQ[ ] // Greater Than or Equal``
        **First pops e2 then pops e1** off the stack and compares them. If e1 is greater than e2, 1,
        signifying TRUE, is pushed onto the stack. If e1 is not greater than e2, 0, signifying FALSE, is
        placed onto the stack.

        """
        e2, e1 = self.popParams(instruction)
        self.gstate.push(e1 >= e2) # Boolean instead of 0/1
        self.debugInstruction(instruction)
        return True

    def i_ODD(self, instruction):
        """

        ``ODD[ ] // ODD``
        Tests whether the number at the top of the stack is odd. Pops e1 from the stack and rounds it as
        specified by the round_state before testing it. After the value is rounded, it is shifted from a
        fixed point value to an integer value (any fractional values are ignored). If the integer value is
        odd, one, signifying TRUE, is pushed onto the stack. If it is even, zero, signifying FALSE is
        placed onto the stack.
        Note that the value is supposed to be in 1/64 pixel measure.

        """
        e = self.popParams(instruction)
        if self.fails(e is not None, '[ODD] Missing parameter.'):
            return False
        rounded = int(M.ftRoundD(e, self.gstate))
        self.gstate.push(M.isOdd(rounded)) # Boolean instead of 0/1
        self.debugInstruction(instruction, dict(e=e, rounded=rounded, odd=M.isOdd(rounded)))
        return True

    def i_EVEN(self, instruction):
        """

        ``EVEN[ ] // EVEN``
        Tests whether the number at the top of the stack is even. Pops e1 off the stack and rounds it as
        specified by the round_state before testing it. If the rounded number is even, one, signifying
        TRUE, is pushed onto the stack if it is odd, zero, signifying FALSE, is placed onto the stack.
        Note that the value is supposed to be in 1/64 pixel measure.

        """
        e = self.popParams(instruction)
        if self.fails(e is not None, '[EVEN] Missing parameter.'):
            return False
        rounded = M.ftRoundD(e, self.gstate)
        self.gstate.push(M.isEven(rounded)) # Boolean instead of 0/1
        self.debugInstruction(instruction, dict(e=e, rounded=rounded, even=M.isEven(rounded)))
        return True

    def i_NOT(self, instruction):
        """

        ``NOT[ ] // logical NOT``
        Pops e off the stack and returns the result of a logical NOT operation performed on e. If
        originally zero, one is pushed onto the stack if originally nonzero, zero is pushed onto the stack.

        """
        e = self.popParams(instruction)
        self.gstate.push(not e)
        self.debugInstruction(instruction, dict(e=e, not_=not e))
        return True

    def i_AND(self, instruction):
        """

        ``AND[ ] // logical AND``
        Pops e1 and e2 off the stack and pushes onto the stack the result of a logical and of the two
        elements. Zero is returned if either or both of the elements are FALSE (have the value zero).
        One is returned if both elements are TRUE (have a non zero value).

        """
        e1, e2 = self.popParams(instruction)
        self.gstate.push(bool(e1 and e2))
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, and_=bool(e1 and e2)))
        return True

    def i_OR(self, instruction):
        """

        ``OR[ ] // logical OR``
        Pops e1 and e2 off the stack and pushes onto the stack the result of a logical or operation
        between the two elements. Zero is returned if both of the elements are FALSE. One is returned
        if either both of the elements are TRUE.

        """
        e1, e2 = self.popParams(instruction)
        self.gstate.push(bool(e1 or e2))
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, or_=bool(e1 or e2)))
        return True

    def i_ADD(self, instruction):
        """

        ``ADD[ ] // ADD``
        Pops e1 and e2 off the stack and pushes onto the stack the result of a logical or operation
        between the two elements. Zero is returned if both of the elements are FALSE. One is returned
        if either both of the elements are TRUE.

        """
        e1, e2 = self.popParams(instruction)
        self.gstate.push(e1 + e2)
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, add=e1 + e2))
        return True

    def i_SUB(self, instruction):
        """

        ``SUB[ ] // SUB``
        Pops n1 and n2 off the stack and pushes the difference between the two elements onto the stack.

        """
        e1, e2 = self.popParams(instruction)
        self.gstate.push(e2 - e1)
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, subtract=e2 - e1))
        return True

    def i_DIV(self, instruction):
        """
        ``DIV[ ] // DIVide``

        Pops n1 and n2 off the stack and pushes onto the stack the quotient
        obtained by dividing n2 by n1. Note that this truncates rather than rounds the
        value. The TrueType Rasterizer v.1.7 and later will catch any division-by-zero
        errors.
        """
        e2, e1 = self.popParams(instruction)

        if self.fails(e2 != 0, '[DIV] Division by 0.'):
            return False

        div = int((64.0 * e1) / e2)
        self.gstate.push(div)
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, divide=div))

        return True

    def i_MUL(self, instruction):
        """
        ``MUL[ ] // MULtiply``

        Multiplies the top two numbers on the stack. Pops two 26.6 numbers, n2 and n1,
        from the stack and pushes onto the stack the product of the two elements. The
        52.12 result is shifted right by 6 bits and the high 26 bits are discarded
        yielding a 26.6 result.
        """
        e1, e2 = self.popParams(instruction)
        product = (e1 * e2) / 64
        self.gstate.push(product)
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, multiply=product))
        return True

    def i_ABS(self, instruction):
        """

        ``ABS[ ] // ABSolute</h2>
        This instruction pops n1 off the stack and pushes onto the stack the negated value of n1.

        """
        e = self.popParams(instruction)
        if self.fails(e is not None, '[ABS] Undefined value.'):
            return False
        self.gstate.push(abs(e))
        self.debugInstruction(instruction, dict(e=e, absolute=abs(e)))
        return True

    def i_NEG(self, instruction):
        """

        ``NEG[ ] // NEGate</h2>
        This instruction pops n1 off the stack and pushes onto the stack the negated value of n1.

        """
        e = self.popParams(instruction)
        if self.fails(e is not None, '[NEG] Undefined value.'):
            return False
        self.gstate.push(-e)
        self.debugInstruction(instruction, dict(e=e, negate=-e))
        return True

    def i_FLOOR(self, instruction):
        """
        ``FLOOR[ ] // FLOOR</h2>

        Takes the floor of the value at the top of the stack.

        Pops a 26.6 fixed point number n from the stack and returns n, the
        greatest integer value less than or equal to n. Note that the floor of n,
        though an integer value, is expressed as 26.6 fixed point number.
        """
        e = self.popParams(instruction)
        if self.fails(e is not None, '[FLOOR] Undefined value.'):
            return False
        self.gstate.push(int(math.floor(e)))
        self.debugInstruction(instruction, dict(e=e, floor=math.floor(e)))
        return True

    def i_CEILING(self, instruction):
        """

        ``CEILING[ ] // CEILING</h2>
        Pops n1 and returns n, the least integer value greater than or equal to n1. For instance, the
        ceiling of 15 is 15, but the ceiling of 15.3 is 16. The ceiling of -0.8 is 0. (n is the least integer
        value greater than or equal to n1)

        """
        e = self.popParams(instruction)
        if self.fails(e is not None, '[CEILING] Undefined value.'):
            return False
        self.gstate.push(math.ceil(e))
        self.debugInstruction(instruction, dict(e=e, ceiling=math.ceil(e)))
        return True

    def i_MAX(self, instruction):
        """

        ``MAX[ ] // MAX</h2>
        Pops two elements, e1 and e2, from the stack and pushes the larger of these two quantities onto
        the stack.

        """
        e1, e2 = self.popParams(instruction)
        if self.fails(e1 is not None and e2 is not None, '[MAX] One or two undefined values.'):
            return False
        self.gstate.push(max(e1, e2))
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, max=max(e1, e2)))
        return True

    def i_MIN(self, instruction):
        """

        ``MIN[ ] // MIN</h2>
        Pops two elements, e1 and e2, from the stack and pushes the smaller of these two quantities
        onto the stack.

        """
        e1, e2 = self.popParams(instruction)
        if self.fails(e1 is not None and e2 is not None, '[MIN] One or two undefined values.'):
            return False
        self.gstate.push(min(e1, e2))
        self.debugInstruction(instruction, dict(e1=e1, e2=e2, min=min(e1, e2)))
        return True

    def i_SMD(self, instruction):
        """
        ``SMD[ ] // Set Minimum_ Distance``

        Pops a value from the stack and sets the minimum_distance variable to that value. The
        distance is assumed to be expressed in sixty-fourths of a pixel.

        """
        distance = self.popParams(instruction)
        self.gstate.minimumDistance = distance
        self.debugInstruction(instruction, dict(distance=distance))
        return True

    def i_IF(self, instruction):
        """
        ``IF[ ] // IF test``

        The ``i_IF`` method handles the conditional IF instruction.  If pop
        value is True, then mark the following instructions as not skipping.  If
        already in skipping mode, add another skipping layer. This is done, to be able
        to see to which level an ELSE belongs. Only ELSE instructions on top level will
        be able to toggle the skipping self.gstate.
        """
        self.gstate.increaseLevel() # Increment level by 1

        if self.gstate.isSkip():
            self.gstate.pushSkip(True)
        else:
            ifCondition = self.popParams(instruction)
            self.debugInstruction(instruction, dict(if_=ifCondition))
            self.gstate.pushSkip(not ifCondition)

        return True

    def i_ELSE(self, instruction):
        """
        ``ELSE[ ] // ELSE``

        The ``i_ELSE`` method handles the conditional ELSE instruction.  Else
        does reverse the current skipping self.gstate, only when none of the levels is
        skipping. Otherwise ignore the level since the whole IF-ELSE-EIF is in
        skipping mode then.
        """
        if self.fails(self.gstate.conditionalLevel > 0, '[ELSE] ELSE instruction without IF.'):
            return False

        elseCondition = self.gstate.popSkip()
        self.gstate.decreaseLevel()
        self.debugInstruction(instruction, dict(else_=elseCondition))

        if not self.gstate.isParentSkip():
            self.gstate.pushSkip(not elseCondition)
        elif DEBUG:
            print('# ...')

        self.gstate.increaseLevel()

        return True

    def i_EIF(self, instruction):
        """
        ``EIF[ ] // END IF``

        The ``i_EIF`` method handles the conditional EIF (End-if) instruction.
        The pop is always performed (because there always is an IF push) regardless of
        skipping self.gstate.  This is done, to be able to see to which level an ELSE
        belongs. Only ELSE instructions on top level will be able to toggle the
        skipping self.gstate.
        """
        if self.fails(self.gstate.conditionalLevel > 0, '[EIF] EIF instruction without IF or ELSE.'):
            return False

        # Pop the current ifskip value, even when we are in skipping mode.
        self.gstate.decreaseLevel()
        self.debugInstruction(instruction)
        self.gstate.popSkip()
        return True

    # TODO: remove?
    '''
    def i_SPVFS(self, instruction):
        """
        ``SPVFS[ ] // Set Projection Vector From Stack``

        Sets the direction of the projection_vector, using values x and y taken
        from the stack, so that its projections onto the x and y-axes are x and y,
        which are specified as signed (two’s complement) fixed-point (2.14) numbers.
        The square root of (x2 + y2) must be equal to 0x4000 (hex).  If values are to
        be saved and used by a glyph program, font program or preprogram across
        different resolutions, extreme care must be used. The values taken from or put
        on the stack are 2.14 fixed-point values for the x and y components of the
        vector in question. The values are based on the normalized vector lengths. More
        simply, the values must always be set such that (X**2 + Y**2) is 1.  If a
        TrueType program uses specific values for X and Y to set the vectors to certain
        angles, these values will not produce identical results across different aspect
        ratios. Values that work correctly at 1:1 aspect ratios (such as VGA and 8514)
        will not necessarily yield the desired results at a ratio of 1.33:1 (e.g. the
        EGA).  By the same token, if a TrueType program is making use of the values
        returned by GPV and GFV, the values returned for a specific angle will vary
        with the aspect ratio in use at the time.
        """
        y = self.popParams(instruction)
        x = self.popParams(instruction)
        self.gstate.projectionVector = Vector(x, y)
        self.debugInstruction(instruction, dict(pv=self.gstate.projectionVector, x=x, y=y))
    '''

    def i_SCFS(self, instruction):
        """
        ``SCFS[ ] // Sets Coordinate From the Stack using projection_vector and freedom_vector``

        Moves point p from its current position along the freedom_vector so
        that its component along the projection_vector becomes the value popped off the
        stack.
        """
        # FIXME.
        distance = self.popParams(instruction)
        point, ip = self.popParams(instruction)

        if self.fails(self.gstate.boundsZone(2, ip), '[SCFS] Point "%s" is outside bounds zone(2).' % ip):

            raise HintingParamsException('Error in SCFS')
            return False

        p = self.gstate.getZonePoint(2, ip)
        print('Zone pointer is %s' % p)

        measured = M.ftProjectionMeasure(p[0], p[1], self.gstate)
        print(measured)

        p.shiftTo(xy)
        M.touchP(p, self.gstate)
        self.debugInstruction(instruction, dict(ip=ip, distance=distance, p=p, measured=measured))
        return True

    def i_ALIGNRP(self, instruction):
        """
        ``ALIGNRP[ ] // ALIGN Relative Point``

        Reduces the distance between rp0 and point p to zero. Since distance is
        measured along the projection_vector and movement is along the freedom_vector,
        the effect of the instruction is to align points.
        """
        irp0 = self.gstate.getReferencePoint(0)
        if self.fails(self.gstate.boundsZone(0, irp0), '[ALIGNRP] Point "%s" is outside bounds zone(0).' % irp0):
            return False
        rp0 = self.gstate.getZonePoint(0, irp0)
        pointstoalign = []
        for index in range(self.getLoopCount(instruction)):
            ip = self.popParams(instruction)
            if self.fails(self.gstate.boundsZone(1, ip), '[ALIGNRP] Point "%s" is outside bounds zone(1).' % ip):
                return False
            alignp = self.gstate.getZonePoint(1, ip)
            pointstoalign.append(alignp)
        # Collect all points first before aligning
        for p in pointstoalign:
            distance = M.ftProjectionMeasure(p.x - rp0.x, p.y - rp0.y, self.gstate)
            xy = M.freeMoveTo(p.x, p.y, FT(-distance), self.gstate)
            p.shiftTo(xy)
            M.touchP(p, self.gstate)

        self.gstate.resetLoop()
        self.debugInstruction(instruction, dict(irp0=irp0, ip=ip, index=index))
        return True

    def i_GPV(self, instruction):
        """

        ``GPV[ ] // Get Projection_Vector``
        Pushes the x and y components of the projection_vector onto the stack as two 2.14 numbers.
        If values are to be saved and used by a glyph program, font program or preprogram across
        different resolutions, extreme care must be used. The values taken from or put on the stack are
        2.14 fixed-point values for the x and y components of the vector in question. The values are
        based on the normalized vector lengths. More simply, the values must always be set such that
        (X**2 + Y**2) is 1.
        If a TrueType program uses specific values for X and Y to set the vectors to certain angles,
        these values will not produce identical results across different aspect ratios. Values that work
        correctly at 1:1 aspect ratios (such as VGA and 8514) will not necessarily yield the desired
        results at a ratio of 1.33:1 (e.g. the EGA).
        By the same token, if a TrueType program is making use of the values returned by GPV and
        GFV, the values returned for a specific angle will vary with the aspect ratio in use at the time.

        """
        pv = self.gstate.projectionVector
        self.gstate.push(pv.x)
        self.gstate.push(pv.y)
        self.debugInstruction(instruction, dict(pv=pv))
        return True

    def i_GFV(self, instruction):
        """

        ``GFV[ ] // Get Freedom_Vector``
        Puts the x and y components of the freedom_vector on the stack. The freedom_vector is put
        onto the stack as two 2.14 coordinates.
        If values are to be saved and used by a glyph program, font program or preprogram across
        different resolutions, extreme care must be used. The values taken from or put on the stack are
        2.14 fixed-point values for the x and y components of the vector in question. The values are
        based on the normalized vector lengths. More simply, the values must always be set such that
        (X**2 + Y**2) is 1.
        If a TrueType program uses specific values for X and Y to set the vectors to certain angles,
        these values will not produce identical results across different aspect ratios. Values that work
        correctly at 1:1 aspect ratios (such as VGA and 8514) will not necessarily yield the desired
        results at a ratio of 1.33:1 (e.g. the EGA).
        By the same token, if a TrueType program is making use of the values returned by GPV and
        GFV, the values returned for a specific angle will vary with the aspect ratio in use at the time.

        """
        fv = self.gstate.getFreedomVector()
        self.gstate.push(fv.x)
        self.gstate.push(fv.y)
        self.debugInstruction(instruction, dict(fv=fv))
        return True

    def i_CINDEX(self, instruction):
        """

        ``CINDEX[ ] // Copy the INDEXed element to the top of the stack``
        Puts a copy of the kth stack element on the top of the stack.

        """
        k = self.popParams(instruction)
        self.gstate.push(self.gstate.peek(k))
        self.debugInstruction(instruction, dict(k=k))
        return True

    def i_MINDEX(self, instruction):
        """
        ``MINDEX[ ] // Move the INDEXed element to the top of the stack``

        Moves the indexed element to the top of the stack.
        """
        k = self.popParams(instruction)
        value = self.gstate.delete(k)
        self.gstate.push(value)
        self.debugInstruction(instruction, dict(k=k, value=value))
        return True

    def i_GC(self, instruction):
        """

        ``GC[ ] // Get Coordinate projected onto the projection_vector``
        Measures the coordinate value of point p on the current projection_vector and pushes the value
        onto the stack.
        *Example*
        The following example shows that the value returned by GC is dependent upon the current
        position of the projection_vector. Note that point p is at the position (300,420) in the coordinate
        grid.

        """
        ip = self.popParams(instruction)
        if self.fails(self.gstate.boundsZone(2, ip), '[GC] Point "%s" is outside bounds zone(2).' % ip):
            return False
        p = self.gstate.getZonePoint(2, ip)
        if instruction.mnemonic.id == self.GC_curp:
            x = p.x
            y = p.y
        else:
            x = p.orgX
            y = p.orgY
        d = self.ftProjectionMeasure(x, y)
        self.gstate.push(d)
        self.debugInstruction(instruction, dict(ip=ip, p=p, x=x, y=y, d=d))
        return True

    i_GC_curp = i_GC

    def i_IP(self, instruction):
        """

        Moves point p so that its relationship to rp1 and rp2 is the same as it was in the original
        uninstructed outline. Measurements are made along the projection_vector, and movement to
        satisfy the interpolation relationship is constrained to be along the freedom_vector. This
        instruction is illegal if rp1 and rp2 have the same position on the projection_vector.

        """
        success = True
        irp1 = self.gstate.getReferencePoint(1) # Get index of reference point 1
        irp2 = self.gstate.getReferencePoint(2) # Get index of reference point 2
        if self.fails(irp1 is not None, '[IP] Reference point 1 is undefined.') or\
            self.fails(irp2 is not None, '[IP] Reference point 2 is undefined.') or\
            self.fails(self.gstate.boundsZone(0, irp1), '[IP] Point "%s" is outside bounds zone(0).' % irp1) or\
            self.fails(self.gstate.boundsZone(1, irp2), '[IP] Point "%s" is outside bounds zone(1).' % irp2):
            return False

        # Get the reference points
        rp1 = self.gstate.getZonePoint(0, irp1)
        rp2 = self.gstate.getZonePoint(1, irp2)
        if self.fails(rp1.x != rp2.x or rp2.x != rp2.y, '[IP] Reference points do not relate in x or y.'):
            return False

        # Omit some code of Freetype solving twilight bugs in old fonts.

        orgrange = M.ftDualProjectionMeasure(rp2.orgX - rp1.orgX, rp2.orgY - rp1.orgY, self.gstate)
        currange = M.ftProjectionMeasure(rp2.x - rp1.x, rp2.y - rp1.y, self.gstate)

        if self.fails(orgrange is not None, '[IP] Dual projection vector is not defined.') or\
            self.fails(currange is not None, '[IP] Projection vector is not defined.'):
            return False

        pointstoip = []
        # Check if we are looping by defined parameters
        # Otherwise get the regular loopcount from the graphics state.
        for _ in range(self.getLoopCount(instruction)):
            ip = self.popParams(instruction)
            if self.fails(self.gstate.boundsZone(2, ip), '[IP] Point "%s" is outside bounds zone(2).' % ip):
                success = False
            else:
                # Get indexed point from zone from zone pointer 2
                p = self.gstate.getZonePoint(2, ip)
                pointstoip.append((p, ip))

        # Collect all points first before interpolate
        for p, ip in pointstoip:
            if self.fails(self.gstate.boundsZone(2, ip), '[IP] Point "%s" is outside bounds zone(2).' % ip):
                return False
            orgdistance = M.ftDualProjectionMeasure(p.orgX - rp1.orgX, p.orgY - rp1.orgY, self.gstate)
            curdistance = M.ftProjectionMeasure(p.x - rp1.x, p.y - rp1.y, self.gstate)

            if orgdistance:
                if orgrange:
                    newdistance = FT(orgdistance * currange / orgrange)
                else:
                    newdistance = curdistance
            else:
                newdistance = 0

            xy = M.freeMoveTo(p.x, p.y, FT(newdistance - curdistance), self.gstate)
            if self.fails(xy is not None, '[IP] No freedom vector defined.'):
                return False
            p.shiftTo(xy)
            M.touchP(p, self.gstate)

            self.debugInstruction(instruction, dict(irp1=irp1, irp2=irp2, ip=ip))

        self.gstate.resetLoop()
        return success

    def i_ISECT(self, instruction):
        """
        ``ISECT[ ] // moves point p to the InterSECTion of two lines``

        Puts point p at the intersection of the lines A and B. The points a0 and a1 define line A.
        Similarly, b0 and b1 define line B. ISECT ignores the freedom_vector in moving point p.

        """
        # WARNING: moves point p to the InterSECTion of two lines
        ib1, ib0, ia1, ia0, ip = self.popParams(instruction)

        if self.fails(self.gstate.boundsZone(0, ib1), '[ISECT] Point "%s" is outside bounds zone(0).' % ib1) or\
            self.fails(self.gstate.boundsZone(0, ib0), '[ISECT] Point "%s" is outside bounds zone(0).' % ib0) or\
            self.fails(self.gstate.boundsZone(1, ia1), '[ISECT] Point "%s" is outside bounds zone(1).' % ia1) or\
            self.fails(self.gstate.boundsZone(1, ia0), '[ISECT] Point "%s" is outside bounds zone(1).' % ia0) or\
            self.fails(self.gstate.boundsZone(2, ip), '[ISECT] Point "%s" is outside bounds zone(2).' % ip):
            return False

        # Get indexed points from zone from zone pointer 2
        b1 = self.gstate.getZonePoint(0, ib1)
        b0 = self.gstate.getZonePoint(0, ib0)
        a1 = self.gstate.getZonePoint(1, ia1)
        a0 = self.gstate.getZonePoint(1, ia0)
        p = self.gstate.getZonePoint(2, ip)


        dbx = b1.x - b0.x
        dby = b1.y - b0.y

        dax = a1.x - a0.x
        day = a1.y - a0.y

        dx = b0.x - a0.x;
        dy = b0.y - a0.y;

        self.touchPxy(p)

        discriminant = float(dax * -dby + day * dbx)

        if abs(discriminant) >= 1:
            val = dx * -dby + dy * dbx
            rx = val * dax / discriminant
            ry = val * day / discriminant

            p.x = a0.x + rx;
            p.y = a0.y + ry;
        else:
            # else, take the middle of the middles of A and B
            p.x = (a0.x + a1.x + b0.x + b1.x)/4
            p.y = (a0.y + a1.y + b0.y + b1.y)/4
        self.debugInstruction(instruction, dict(ib1=ib1, ib0=ib0, ia1=ia1, ia0=ia0, ip=ip, p=p))
        return True

    def i_SCVTCI(self, instruction):
        """

        ``SCVTCI[ ] // Set Control Value Table Cut In``
        Sets the control_value_cut_in in the Graphics State. The value n is expressed in sixty-fourths of
        a pixel.

        """
        n = self.popParams(instruction)
        if n is None:
            return False
        n = FT(n) # Make it fixed floatm value is already multiplied.
        self.gstate.cvtCutIn = n
        self.debugInstruction(instruction, dict(n=n))
        return True

    def i_SSWCI(self, instruction):
        """

        ``SSWCI[ ] // Set Single Width Cut In``
        Sets the single_width_cut_in in the Graphics State. The value n is expressed in sixty-fourths of
        a pixel.

        """
        n = self.popParams(instruction)
        if n is None:
            return False
        n = FT(n)
        self.gstate.singleWidthCutIn = n
        self.debugInstruction(instruction, dict(n=n))
        return True

    def i_SSW(self, instruction):
        """

        ``SSW[ ] // Set Single Width Value``
        Sets the single_width_value in the Graphics State. The value n is expressed in sixty-fourths of
        a pixel.

        """
        n = self.popParams(instruction)
        if n is None:
            return False
        n = FT(n)
        self.gstate.singleWidthValue = n
        self.debugInstruction(instruction, dict(n=n))
        return True

    def i_MD(self, instruction):
        """

        ``MD[a] // Measure Distance``
        a=0 measure distance in grid-fitted outline, a=N measure distance in original outline.
        Measures the distance between outline point p1 and outline point p2. The value returned is in
        pixels (F26Dot6) If distance is negative, it was measured against the projection vector.
        Reversing the order in which the points are listed will change the sign of the result.
          /*************************************************************************/
          /* Freetype source remarks                                               */
          /* BULLSHIT: Measure taken in the original glyph must be along the dual  */
          /*           projection vector.                                          */
          /*                                                                       */
          /* Second BULLSHIT: Flag attributes are inverted!                        */
          /*                  0 => measure distance in original outline            */
          /*                  1 => measure distance in grid-fitted outline         */
          /*                                                                       */
          /* Third one: `zp0 - zp1', and not `zp2 - zp1!                           */
          /*************************************************************************/

        """
        opcode = instruction.mnemonic.id == self.C.MD_org # Type of measure
        ip0, ip1 = self.popParams(instruction)
        z0 = self.gstate.getZonePointer(0)
        z1 = self.gstate.getZonePointer(1)
        if ip0 < 0 or ip0 >= len(z0) or ip1 < 0 or ip1 >= len(z1):
            return False
        if opcode:
            # Measure on grid fitted outline
            d = M.pointDistance(z0[ip0], z0[ip1])
        else:
            # Measure on original outline
            p0 = z1[ip0]
            p1 = z1[ip1]
            # TODO: things to be done here
            d = 0
        self.gstate.push(d)
        return True

    i_MD_grid = i_MD
    i_MD_org = i_MD

    def i_MIAP(self, instruction):
        """

        ``MIAP[a] // Move Indirect Absolute Point``
        Moves point p to the absolute coordinate position specified by the nth
        Control Value Table entry. The coordinate is measured along the current
        projection_vector. If a=1, the position will be rounded as specified by
        round_state. If a=1, and if the device space difference between the CVT value
        and the original position is greater than the control_value_cut_in, then the
        original position will be rounded (instead of the CVT value.) Rounding is done
        as if the entircoordinate system has been rotated to be consistent with the
        projection_vector. That is, if round_state is set to 1, and the
        projection_vector and freedom_vector are at a 45_ angle to the x-axis, then a
        MIAP[1] of a point to 2.9 pixels will round to 3.0 pixels along the
        projection_vector.  The a Boolean above controls both rounding and the use of
        the control_value_cut_in. If you would like the meaning of this Boolean to
        specify only whether or not the MIAP[ ] instruction should look at the
        control_value_cut_in value, use the ROFF[ ] instruction to turn off rounding.

        Freetype comments:
        /* NOTE: UNDOCUMENTED!                                   */
        /*                                                       */
        /* The behaviour of an MIAP instruction is quite         */
        /* different when used in the twilight zone.             */
        /*                                                       */
        /* First, no control value cut-in test is performed      */
        /* as it would fail anyway.  Second, the original        */
        /* point, i.e. (org_x,org_y) of zp0.point, is set        */
        /* to the absolute, unrounded distance found in          */
        /* the CVT.                                              */
        /*                                                       */
        /* This is used in the CVT programs of the Microsoft     */
        /* fonts Arial, Times, etc., in order to re-adjust       */
        /* some key font heights.  It allows the use of the      */
        /* IP instruction in the twilight zone, which            */
        /* otherwise would be `illegal' according to the         */
        /* specification.                                        */
        /*                                                       */
        /* We implement it with a special sequence for the       */
        /* twilight zone. This is a bad hack, but it seems       */
        /* to work.                                              */

        """
        #import time
        #t = time.time()
        ip, icvt = self.popParams(instruction) # Absolute length as position of
        #t = time.time()
        if self.fails(self.gstate.boundsCvt(icvt),
            '[MIAP] Cvt reference "%s" is undefined.' % icvt) or\
            self.fails(self.gstate.boundsZone(0, ip),
                '[MIAP] Point "%s" is outside bounds zone(0).' % ip):
            return False

        #t = time.time()

        # Get indexed point from zone from zone pointer 0
        p = self.gstate.getZonePoint(0, ip)
        orgdistance = M.ftProjectionMeasure(p.x, p.y, self.gstate)
        if self.fails(orgdistance is not None, '[MIAP] Set projection vector'):
            return False
        #t = time.time()

        # Set the focus points (origin, p) in the gstate, so the getCvtValue can calculate
        # the distance to guess the contextual matching CvtValue
        self.gstate.focusPoints = (self.originPoint, p)
        #t = time.time()

        distance = M.value2Ft(self.gstate.getCvt(icvt, 0, self.gstate)) # Default is 0
        #t = time.time()

        singlewidthcutin = M.value2Ft(self.gstate.cvtCutIn)
        #t = time.time()

        if instruction.mnemonic.id == self.C.MIAP_R:
            # Round distance and look at the control_value_cut_in
            if abs(distance - orgdistance) > singlewidthcutin:
                distance = orgdistance
            distance = M.ftRoundD(distance, self.gstate, self.C.COMPENSATION_GRAY)
        #t = time.time()

        xy = M.freeMoveTo(p.x, p.y, FT(distance - orgdistance), self.gstate)
        p.shiftTo(xy)
        M.touchP(p, self.gstate)
        #t = time.time()

        # Set reference points
        self.gstate.referencePoint0 = ip
        self.gstate.referencePoint1 = ip
        self.debugInstruction(instruction, dict(icvt=icvt, ip=ip, p=p, distance=distance))
        return True

    i_MIAP_r = i_MIAP
    i_MIAP_R = i_MIAP

    def i_MDRP(self, instruction):
        """

        ``MDRP[abcde] // Move Direct Relative Point``
        [m....] Do not set rp0 to point p after move;
        [M....] Set rp0 to p after move;
        [.<...] Do not keep distance greater than or equal to MinimumDistance
        [.>...] Keep distance greater than or equal to MinimumDistance
        [..r..] Do not round distance
        [..R..] Do round distance
        [...Wh] Distance type for engine characteristics compensation
        [...Bl]
        [...Gr]

        MDRP moves point p along the freedom_vector so that the distance from
        its new position to the current position of rp0 is the same as the distance
        between the two points in the original uninstructed outline, and then adjusts
        it to be consistent with the Boolean settings. Note that it is only the
        original positions of rp0 and point p and the current position of rp0 that
        determine the new position of point p along the freedom_vector.  MDRP is
        typically used to control the width or height of a glyph feature using a value
        which comes from the original outline. Since MDRP uses a direct measurement and
        does not reference the control_value_cut_in, it is used to control measurements
        that are unique to the glyph being instructed. Where there is a need to
        coordinate the control of a point with the treatment of points in other glyphs
        in the font, a MIRP instruction is needed.  Though MDRP does not refer to the
        CVT, its effect does depend upon the single-width cut-in value. If the device
        space distance between the measured value taken from the uninstructed outline
        and the single_width_value is less than the single_width_cut_in, the
        single_width_value will be used in preference to the outline distance. In other
        words, if the two distances are sufficiently close (differ by less than the
        single_width_cut_in), the single_width_value will be used.  The setting of the
        round_state Graphics State variable will determine whether and how the distance
        of point p from point q is rounded. If the round bit is not set, the value will
        be unrounded. If the round bit is set, the effect will depend upon the choice
        of rounding state. The value of the minimum distance variable is the smallest
        possible value the distance between two points can be rounded to.

        """
        # FIXME: Where is MxRP_i_COLOR used?

        ip = self.popParams(instruction)
        irp0 = self.gstate.getReferencePoint(0)

        # Validate params and state for this instruction
        if self.fails(irp0 is not None, '[MDRP] Reference point 0 is not set.') or\
            self.fails(ip is not None, '[MDRP] Point %s is not defined.' % ip) or\
            self.fails(self.gstate.boundsZone(1, ip), '[MDRP] Point %s is outside bounds zone(1).' % ip) or\
            self.fails(self.gstate.boundsZone(0, irp0), '[MDRP] Reference point %s is outside bounds zone(0).' % irp0):
            return False

        # Get indexed point from zone from zone pointer 0
        p = self.gstate.getZonePoint(1, ip)

        # Get the reference point
        rp0 = self.gstate.getZonePoint(0, irp0)

        # Omitted Freetype special case code for twilight zone.

        if self.gstate.scale.x == self.gstate.scale.y:
            orgdistance = M.ftDualProjectionMeasure(p.orgX - rp0.orgX, p.orgY - rp0.orgY, self.gstate)
        else:
            # TODO: Untested for non-square scaling
            dx = (p.orgX - rp0.x) * self.gstate.scale.x
            dy = (p.orgY - rp0.y) * self.gstate.scale.y
            orgdistance = M.ftDualProjectionMeasure(dx, dy, self.gstate)

        singlewidthvalue = self.gstate.singleWidthValue
        singlewidthcutin = self.gstate.singleWidthCutIn

        # Single width cut-in test
        if abs(orgdistance - singlewidthvalue) < singlewidthcutin:
            if orgdistance >= 0:
                orgdistance = singlewidthvalue
            else:
                orgdistance = FT(-singlewidthvalue)

        # Round flag
        if instruction.mnemonic.getAttribute(self.C.MxRP_i_ROUNDDISTANCE):
            distance = M.ftRoundD(orgdistance, self.gstate, self.C.COMPENSATION_WHITE)
        else:
            distance = M.ftRoundD(orgdistance, self.gstate, self.C.COMPENSATION_WHITE, roundState=self.C.ROUND_NONE)

        # Minimum distance flag
        if instruction.mnemonic.getAttribute(self.C.MxRP_i_KEEPDISTANCE):
            if orgdistance >= 0:
                distance = M.ftMax(distance, self.gstate.getMinimumDistance())
            else:
                distance = M.ftMin(distance, -self.gstate.getMinimumDistance())

        # Move the point
        orgdistance = M.ftProjectionMeasure(p.x - rp0.x, p.y - rp0.y, self.gstate)
        xy = M.freeMoveTo(p.x, p.y, FT(distance - orgdistance), self.gstate)
        p.shiftTo(xy)
        M.touchP(p, self.gstate)

        # Remember the winglabels we are passing through, to draw them later
        self.gstate.setWingLabel(rp0, p, instruction) # Deprecated?

        # Set the reference points
        self.gstate.referencePoint1 = irp0
        self.gstate.referencePoint2 = ip
        if instruction.mnemonic.getAttribute(self.C.MxRP_i_RP2P):
            self.gstate.referencePoint0 = ip

        self.debugInstruction(instruction, dict(irp0=irp0, ip=ip, distance=distance, orgdistance=orgdistance))
        return True

    i_MDRP_m_lt_r_Gray = i_MDRP
    i_MDRP_M_lt_r_Gray = i_MDRP
    i_MDRP_m_gt_r_Gray = i_MDRP
    i_MDRP_M_gt_r_Gray = i_MDRP
    i_MDRP_m_lt_R_Gray = i_MDRP
    i_MDRP_M_lt_R_Gray = i_MDRP
    i_MDRP_m_gt_R_Gray = i_MDRP
    i_MDRP_M_gt_R_Gray = i_MDRP

    i_MDRP_m_lt_r_01 = i_MDRP
    i_MDRP_M_lt_r_01 = i_MDRP
    i_MDRP_m_gt_r_01 = i_MDRP
    i_MDRP_M_gt_r_01 = i_MDRP
    i_MDRP_m_lt_R_01 = i_MDRP
    i_MDRP_M_lt_R_01 = i_MDRP
    i_MDRP_m_gt_R_01 = i_MDRP
    i_MDRP_M_gt_R_01 = i_MDRP

    i_MDRP_m_lt_r_Black = i_MDRP
    i_MDRP_M_lt_r_Black = i_MDRP
    i_MDRP_m_gt_r_Black = i_MDRP
    i_MDRP_M_gt_r_Black = i_MDRP
    i_MDRP_m_lt_R_Black = i_MDRP
    i_MDRP_M_lt_R_Black = i_MDRP
    i_MDRP_m_gt_R_Black = i_MDRP
    i_MDRP_M_gt_R_Black = i_MDRP

    i_MDRP_m_lt_r_White = i_MDRP
    i_MDRP_M_lt_r_White = i_MDRP
    i_MDRP_m_gt_r_White = i_MDRP
    i_MDRP_M_gt_r_White = i_MDRP
    i_MDRP_m_lt_R_White = i_MDRP
    i_MDRP_M_lt_R_White = i_MDRP
    i_MDRP_m_gt_R_White = i_MDRP
    i_MDRP_M_gt_R_White = i_MDRP

    def i_MSIRP(self, instruction):
        """
        ``MSIRP[ ] // Move Stack Indirect Relative Point``

        Makes the distance between a point p and rp0 equal to the value
        specified on the stack. The distance on the stack is in fractional pixels
        (F26Dot6). An MSIRP has the same effect as a MIRP instruction except that it
        takes its value from the stack rather than the Control Value Table. As a
        result, the cut_in does not affect the results of a MSIRP. Additionally, MSIRP
        is unaffected by the round_state.
        """
        fv = self.gstate.getFreedomVector()
        d, ip = self.popParams(instruction)
        d = M.scalexyByVector(d, d, fv)
        #self.fails(self.gstate.boundsZone(1, ib1)) #FIXME
        p = self.gstate.getZonePoint(1, ip)
        irp0 = self.gstate.getReferencePoint(0)
        rp0 = self.gstate.getZonePoint(0, irp0)
        distance = self.ftProjectionMeasure(p.x - rp0.x, p.y - rp0.y)
        x, y = self.freeMoveTo(p.x, p.y, distance)
        p.shiftTo(x, y)
        M.touchP(p, self.gstate)

        self.gstate.referencePoint1 = irp0
        self.gstate.referencePoint2 = ip
        if instruction.mnemonic.id == self.C.MSIRP_M:
            self.gstate.referencePoint0 = ip
        self.debugInstruction(instruction, dict(ip=ip, rp0=rp0))
        return True

    i_MSIRP_m = i_MSIRP
    i_MSIRP_M = i_MSIRP

    def i_MIRP(self, instruction):
        """
        ``MIRP[abcde] // Move Indirect Relative Point``

        [m....] Do not set rp0 to point p after move;
        [M....] Set rp0 to p after move;
        [.<...] Do not keep distance greater than or equal to MinimumDistance
        [.>...] Keep distance greater than or equal to MinimumDistance
        [..r..] Do not round distance
        [..R..] Do round distance
        [...Wh] Distance type for engine characteristics compensation
        [...Bl]
        [...Gr]

        A MIRP instruction makes it possible to preserve the distance between
        two points subject to a number of qualifications. Depending upon the setting of
        Boolean flag b, the distance can be kept greater than or equal to the value
        established by the minimum_distance state variable.  Similarly, the instruction
        can be set to round the distance according to the round_state graphics state
        variable. The value of the minimum distance variable is the smallest possible
        value the distance between two points can be rounded to. Additionally, if the c
        Boolean is set, the MIRP instruction acts subject to the control_value_cut_in.
        If the difference between the actual measurement and the value in the CVT is
        sufficiently small (less than the cut_in_value), the CVT value will be used and
        not the actual value. If the device space difference between this distance from
        the CVT and the single_width_value is smaller than the single_width_cut_in,
        then use the single_width_value rather than the outline or Control Value Table
        distance.
        """
        ip, icvt = self.popParams(instruction) # Absolute length as position of
        irp0 = self.gstate.getReferencePoint(0)

        if self.fails(self.gstate.boundsCvt(icvt), '[MIRP] Cvt "%s" is undefined.' % icvt) or\
            self.fails(ip is not None, '[MIRP] Point index is not defined.') or\
            self.fails(self.gstate.boundsZone(1, ip), '[MIRP] Point "%s" is outide bounds zone(1).' % ip) or\
            self.fails(irp0 is not None, '[MIRP] Reference point 0 is not defined.') or\
            self.fails(self.gstate.boundsZone(0, irp0), '[MIRP] Point "%s" is outside bounds zone(0).' % irp0):
            return False

        # Get indexed point from zone from zone pointer 0
        p = self.gstate.getZonePoint(1, ip)

        # Get the reference point
        rp0 = self.gstate.getZonePoint(0, irp0)

        # Set the current point set in the gstate, so we can calculate the
        # contextual distance to guess the matching CVT value.
        self.gstate.focusPoints = (rp0, p)

        # Get the absolute position from cvt as d in direction of projectionvector
        cvtdistance = M.value2Ft(self.gstate.getCvt(icvt, 0))

        mnemonic = instruction.mnemonic

        singlewidthvalue = M.value2Ft(self.gstate.singleWidthValue)
        singlewidthcutin = M.value2Ft(self.gstate.singleWidthCutIn  )

        # Single width test
        if abs(cvtdistance - singlewidthvalue) < singlewidthcutin:
            if cvtdistance >= 0:
                cvtdistance = singlewidthvalue
            else:
                cvtdistance = FT(-singlewidthvalue)

        # Undocumented if twilight zone code omitted here, see Freetype documentation
        orgdistance = M.ftDualProjectionMeasure(p.orgX - rp0.orgX, p.orgY - rp0.orgY, self.gstate)
        curdistance = M.ftProjectionMeasure(p.x - rp0.x, p.y - rp0.y, self.gstate)

        # Auto flip test
        if self.gstate.autoFlip and (orgdistance ^ cvtdistance) < 0: # Right translation of if ( ( org_dist ^ cvt_dist ) < 0 )?
            cvtdistance = FT(-cvtdistance)

        # TODO: This may not be working right when cvt value is smaller than the minimum distance.
        # Control value cut-in and round
        if mnemonic.getAttribute(self.C.MxRP_i_ROUNDDISTANCE):
            # Undocumented, see Freetype:  Only perform cut-in test when both points
            # refer to the same zone. Test code is left out here.
            # distance is a scaled unit value
            distance = M.ftRoundD(cvtdistance, self.gstate, mnemonic.getAttribute(self.C.MxRP_i_COLOR))
        else:
            distance = M.ftRoundD(cvtdistance, self.gstate, mnemonic.getAttribute(self.C.MxRP_i_COLOR), roundState=self.C.ROUND_NONE)

        # Minimum distance test
        if mnemonic.getAttribute(self.C.MxRP_i_KEEPDISTANCE):
            if orgdistance >= 0:
                distance = M.ftMax(distance, self.gstate.minimumDistance)
            else:
                distance = M.ftMin(distance, -self.gstate.minimumDistance)

        # Move the point
        xy = M.freeMoveTo(p.x, p.y, FT(distance - curdistance), self.gstate)
        p.shiftTo(xy)
        M.touchP(p, self.gstate)

        # Remember the winglabels we are passing through, to draw them later
        self.gstate.setWingLabel(rp0, p, instruction) # Deprecated?

        # Set the reference points
        self.gstate.referencePoint1 = irp0
        self.gstate.referencePoint2 = ip

        if mnemonic.getAttribute(self.C.MxRP_i_RP2P):
            self.gstate.referencePoint0 = ip

        d = dict(icvt=icvt, cvtdistance=cvtdistance, irp0=irp0, ip=ip,
                distance=distance, orgdistance=orgdistance,
                doround=mnemonic.getAttribute(self.C.MxRP_i_ROUNDDISTANCE),
                keepdistance=mnemonic.getAttribute(self.C.MxRP_i_KEEPDISTANCE),
                setrp=mnemonic.getAttribute(self.C.MxRP_i_RP2P))

        self.debugInstruction(instruction, d)
        return True

    i_MIRP_m_lt_r_Gray = i_MIRP
    i_MIRP_M_lt_r_Gray = i_MIRP
    i_MIRP_m_gt_r_Gray = i_MIRP
    i_MIRP_M_gt_r_Gray = i_MIRP
    i_MIRP_m_lt_R_Gray = i_MIRP
    i_MIRP_M_lt_R_Gray = i_MIRP
    i_MIRP_m_gt_R_Gray = i_MIRP
    i_MIRP_M_gt_R_Gray = i_MIRP

    i_MIRP_m_lt_r_01 = i_MIRP
    i_MIRP_M_lt_r_01 = i_MIRP
    i_MIRP_m_gt_r_01 = i_MIRP
    i_MIRP_M_gt_r_01 = i_MIRP
    i_MIRP_m_lt_R_01 = i_MIRP
    i_MIRP_M_lt_R_01 = i_MIRP
    i_MIRP_m_gt_R_01 = i_MIRP
    i_MIRP_M_gt_R_01 = i_MIRP

    i_MIRP_m_lt_r_Black = i_MIRP
    i_MIRP_M_lt_r_Black = i_MIRP
    i_MIRP_m_gt_r_Black = i_MIRP
    i_MIRP_M_gt_r_Black = i_MIRP
    i_MIRP_m_lt_R_Black = i_MIRP
    i_MIRP_M_lt_R_Black = i_MIRP
    i_MIRP_m_gt_R_Black = i_MIRP
    i_MIRP_M_gt_R_Black = i_MIRP

    i_MIRP_m_lt_r_White = i_MIRP
    i_MIRP_M_lt_r_White = i_MIRP
    i_MIRP_m_gt_r_White = i_MIRP
    i_MIRP_M_gt_r_White = i_MIRP
    i_MIRP_m_lt_R_White = i_MIRP
    i_MIRP_M_lt_R_White = i_MIRP
    i_MIRP_m_gt_R_White = i_MIRP
    i_MIRP_M_gt_R_White = i_MIRP

    def i_CLEAR(self, instruction):
        """
        Code Range  0x22
        Pops    all the items on the stack (StkElt)
        Pushes  -

        Clears all elements from the stack.
        """
        self.gstate.clear()
        return True

    # TODO: to be implemented.

    def i_JMPR(self, instruction):
        """
        Code Range  0x1C
        Pops    offset: number of bytes to move instruction pointer (int32)
        Pushes  -
        Related instructions    JROF[ ], JROT[ ]

        Moves the instruction pointer to a new location specified by the offset
        popped from the stack.

        Pops an integer offset from the stack. The signed offset is added to the
        instruction pointer and execution is resumed at the new location in the
        instruction steam. The jump is relative to the position of the instruction
        itself. That is, an offset of +1 causes the instruction immediately following
        the JMPR[] instruction to be executed.
        """
        offset = self.popParams(instruction)
        self.message('JMPR, to be implemented')
        return True

    def i_JROF(self, instruction):
        """
        Code Range  0x79
        Pops    e: stack element offset: number of bytes to move instruction pointer (int32)
        Pushes  -
        Related instructions    JMPR[ ] JROT[ ]

        Moves the instruction pointer to a new location specified by the offset popped
        from the stack if the element tested has a FALSE (zero) value.

        Pops a Boolean value, e and an offset. In the case where the Boolean, e, is
        FALSE, the signed offset will be added to the instruction pointer and execution
        will be resumed at the new location; otherwise, the jump is not taken. The jump
        is relative to the position of the instruction itself.
        """
        e = self.popParams(instruction)
        self.message('JROF, to be implemented', isError=True)
        return True

    def i_JROT(self, instruction):
        """
        Code Range  0x78
        Pops    e: stack element
        offset: number of bytes to move
        instruction pointer (int32)
        Pushes  -
        Related instructions    JMPR[ ] JROF[ ]

        Moves the instruction pointer to a new location specified by the offset value
        popped from the stack if the element tested has a TRUE value.

        Pops a Boolean value, e and an offset. If the Boolean is TRUE (non-zero) the
        signed offset will be added to the instruction pointer and execution will be
        resumed at the address obtained. Otherwise, the jump is not taken. The jump is
        relative to the position of the instruction itself.
        """
        e = self.popParams(instruction)
        self.message('JROT, to be implemented', isError=True)
        return True

    def i_DELTAC1(self, instruction):
        """
        Code Range  0x73
        Pops    n: number of pairs of exception specifications and CVT entry numbers (uint32)
        argn, cn, argn-1, cn-1, , arg1, c1: pairs of CVT entry number and
        exception specifications (pairs of uint32s)
        Pushes  -
        Uses    delta shift, delta base
        Related instructions    DELTAC2[ ], DELTAC3, DELTAP1, DELTAP2, DELTAP3

        Creates an exception to one or more CVT values, each at a specified
        point size and by a specified amount.

        Pops an integer, n, followed by n pairs of exception specifications and
        control value table entry numbers. DELTAC1[] changes the value in each CVT
        entry specified at the size and by the pixel amount specified in its paired
        argument.

        The 8 bit arg component of the DELTAC1[] instruction decomposes into
        two parts. The most significant 4 bits represent the relative number of pixels
        per em at which the exception is applied. The least significant 4 bits
        represent the magnitude of the change to be made.

        The relative number of pixels per em is a function of the value
        specified in the argument and the delta base. The DELTAC1[] instruction works
        at pixel per em sizes beginning with the delta base through the delta_base +
        15. To invoke an exception at a larger pixel per em size, use the DELTAC2[] or
        DELTAC3[] instruction which can affect changes at sizes up to delta_base + 47
        or, if necessary, increase the value of the delta base.

        The magnitude of the move is specified, in a coded form, in the
        instruction. Table 5 lists the mapping from exception values and the magnitude
        of the move made.The size of the step depends on the value of the delta shift.
        """
        n = self.popParams(instruction)

        # Popping n parameters.
        for i in range(n):
            p = self.popParams(instruction)
            #TODO: Do something.

        self.message('DELTAC1, to be implemented', isError=True)
        return True

    i_DELTAC2 = i_DELTAC1
    i_DELTAC3 = i_DELTAC1

    i_DELTAP1 = i_DELTAC1
    i_DELTAP2 = i_DELTAC1
    i_DELTAP3 = i_DELTAC1

    '''

    # Deprecated, see i_DELTAC1.

    def i_DELTAP1(self, instruction):
        """
        DELTAP1 moves the specified points at the size and by the amount
        specified in the paired argument. An arbitrary number of points and arguments
        can be specified.  The grouping [pi, argi] can be executed n times. The value
        of argi may vary between iterations.
        """
        n = self.popParams(instruction)

        # FIXME: pop errors.
        for i in range(n):
            ip, arg = self.gstate.pop(2)
            # Nothing here yet

    i_DELTAP2 = i_DELTAP3 = i_DELTAP1
    '''

