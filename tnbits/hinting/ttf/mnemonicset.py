# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    mnemonicset.py
#

from tnbits.toolbox.transformer import TX
from tnbits.constants import Constants as C
from tnbits.hinting.ttf.mnemonic import Mnemonic
import traceback

class MnemonicSet(object):
    """
    Global mnemonic values, to be inherited by Instruction.
    """

    BY        = C.PARAMTYPE_BYTE
    WD        = C.PARAMTYPE_WORD
    LO        = C.PARAMTYPE_LONG
    UL        = C.PARAMTYPE_ULONG
    IN        = C.PARAMTYPE_INTEGER
    PT        = C.PARAMTYPE_POINT # Long
    NPT        = C.PARAMTYPE_NPOINT # One or more points
    FX        = C.PARAMTYPE_FIXED # Integer value for 1/64 pixel size.
    I16        = C.PARAMTYPE_INT16
    I32        = C.PARAMTYPE_INT32
    U32        = C.PARAMTYPE_USHORT32
    F32        = C.PARAMTYPE_FLAG32 # Flags padded to 32 bits
    V_        = C.PARAMTYPE_V_ # @@@ Check on type
    CV        = C.PARAMTYPE_CVT
    N        = UL # n-count, defining number of parameters on stack that follow

    # Conversion of push attributes to bit numbers.
    NUM2BIT = {0: '000', 1: '001', 2: '010', 3: '011', 4: '100', 5: '101', 6: '110', 7: '111'}

    '''
    Pushing data onto the interpreter stack
    Note that the pop and push parameters are in reversed order
    compared to the mnemonic documentation, since they push/pop
    in reverse order.
    '''
    MNEMONICS = (

    # id | Instruction | code | # Params | Skip | Pop, Push | Method | RoboHint | Raw code | Free names | Comment

    # Non standard mnemonics
    Mnemonic(C.PUSH, 3002, [], None, [N], None, 'push', 'PUSH', 'PUSH[]', 'push', 'Generic push.'),
    # Standard mnemonics
    Mnemonic(C.NPUSHB, 0x40, [], None, [N], None, 'npushb', 'NPUSHB[]', 'NPUSHB[]', 'push n bytes', 'Push N Bytes.'),
    Mnemonic(C.NPUSHW, 0x41, [], None, [N], None, 'npushw', 'NPUSHW[]', 'NPUSHW[]', 'push n words', 'Push N Words.'),

    Mnemonic(C.PUSHB, 0xB0, [], 1, [BY], [], 'pushb', 'PUSHB[]', 'PUSHB[]', 'pushb', 'Push 1 Byte.'),
    Mnemonic(C.PUSHB_1, 0xB0, [], 1, [BY], [], 'pushb', 'PUSHB[1]', 'PUSHB[000]', 'push 1b', 'Push 1 Byte.'),
    Mnemonic(C.PUSHB_2, 0xB1, [], 2, [BY]*2, [], 'pushb', 'PUSHB[2]', 'PUSHB[001]', 'push 2b', 'Push 2 Bytes.'),
    Mnemonic(C.PUSHB_3, 0xB2, [], 3, [BY]*3, [], 'pushb', 'PUSHB[3]', 'PUSHB[010]', 'push 3b', 'Push 3 Bytes.'),
    Mnemonic(C.PUSHB_4, 0xB3, [], 4, [BY]*4, [], 'pushb', 'PUSHB[4]', 'PUSHB[011]', 'push 4b', 'Push 4 Bytes.'),
    Mnemonic(C.PUSHB_5, 0xB4, [], 5, [BY]*5, [], 'pushb', 'PUSHB[5]', 'PUSHB[100]', 'push 5b', 'Push 5 Bytes.'),
    Mnemonic(C.PUSHB_6, 0xB5, [], 6, [BY]*6, [], 'pushb', 'PUSHB[6]', 'PUSHB[101]', 'push 6b', 'Push 6 Bytes.'),
    Mnemonic(C.PUSHB_7, 0xB6, [], 7, [BY]*7, [], 'pushb', 'PUSHB[7]', 'PUSHB[110]', 'push 7b', 'Push 7 Bytes.'),
    Mnemonic(C.PUSHB_8, 0xB7, [], 8, [BY]*8, [], 'pushb', 'PUSHB[8]', 'PUSHB[111]', 'push 8b', 'Push 8 Bytes.'),

    Mnemonic(C.PUSHW, 0xB8, [], 2, [WD], [], 'pushw', 'PUSHW[]', 'PUSHW[]', 'pushw', 'Push 1 Word.'),
    Mnemonic(C.PUSHW_1, 0xB8, [], 2, [WD], [], 'pushw', 'PUSHW[1]', 'PUSHW[000]', 'push 1w', 'Push 1 Word.'),
    Mnemonic(C.PUSHW_2, 0xB9, [], 4, [WD]*2, [], 'pushw', 'PUSHW[2]', 'PUSHW[001]', 'push 2w', 'Push 2 Words.'),
    Mnemonic(C.PUSHW_3, 0xBA, [], 6, [WD]*3, [], 'pushw', 'PUSHW[3]', 'PUSHW[010]', 'push 3w', 'Push 3 Words.'),
    Mnemonic(C.PUSHW_4, 0xBB, [], 8, [WD]*4, [], 'pushw', 'PUSHW[4]', 'PUSHW[011]', 'push 4w', 'Push 4 Words.'),
    Mnemonic(C.PUSHW_5, 0xBC, [], 10, [WD]*5, [], 'pushw', 'PUSHW[5]', 'PUSHW[100]', 'push 5w', 'Push 5 Words.'),
    Mnemonic(C.PUSHW_6, 0xBD, [], 12, [WD]*6, [], 'pushw', 'PUSHW[6]', 'PUSHW[101]', 'push 6w', 'Push 6 Words.'),
    Mnemonic(C.PUSHW_7, 0xBE, [], 14, [WD]*7, [], 'pushw', 'PUSHW[7]', 'PUSHW[110]', 'push 7w', 'Push 7 Words.'),
    Mnemonic(C.PUSHW_8, 0xBF, [], 16, [WD]*8, [], 'pushw', 'PUSHW[8]', 'PUSHW[111]', 'push 8w', 'Push 8 Words.'),

    # Managing the Storage Area
    Mnemonic(C.RS, 0x43, [], 0, [UL], [UL], None, 'RS[]', 'RS[]', 'read store', 'Read Store. Pops location: Storage Area location (ULONG) Pushes value: Storage Area value (ULONG) Gets Storage Area value.'),
    Mnemonic(C.WS, 0x42, [], 0, [UL]*2, [], None, 'WS[]', 'WS[]', 'write store', 'Write Store. Pops value: Storage Area value (ULONG) location: Storage Area location (ULONG).'),
    # Managing the Control Value Table
    Mnemonic(C.WCVTP, 0x44, [], 0, [CV,FX], [], None, 'WCVTP[]', 'WCVTP[]', 'write cvt pixel', 'Write Control Value Table in Pixel units. Pops a location and a value from the stack and puts that value in the specified location in the Control Value Table. This instruction assumes the value is in pixels and not in FUnits.'),
    Mnemonic(C.WCVTF, 0x70, [], 0, [CV,UL], [], None, 'WCVTF[]', 'WCVTF[]', 'write cvt fixed', 'Write Control Value Table in FUnits. .'),
    Mnemonic(C.RCVT, 0x45, [], 0, [CV], [FX], None, 'RCVT[]', 'RCVT[]', 'read cvt', 'Read Control Value Table. Pops a location from the stack and pushes the value in the location specified in the Control Value Table onto the stack.'),

    # Manage the Gaphics State
    Mnemonic(C.SVTCA_Y, 0x00, [0], 0, [], [], None, 'SVTCA[Y]', 'SVTCA[0]', 'y', 'Set freedom and projection Vectors to y-axis.'),
    Mnemonic(C.SVTCA_X, 0x01, [1], 0, [], [], None, 'SVTCA[X]', 'SVTCA[1]', 'x', 'Set freedom and projection Vectors to x-axis.'),
    Mnemonic(C.SPVTCA_Y, 0x02, [0], 0, [], [], None, 'SPVTCA[Y]', 'SPVTCA[0]', 'projection y', 'Set Projection Vector to y-axis.'),
    Mnemonic(C.SPVTCA_X, 0x03, [1], 0, [], [], None, 'SPVTCA[X]', 'SPVTCA[1]', 'projection x', 'Set Projection Vector to x-axis.'),
    Mnemonic(C.SFVTCA_Y, 0x04, [0], 0, [], [], None, 'SFVTCA[Y]', 'SFVTCA[0]', 'freedom y', 'Set Freedom Vector to y-axis.'),
    Mnemonic(C.SFVTCA_X, 0x05, [1], 0, [], [], None, 'SFVTCA[X]', 'SFVTCA[1]', 'freedom x', 'Set Freedom Vector to x-axis.'),
    Mnemonic(C.SPVTL_r, 0x07, [0], 0, [PT]*2, [], None, 'SPVTL[r]', 'SPVTL[0]', 'projection to line', 'Set Projection Vector to Line parallel Pt1 and Pt2.'),
    Mnemonic(C.SPVTL_R, 0x06, [1], 0, [PT]*2, [], None, 'SPVTL[R]', 'SPVTL[1]', 'projection perpendicular to line','Set Projection Vector to Line perpendicular Pt1 and Pt2.'),
    Mnemonic(C.SFVTL_r, 0x08, [0], 0, [PT]*2, [], None, 'SFVTL[r]', 'SFVTL[0]', 'freedom to line', 'Set Freedom Vector to Line parallel Pt1 and Pt2.'),
    Mnemonic(C.SFVTL_R, 0x09, [1], 0, [PT]*2, [], None, 'SFVTL[R]', 'SFVTL[1]', 'freedom perpendicular to line','Set Freedom Vector to Line perpendicular Pt1 and Pt2.'),
    Mnemonic(C.SFVTPV, 0x0E, [], 0, [], [], None, 'SFVTPV[]', 'SFVTPV[]', 'freedom to projection', 'Set Freedom Vector to Projection Vector.'),
    Mnemonic(C.SDPVTL_r, 0x86, [0], 0, [PT]*2, [], None, 'SDPVTL[r]', 'SDPVTL[0]', 'dual projection to line', 'Set Dual Projection Vector to Line parallel Pt1 and Pt2.'),
    Mnemonic(C.SDPVTL_R, 0x87, [1], 0, [PT]*2, [], None, 'SDPVTL[R]', 'SDPVTL[1]', 'dual projection perpendicular to line', 'Set Dual Projection Vector to Line perpendicular Pt1 and Pt2.'),
    Mnemonic(C.SPVFS, 0x0A, [], 0, [PT]*2, [], None, 'SPVFS[]', 'SPVFS[]', 'projection from stack', 'Set Projection Vector from Stack Pt1 and Pt2.'),
    Mnemonic(C.SFVFS, 0x0B, [], 0, [FX]*2, [], None, 'SFVFS[]', 'SFVFS[]', 'freedom from stack', 'Set Freedom Vector from Stack. Pops x and y component of the Freedom Vector.'),
    Mnemonic(C.GPV, 0x0C, [], 0, [], [FX]*2, None, 'GPV[]', 'GPV[]', 'get projection', 'Get Projection Vector.'),
    Mnemonic(C.GFV, 0x0D, [], 0, [], [FX]*2, None, 'GFV[]', 'GFV[]', 'get freedom', 'Get Freedom Vector.'),
    Mnemonic(C.SRP0, 0x10, [], 1, [PT], [], None, 'SRP0[]', 'SRP0[]', 'reference0', 'Set Reference Point 0.'),
    Mnemonic(C.SRP1, 0x11, [], 1, [PT], [], None, 'SRP1[]', 'SRP1[]', 'reference1', 'Set Reference Point 1.'),
    Mnemonic(C.SRP2, 0x12, [], 1, [PT], [], None, 'SRP2[]', 'SRP2[]', 'reference2', 'Set Reference Point 2.'),
    Mnemonic(C.SZP0, 0x13, [], 0, [UL], [], None, 'SZP0[]', 'SZP0[]', 'zone0', 'Set Zone Pointer 0 to zone number.'),
    Mnemonic(C.SZP1, 0x14, [], 0, [UL], [], None, 'SZP1[]', 'SZP1[]', 'zone1', 'Set Zone Pointer 1 to zone number.'),
    Mnemonic(C.SZP2, 0x15, [], 0, [UL], [], None, 'SZP2[]', 'SZP2[]', 'zone2', 'Set Zone Pointer 2 (zp2) to zone number.'),
    Mnemonic(C.SZPS, 0x16, [], 0, [UL], [], None, 'SZPS[]', 'SZPS[]', 'zones', 'Set Zone PointerS zp0, zp1, zp2 to zone number.'),
    Mnemonic(C.RTHG, 0x19, [], 0, [], [], None, 'RTHG[]', 'RTHG[]', 'round half grid', 'Round To Half Grid.'),
    Mnemonic(C.RTG, 0x18, [], 0, [], [], None, 'RTG[]', 'RTG[]', 'round grid', 'Round To Full Grid.'),
    Mnemonic(C.RTDG, 0x3D, [], 0, [], [], None, 'RTDG[]', 'RTDG[]', 'round double grid', 'Round To Double Grid.'),
    Mnemonic(C.RDTG, 0x7D, [], 0, [], [], None, 'RDTG[]', 'RDTG[]', 'round down grid', 'Round Down To Grid.'),
    Mnemonic(C.RUTG, 0x7C, [], 0, [], [], None, 'RUTG[]', 'RUTG[]', 'round up grid', 'Round Up To Grid.'),
    Mnemonic(C.ROFF, 0x7A, [], 0, [], [], None, 'ROFF[]', 'ROFF[]', 'round off', 'Round OFF.'),
    Mnemonic(C.SROUND, 0x76, [], 0, [LO], [], None, 'SROUND[]', 'SROUND[]', 'round super', 'Super ROUND. pops number decomposed to obtain period, phase, threshold.'),
    Mnemonic(C.S45ROUND, 0x77, [], 0, [UL], [], None, 'S45ROUND[]', 'S45ROUND[]', 'round super45', 'Super ROUND 45 degrees.'),
    Mnemonic(C.SLOOP, 0x17, [], 0, [V_], [], None, 'SLOOP[]', 'SLOOP[]', 'loop', 'Set LOOP variable to amount of iterations.'),
    Mnemonic(C.SMD, 0x1A, [], 0, [FX], [], None, 'SMD[]', 'SMD[]', 'minimum distance', 'Set Minimum Distance variable.'),
    Mnemonic(C.INSTCTRL, 0x8E, [], 0, [I32,U32], [], None, 'INSTCTRL[]', 'INSTCTRL[]', 'instruction control', 'INSTRuction execution ConTRoL.'),
    Mnemonic(C.SCANCTRL, 0x85, [], 0, [F32], [], None, 'SCANCTRL[]', 'SCANCTRL[]', 'scan conversion control', 'SCAN conversion ConTRoL.'),
    Mnemonic(C.SCANTYPE, 0x8D, [], 0, [I32], [], None, 'SCANTYPE[]', 'SCANTYPE[]', 'scan type', 'SCANTYPE.'),
    Mnemonic(C.SCVTCI, 0x1D, [], 0, [FX], [], None, 'SCVTCI[]', 'SCVTCI[]', 'cvt cutin', 'Set Control Value Table Cut In.'),
    Mnemonic(C.SSWCI, 0x1E, [], 0, [FX], [], None, 'SSWCI[]', 'SSWCI[]', 'single width cutin', 'Set Single Width Cut In.'),
    Mnemonic(C.SSW, 0x1F, [], 0, [V_], [], None, 'SSW[]', 'SSW[]', 'single width', 'Set Single Width.'),
    Mnemonic(C.FLIPON, 0x4D, [], 0, [], [], None, 'FLIPON[]', 'FLIPON[]', 'flip on', 'Set the auto flip Boolean to ON.'),
    Mnemonic(C.FLIPOFF, 0x4E, [], 0, [], [], None, 'FLIPOFF[]', 'FLIPOFF[]', 'flip off', 'Set the auto flip Boolean to OFF.'),
    Mnemonic(C.SANGW, 0x7E, [], 0, [V_], [], None, 'SANGW[]', 'SANGW[]', 'angle weight', 'Set Angle Weight is no longer needed because of dropped support to the AA instruction.'),
    Mnemonic(C.AA, 0x7F, [], 0, None, None, None, 'AA[]', 'AA[]', 'adjust angle', 'Adjust Angle. No longer in use, dropped support.'),
    Mnemonic(C.SDB, 0x5E, [], 0, [UL], [], None, 'SDB[]', 'SDB[]', 'delta base', 'Set Delta Base in the graphics state. Default value is 9.'),
    Mnemonic(C.SDS, 0x5F, [], 0, [UL], [], None, 'SDS[]', 'SDS[]', 'delta shift', 'Set Delta Shift in the graphics state. Default value is 3.'),

    # Reading and writing data
    Mnemonic(C.GC_curp, 0x46, [0], 0, [PT], [FX], None, 'GC[0]', 'GC[0]', 'projected position', 'Get Coordinate projected onto the ProjectionVector at the current position.'),
    Mnemonic(C.GC_orgp, 0x47, [1], 0, [PT], [FX], None, 'GC[N]', 'GC[1]', 'projected original position', 'Get Coordinate projected onto the ProjectionVector at original position.'),
    Mnemonic(C.SCFS, 0x48, [], 0, [PT,FX], [], None, 'SCFS[]', 'SCFS[]', 'coordinate from projection and freedom', 'Sets Coordinate From the Stack using ProjectionVector and FreedomVector.'),
    Mnemonic(C.MD_grid, 0x49, [0], 0, [PT]*2, [FX], None, 'MD[0]', 'MD[0]', 'measure grid', 'Measure Distance (Grid-fitted.'),
    Mnemonic(C.MD_org, 0x4A, [1], 0, [PT]*2, [FX], None, 'MD[N]', 'MD[1]', 'measure original', 'Measure Distance (Original.'),
    Mnemonic(C.MPPEM, 0x4B, [], 0, [], [UL], None, 'MPPEM[]', 'MPPEM[]', 'measure ppem', 'Measure Pixels per EM.'),
    Mnemonic(C.MPS, 0x4C, [], 0, [], [FX], None, 'MPS[]', 'MPS[]', 'measure point size', 'Measure Point Size.'),

    # Managing outlines
    Mnemonic(C.FLIPPT, 0x80, [], 0, [PT], [], None, 'FLIPPT[]', 'FLIPPT[]', 'flip point', 'FLIP PointT.'),
    Mnemonic(C.FLIPRGEON, 0x81, [], 0, [PT]*2, [], None, 'FLIPRGON[]', 'FLIPRGON[]', 'flip range on', 'FLIP RanGe ON.'),
    Mnemonic(C.FLIPRGEOFF, 0x82, [], 0, [PT]*2, [], None, 'FLIPRGOFF[]', 'FLIPRGOFF[]', 'flip range off', 'FLIP RanGe OFF.'),
    Mnemonic(C.SHP_0, 0x32, [0], 0, [NPT], [], None, 'SHP[2]', 'SHP[0]', 'shift', 'SHift Point by last point reference2 (scaled glyph zone1).'),
    Mnemonic(C.SHP_1, 0x33, [1], 0, [NPT], [], None, 'SHP[1]', 'SHP[1]', 'shift original', 'SHift Point by last point reference1 (original glyph zone0).'),
    Mnemonic(C.SHC_0, 0x34, [0], 0, [PT], [], None, 'SHC[2]', 'SHC[0]', 'shift contour', 'SHift Contour by last point reference2 (scaled glyph zone1).'),
    Mnemonic(C.SHC_1, 0x35, [1], 0, [PT], [], None, 'SHC[1]', 'SHC[1]', 'shift contour original', 'SHift Contour by last point reference1 (scaled glyph zone0).'),
    Mnemonic(C.SHZ_0, 0x36, [0], 0, [PT], [], None, 'SHZ[2]', 'SHZ[0]', 'shift zone', 'SHift Zone by last point reference2 (scaled glyph zone1).'),
    Mnemonic(C.SHZ_1, 0x37, [1], 0, [PT], [], None, 'SHZ[1]', 'SHZ[1]', 'shift zone original', 'SHift Zone by last point reference1 (original glyph zone0).'),
    Mnemonic(C.SHPIX, 0x38, [], 0, None, [], None, 'SHPIX[]', 'SHPIX[]', 'shift zone pixels', 'SHift point by a PIXel amount.'),
    Mnemonic(C.MSIRP_m, 0x3A, [0], 0, [UL,FX], [], None, 'MSIRP[m]', 'MSIRP[0]', 'relative', 'Move Stack Indirect Relative Point. Not set reference0 to p.'),
    Mnemonic(C.MSIRP_M, 0x3B, [1], 0, [UL,FX], [], None, 'MSIRP[M]', 'MSIRP[1]', 'relative reference', 'Move Stack Indirect Relative Point. Set reference0 to p.'),
    Mnemonic(C.MDAP_r, 0x2E, [0], 0, [PT], [], None, 'MDAP[r]', 'MDAP[0]', 'direct', 'Move Direct Absolute Point. Not round value.'),
    Mnemonic(C.MDAP_R, 0x2F, [1], 0, [PT], [], None, 'MDAP[R]', 'MDAP[1]', 'direct round', 'Move Direct Absolute Point. Round value.'),
    Mnemonic(C.MIAP_r, 0x3E, [0], 0, [PT,CV], [], None, 'MIAP[r]', 'MIAP[0]', 'indirect', 'Move Indirect Absolute Point. Not round distance.'),
    Mnemonic(C.MIAP_R, 0x3F, [1], 0, [PT,CV], [], None, 'MIAP[R]', 'MIAP[1]', 'indirect round', 'Move Indirect Absolute Point. Round distance.'),

    Mnemonic(C.MDRP_m_lt_r_Gray, 0xC0, [0,0,0,0], 0, [PT], [], None, 'MDRP[m<rGr]', 'MDRP[00000]', 'gray', 'Move Direct Relative Point. Can be 0. Gray.'),
    Mnemonic(C.MDRP_m_lt_r_Black, 0xC1, [0,0,0,1], 0, [PT], [], None, 'MDRP[m<rBl]', 'MDRP[00001]', 'black', 'Move Direct Relative Point. Can be 0. Black.'),
    Mnemonic(C.MDRP_m_lt_r_White, 0xC2, [0,0,0,2], 0, [PT], [], None, 'MDRP[m<rWh]', 'MDRP[00010]', 'white', 'Move Direct Relative Point. Can be 0. White.'),
    Mnemonic(C.MDRP_m_lt_R_Gray, 0xC4, [0,0,1,0], 0, [PT], [], None, 'MDRP[m<RGr]', 'MDRP[00100]', 'round gray', 'Move Direct Relative Point. Can be 0. Round Gray.'),
    Mnemonic(C.MDRP_m_lt_R_Black, 0xC5, [0,0,1,1], 0, [PT], [], None, 'MDRP[m<RBl]', 'MDRP[00101]', 'round black', 'Move Direct Relative Point. Can be 0. Round Black.'),
    Mnemonic(C.MDRP_m_lt_R_White, 0xC6, [0,0,1,2], 0, [PT], [], None, 'MDRP[m<RWh]', 'MDRP[00110]', 'round white', 'Move Direct Relative Point. Can be 0. Round White.'),
    Mnemonic(C.MDRP_m_gt_r_Gray, 0xC8, [0,1,0,0], 0, [PT], [], None, 'MDRP[m>rGr]', 'MDRP[01000]', 'min gray', 'Move Direct Relative Point. Keep equal or greater than minimal value. Gray.'),
    Mnemonic(C.MDRP_m_gt_r_Black, 0xC9, [0,1,0,1], 0, [PT], [], None, 'MDRP[m>rBl]', 'MDRP[01001]', 'min black', 'Move Direct Relative Point. Keep equal or greater than minimal value. Black.'),
    Mnemonic(C.MDRP_m_gt_r_White, 0xCA, [0,1,0,2], 0, [PT], [], None, 'MDRP[m>rWh]', 'MDRP[01010]', 'min white', 'Move Direct Relative Point. Keep equal or greater than minimal value. White.'),
    Mnemonic(C.MDRP_m_gt_R_Gray, 0xCC, [0,1,1,0], 0, [PT], [], None, 'MDRP[m>RGr]', 'MDRP[01100]', 'min round gray', 'Move Direct Relative Point. Keep equal or greater than minimal value. Round Gray.'),
    Mnemonic(C.MDRP_m_gt_R_Black, 0xCD, [0,1,1,1], 0, [PT], [], None, 'MDRP[m>RBl]', 'MDRP[01101]', 'min round black', 'Move Direct Relative Point. Keep equal or greater than minimal value. Round Black.'),
    Mnemonic(C.MDRP_m_gt_R_White, 0xCE, [0,1,1,2], 0, [PT], [], None, 'MDRP[m>RWh]', 'MDRP[01110]', 'min round white', 'Move Direct Relative Point. Keep equal or greater than minimal value. Round White.'),
    Mnemonic(C.MDRP_M_lt_r_Gray, 0xD0, [1,0,0,0], 0, [PT], [], None, 'MDRP[M<rGr]', 'MDRP[10000]', 'reference gray', 'Move Direct Relative Point. Move reference0. Can be 0. Gray.'),
    Mnemonic(C.MDRP_M_lt_r_Black, 0xD1, [1,0,0,1], 0, [PT], [], None, 'MDRP[M<rBl]', 'MDRP[10001]', 'reference black', 'Move Direct Relative Point. Move reference0. Can be 0. Black.'),
    Mnemonic(C.MDRP_M_lt_r_White, 0xD2, [1,0,0,2], 0, [PT], [], None, 'MDRP[M<rWh]', 'MDRP[10010]', 'reference white', 'Move Direct Relative Point. Move reference0. Can be 0. White.'),
    Mnemonic(C.MDRP_M_lt_R_Gray, 0xD4, [1,0,1,0], 0, [PT], [], None, 'MDRP[M<RGr]', 'MDRP[10100]', 'reference round gray', 'Move Direct Relative Point. Move reference0. Can be 0. Round Gray.'),
    Mnemonic(C.MDRP_M_lt_R_Black, 0xD5, [1,0,1,1], 0, [PT], [], None, 'MDRP[M<RBl]', 'MDRP[10101]', 'reference round black', 'Move Direct Relative Point. Move reference0. Can be 0. Round Black.'),
    Mnemonic(C.MDRP_M_lt_R_White, 0xD6, [1,0,1,2], 0, [PT], [], None, 'MDRP[M<RWh]', 'MDRP[10110]', 'reference round white', 'Move Direct Relative Point. Move reference0. Can be 0. Round White.'),
    Mnemonic(C.MDRP_M_gt_r_Gray, 0xD8, [1,1,0,0], 0, [PT], [], None, 'MDRP[M>rGr]', 'MDRP[11000]', 'reference min gray', 'Move Direct Relative Point. Move reference0. Keep equal or greater than minimal value. Gray.'),
    Mnemonic(C.MDRP_M_gt_r_Black, 0xD9, [1,1,0,1], 0, [PT], [], None, 'MDRP[M>rBl]', 'MDRP[11001]', 'reference min black', 'Move Direct Relative Point. Move reference0. Keep equal or greater than minimal value. Gray.'),
    Mnemonic(C.MDRP_M_gt_r_White, 0xDA, [1,1,0,2], 0, [PT], [], None, 'MDRP[M>rWh]', 'MDRP[11010]', 'reference min white', 'Move Direct Relative Point. Move reference0. Keep equal or greater than minimal value. Black.'),
    Mnemonic(C.MDRP_M_gt_R_Gray, 0xDC, [1,1,1,0], 0, [PT], [], None, 'MDRP[M>RGr]', 'MDRP[11100]', 'reference min round gray', 'Move Direct Relative Point. Move reference0. Keep equal or greater than minimal value. Round Gray.'),
    Mnemonic(C.MDRP_M_gt_R_Black, 0xDD, [1,1,1,1], 0, [PT], [], None, 'MDRP[M>RBl]', 'MDRP[11101]', 'reference min round black', 'Move Direct Relative Point. Move reference0. Keep equal or greater than minimal value. Round Black.'),
    Mnemonic(C.MDRP_M_gt_R_White, 0xDE, [1,1,1,2], 0, [PT], [], None, 'MDRP[M>RWh]', 'MDRP[11110]', 'reference min round white', 'Move Direct Relative Point. Move reference0. Keep equal or greater than minimal value. Round White.'),

    Mnemonic(C.MIRP_m_lt_r_Gray, 0xE0, [0,0,0,0], 0, [PT,CV], [], None, 'MIRP[m<rGr]', 'MIRP[00000]', 'indirect gray', 'Move Indirect Relative Point. Can be 0. Gray.'),
    Mnemonic(C.MIRP_m_lt_r_Black, 0xE1, [0,0,0,1], 0, [PT,CV], [], None, 'MIRP[m<rBl]', 'MIRP[00001]', 'indirect black', 'Move Indirect Relative Point. Can be 0. Black.'),
    Mnemonic(C.MIRP_m_lt_r_White, 0xE2, [0,0,0,2], 0, [PT,CV], [], None, 'MIRP[m<rWh]', 'MIRP[00010]', 'indirect white', 'Move Indirect Relative Point. Can be 0. White.'),
    Mnemonic(C.MIRP_m_lt_R_Gray, 0xE4, [0,0,1,0], 0, [PT,CV], [], None, 'MIRP[m<RGr]', 'MIRP[00100]', 'indirect round gray', 'Move Indirect Relative Point. Can be 0. Round Gray.'),
    Mnemonic(C.MIRP_m_lt_R_Black, 0xE5, [0,0,1,1], 0, [PT,CV], [], None, 'MIRP[m<RBl]', 'MIRP[00101]', 'indirect round black', 'Move Indirect Relative Point. Can be 0. Round Black.'),
    Mnemonic(C.MIRP_m_lt_R_White, 0xE6, [0,0,1,2], 0, [PT,CV], [], None, 'MIRP[m<RWh]', 'MIRP[00110]', 'indirect round white', 'Move Indirect Relative Point. Can be 0. Round White.'),
    Mnemonic(C.MIRP_m_gt_r_Gray, 0xE8, [0,1,0,0], 0, [PT,CV], [], None, 'MIRP[m>rGr]', 'MIRP[01000]', 'indirect min gray', 'Move Indirect Relative Point. Keep equal or greater than minimal value. Gray.'),
    Mnemonic(C.MIRP_m_gt_r_Black, 0xE9, [0,1,0,1], 0, [PT,CV], [], None, 'MIRP[m>rBl]', 'MIRP[01001]', 'indirect min black', 'Move Indirect Relative Point. Keep equal or greater than minimal value. Black.'),
    Mnemonic(C.MIRP_m_gt_r_White, 0xEA, [0,1,0,2], 0, [PT,CV], [], None, 'MIRP[m>rWh]', 'MIRP[01010]', 'indirect min white', 'Move Indirect Relative Point. Keep equal or greater than minimal value. White.'),
    Mnemonic(C.MIRP_m_gt_R_Gray, 0xEC, [0,1,1,0], 0, [PT,CV], [], None, 'MIRP[m>RGr]', 'MIRP[01100]', 'indirect min round gray', 'Move Indirect Relative Point. Keep equal or greater than minimal value. Round Gray.'),
    Mnemonic(C.MIRP_m_gt_R_Black, 0xED, [0,1,1,1], 0, [PT,CV], [], None, 'MIRP[m>RBl]', 'MIRP[01101]', 'indirect min round black', 'Move Indirect Relative Point. Keep equal or greater than minimal value. Round Black.'),
    Mnemonic(C.MIRP_m_gt_R_White, 0xEE, [0,1,1,2], 0, [PT,CV], [], None, 'MIRP[m>RWh]', 'MIRP[01110]', 'indirect min round white', 'Move Indirect Relative Point. Keep equal or greater than minimal value. Round White.'),
    Mnemonic(C.MIRP_M_lt_r_Gray, 0xF0, [1,0,0,0], 0, [PT,CV], [], None, 'MIRP[M<rGr]', 'MIRP[10000]', 'indirect reference gray', 'Move Indirect Relative Point. Move reference0. Can be 0. Gray.'),
    Mnemonic(C.MIRP_M_lt_r_Black, 0xF1, [1,0,0,1], 0, [PT,CV], [], None, 'MIRP[M<rBl]', 'MIRP[10001]', 'indirect reference black', 'Move Indirect Relative Point. Move reference0. Can be 0. Black.'),
    Mnemonic(C.MIRP_M_lt_r_White, 0xF2, [1,0,0,2], 0, [PT,CV], [], None, 'MIRP[M<rWh]', 'MIRP[10010]', 'indirect reference white', 'Move Indirect Relative Point. Move reference0. Can be 0. White.'),
    Mnemonic(C.MIRP_M_lt_R_Gray, 0xF4, [1,0,1,0], 0, [PT,CV], [], None, 'MIRP[M<RGr]', 'MIRP[10100]', 'indirect reference round gray', 'Move Indirect Relative Point. Move reference0. Can be 0. Round Gray.'),
    Mnemonic(C.MIRP_M_lt_R_Black, 0xF5, [1,0,1,1], 0, [PT,CV], [], None, 'MIRP[M<RBl]', 'MIRP[10101]', 'indirect reference round black', 'Move Indirect Relative Point. Move reference0. Can be 0. Round Black.'),
    Mnemonic(C.MIRP_M_lt_R_White, 0xF6, [1,0,1,2], 0, [PT,CV], [], None, 'MIRP[M<RWh]', 'MIRP[10110]', 'indirect reference round white', 'Move Indirect Relative Point. Move reference0. Can be 0. Round White.'),
    Mnemonic(C.MIRP_M_gt_r_Gray, 0xF8, [1,1,0,0], 0, [PT,CV], [], None, 'MIRP[M>rGr]', 'MIRP[11000]', 'indirect reference min gray', 'Move Indirect Relative Point. Move reference0. Keep equal or greater than minimal value. Gray.'),
    Mnemonic(C.MIRP_M_gt_r_Black, 0xF9, [1,1,0,1], 0, [PT,CV], [], None, 'MIRP[M>rBl]', 'MIRP[11001]', 'indirect reference min black', 'Move Indirect Relative Point. Move reference0. Keep equal or greater than minimal value. Black.'),
    Mnemonic(C.MIRP_M_gt_r_White, 0xFA, [1,1,0,2], 0, [PT,CV], [], None, 'MIRP[M>rWh]', 'MIRP[11010]', 'indirect reference min white', 'Move Indirect Relative Point. Move reference0. Keep equal or greater than minimal value. White.'),
    Mnemonic(C.MIRP_M_gt_R_Gray, 0xFC, [1,1,1,0], 0, [PT,CV], [], None, 'MIRP[M>RGr]', 'MIRP[11100]', 'indirect reference min round gray','Move Indirect Relative Point. Move reference0. Keep equal or greater than minimal value. Round Gray.'),
    Mnemonic(C.MIRP_M_gt_R_Black, 0xFD, [1,1,1,1], 0, [PT,CV], [], None, 'MIRP[M>RBl]', 'MIRP[11101]', 'indirect reference min round black','Move Indirect Relative Point. Move reference0. Keep equal or greater than minimal value. Round Black.'),
    Mnemonic(C.MIRP_M_gt_R_White, 0xFE, [1,1,1,2], 0, [PT,CV], [], None, 'MIRP[M>RWh]', 'MIRP[11110]', 'indirect reference min round white','Move Indirect Relative Point. Move reference0. Keep equal or greater than minimal value. Round White.'),

    Mnemonic(C.ALIGNRP, 0x3C, [], 0, [PT], [], None, 'ALIGNRP[]', 'ALIGNRP[]', 'align', 'ALIGN Relative Point (p) to reference0.'),
    Mnemonic(C.ISECT, 0x0F, [], 0, [PT]*5, [], None, 'ISECT[]', 'ISECT[]', 'intersect', 'Moves point p to the InterSECTion of two lines.'),
    Mnemonic(C.ALIGNPTS, 0x27, [], 0, [PT]*2, [], None, 'ALIGNPTS[]', 'ALIGNPTS[]', 'align points', 'ALIGN Points.'),
    Mnemonic(C.IP, 0x39, [], 0, [PT], [], None, 'IP[]', 'IP[]', 'interpolate', 'Interpolate Point by the last relative stretch.'),
    Mnemonic(C.UTP, 0x29, [], 0, [PT], [], None, 'UTP[]', 'UTP[]', 'untouch', 'UnTouch Point.'),
    Mnemonic(C.IUP_Y, 0x30, [0], 0, [], [], None, 'IUP[Y]', 'IUP[0]', 'interpolate y', 'Interpolate Untouched Points through the outline to y-axis.'),
    Mnemonic(C.IUP_X, 0x31, [1], 0, [], [], None, 'IUP[X]', 'IUP[1]', 'interpolate x', 'Interpolate Untouched Points through the outline to x-axis.'),

    # Exceptions
    Mnemonic(C.DELTAP1, 0x5D, [], 1, [N], [], None, 'DELTAP1[]', 'DELTAP1[]', 'delta exception p1', 'DELTA exception P1.'),
    Mnemonic(C.DELTAP2, 0x71, [], 1, [N], [], None, 'DELTAP2[]', 'DELTAP2[]', 'delta exception p2', 'DELTA exception P2.'),
    Mnemonic(C.DELTAP3, 0x72, [], 1, [N], [], None, 'DELTAP3[]', 'DELTAP3[]', 'delta exception p3', 'DELTA exception P3.'),
    Mnemonic(C.DELTAC1, 0x73, [], 1, [N], [], None, 'DELTAC1[]', 'DELTAC1[]', 'delta exception c1', 'DELTA exception C1.'),
    Mnemonic(C.DELTAC2, 0x74, [], 1, [N], [], None, 'DELTAC2[]', 'DELTAC2[]', 'delta exception c2', 'DELTA exception C2.'),
    Mnemonic(C.DELTAC3, 0x75, [], 1, [N], [], None, 'DELTAC3[]', 'DELTAC3[]', 'delta exception c3', 'DELTA exception C3.'),

    # Managing the stack
    Mnemonic(C.DUP, 0x20, [], 0, [UL], [UL]*2, None, 'DUP[]', 'DUP[]', 'duplicate', 'Duplicate top stack element.'),
    Mnemonic(C.POP, 0x21, [], 0, [UL], [], None, 'POP[]', 'POP[]', 'pop', 'Pop top stack element.'),
    Mnemonic(C.CLEAR, 0x22, [], 0, None, [], None, 'CLEAR[]', 'CLEAR[]', 'clear stack', 'Clear the entire stack.'),
    Mnemonic(C.SWAP, 0x23, [], 0, [UL]*2, [UL]*2, None, 'SWAP[]', 'SWAP[]', 'swap', 'Swap the two top elements of the stack.'),
    Mnemonic(C.DEPTH, 0x24, [], 0, [], [UL], None, 'DEPTH[]', 'DEPTH[]', 'stack depth', 'Returns the DEPTH of the stack.'),
    Mnemonic(C.CINDEX, 0x25, [], 0, [V_], [UL], None, 'CINDEX[]', 'CINDEX[]', 'copy index', 'Copy the INDEXed element to the top of the stack.'),
    Mnemonic(C.MINDEX, 0x26, [], 0, [V_], [UL], None, 'MINDEX[]', 'MINDEX[]', 'move index', 'Move the INDEXed element to the top of the stack.'),
    Mnemonic(C.ROLL, 0x8A, [], 0, [UL]*3, [UL]*3, None, 'ROLL[]', 'ROLL[]', 'roll', 'ROLL the top three elements of the stack.'),

    # Flow control
    Mnemonic(C.IF, 0x58, [], 0, [UL], [], None, 'IF[]', 'IF[]', 'if', 'IF test.'),
    Mnemonic(C.ELSE, 0x1B, [], 0, [], [], None, 'ELSE[]', 'ELSE[]', 'else', 'ELSE.'),
    Mnemonic(C.EIF, 0x59, [], 0, [], [], None, 'EIF[]', 'EIF[]', 'end if', 'End IF.'),
    Mnemonic(C.JROT, 0x78, [], 0, [LO,UL], [], None, 'JROT[]', 'JROT[]', 'jump on true', 'Jump Relative On True.'),
    Mnemonic(C.JMPR, 0x1C, [], 0, [LO], [], None, 'JMPR[]', 'JMPR[]', 'jump', 'JuMP.'),
    Mnemonic(C.JROF, 0x79, [], 0, [LO,UL], [], None, 'JROF[]', 'JROF[]', 'jump on false', 'Jump Relative On False.'),

    # Logical functions
    Mnemonic(C.LT, 0x50, [], 0, [UL]*2, [UL], None, 'LT[]', 'LT[]', 'less than', 'Less Than.'),
    Mnemonic(C.LTEQ, 0x51, [], 0, [UL]*2, [UL], None, 'LTEQ[]', 'LTEQ[]', 'less than or equal', 'Less Than or EQual.'),
    Mnemonic(C.GT, 0x52, [], 0, [UL]*2, [UL], None, 'GT[]', 'GT[]', 'greater than', 'Greater Than.'),
    Mnemonic(C.GTEQ, 0x53, [], 0, [UL]*2, [UL], None, 'GTEQ[]', 'GTEQ[]', 'greater than or equal', 'Greater Than or EQual.'),
    Mnemonic(C.EQ, 0x54, [], 0, [UL]*2, [UL], None, 'EQ[]', 'EQ[]', 'equal', 'EQual.'),
    Mnemonic(C.NEQ, 0x55, [], 0, [UL]*2, [UL], None, 'NEQ[]', 'NEQ[]', 'not equal', 'Not EQual.'),
    Mnemonic(C.ODD, 0x56, [], 0, [UL], [UL], None, 'ODD[]', 'ODD[]', 'odd', 'ODD.'),
    Mnemonic(C.EVEN, 0x57, [], 0, [UL], [UL], None, 'EVEN[]', 'EVEN[]', 'even', 'EVEN.'),
    Mnemonic(C.AND, 0x5A, [], 0, [UL]*2, [UL], None, 'AND[]', 'AND[]', 'and', 'Logical AND.'),
    Mnemonic(C.OR, 0x5B, [], 0, [UL]*2, [UL], None, 'OR[]', 'OR[]', 'or', 'Logical OR.'),
    Mnemonic(C.NOT, 0x5C, [], 0, [UL], [UL], None, 'NOT[]', 'NOT[]', 'not', 'Logical NOT.'),

    # Arithmetic and math instructions
    Mnemonic(C.ADD, 0x60, [], 0, [FX]*2, [FX], None, 'ADD[]', 'ADD[]', 'add', 'ADD.'),
    Mnemonic(C.SUB, 0x61, [], 0, [FX]*2, [FX], None, 'SUB[]', 'SUB[]', 'subtract', 'SUBtract.'),
    Mnemonic(C.DIV, 0x62, [], 0, [FX]*2, [FX], None, 'DIV[]', 'DIV[]', 'divide', 'DIVide.'),
    Mnemonic(C.MUL, 0x63, [], 0, [FX]*2, [FX], None, 'MUL[]', 'MUL[]', 'multiply', 'MULtiply.'),
    Mnemonic(C.ABS, 0x64, [], 0, [FX], [FX], None, 'ABS[]', 'ABS[]', 'absolute', 'ABSolute value.'),
    Mnemonic(C.NEG, 0x65, [], 0, [FX], [FX], None, 'NEG[]', 'NEG[]', 'negate', 'NEGate value.'),
    Mnemonic(C.FLOOR, 0x66, [], 0, [FX], [FX], None, 'FLOOR[]', 'FLOOR[]', 'floor', 'FLOOR.'),
    Mnemonic(C.CEILING, 0x67, [], 0, [FX], [FX], None, 'CEILING[]', 'CEILING[]', 'ceiling', 'CEILING.'),
    Mnemonic(C.MAX, 0x8B, [], 0, [FX]*2, [FX], None, 'MAX[]', 'MAX[]', 'maximum', 'MAXimum of top two stack elements.'),
    Mnemonic(C.MIN, 0x8C, [], 0, [FX]*2, [FX], None, 'MIN[]', 'MIN[]', 'minimum', 'MINimum of top two stack elements.'),

    # Compensating for machine characteristics
    Mnemonic(C.ROUND_gray, 0x68, [0], 0, [V_], [V_], None, 'ROUND[Gr]', 'ROUND[00]', 'round value gray', 'ROUND value gray.'),
    Mnemonic(C.ROUND_black, 0x69, [1], 0, [V_], [V_], None, 'ROUND[Bl]', 'ROUND[01]', 'round value black', 'ROUND value black.'),
    Mnemonic(C.ROUND_white, 0x6A, [2], 0, [V_], [V_], None, 'ROUND[Wh]', 'ROUND[10]', 'round value white', 'ROUND value white.'),

    # What does the 4th code 0x6B do?
    Mnemonic(C.NROUND_gray, 0x6C, [0], 0, [V_], [V_], None, 'NROUND[Gr]', 'NROUND[00]', 'nround value gray', 'NROUND value gray.'),
    Mnemonic(C.NROUND_black, 0x6D, [1], 0, [V_], [V_], None, 'NROUND[Bl]', 'NROUND[01]', 'nround value black', 'NROUND value black.'),
    Mnemonic(C.NROUND_white, 0x6E, [2], 0, [V_], [V_], None, 'NROUND[Wh]', 'NROUND[10]', 'nround value white', 'NROUND value white.'),
    # What does the 4th code 0x6F do?

    # Defining and using functions and instructions
    Mnemonic(C.FDEF, 0x2C, [], 0, [V_], [], None, 'FDEF[]', 'FDEF[]', 'function', 'Functions DEFinition.'),
    Mnemonic(C.ENDF, 0x2D, [], 0, [], [], None, 'ENDF[]', 'ENDF[]', 'end function', 'END function DEFinition.'),
    Mnemonic(C.CALL, 0x2B, [], 0, [V_], [], None, 'CALL[]', 'CALL[]', 'call function', 'CALL function.'),
    Mnemonic(C.LOOPCALL, 0x2A, [], 0, [V_]*2, [], None, 'LOOPCALL[]', 'LOOPCALL[]', 'loop call', 'LOOP and CALL function.'),
    Mnemonic(C.IDEF, 0x89, [], 0, [UL], [], None, 'IDEF[]', 'IDEF[]', 'instruction definition', 'Instruction DEFinition.'),
    Mnemonic(C.DEBUG, 0x4F, [], 0, [UL], [], None, 'DEBUG[]', 'DEBUG[]', 'debug', 'DEBUG Call.'),
    Mnemonic(C.GETINFO, 0x88, [], 0, [V_], [V_], None, 'GETINFO[]', 'GETINFO[]', 'get info', 'GET INFOrmation.'),

    # Unknown Mnemonic
    Mnemonic(C.UNKNOWN, 1000, [], 0, [], [], None, 'UNKNOWN', 'UNKNOWN', 'error', '###ERROR Unknown instruction.'),
    Mnemonic(C.EMPTY, 1001, [], 0, [], [], None, 'EMPTY', 'EMPTY', 'pass', 'Empty pass. Instruction does do nothing.'),

    # VTT Talk
    Mnemonic(C.VTT_BEGIN, 2000, [], 0, [], [], None, '#BEGIN', None, 'vtt begin block', 'VTT Talk, Begin block.'),
    Mnemonic(C.VTT_END, 2001, [], 0, [], [], None, '#END', None, 'vtt end block', 'VTT Talk, End block.'),
    Mnemonic(C.VTT_PUSH, 2002, [], 0, [], [], 'vttpush', '#PUSH', None, 'vtt push', 'VTT Talk, Push.'),
    Mnemonic(C.VTT_PUSHON, 2003, [], 0, [], [], None, '#PUSHON', None, 'vtt pushon', 'VTT Talk, Push on.'),
    Mnemonic(C.VTT_PUSHOFF, 2004, [], 0, [], [], None, '#PUSHOFF', None, 'vtt pushoff', 'VTT Talk, Push off.'),

    # RoboHint instructions
    Mnemonic('show_stack', 3000, [], 0, [], [], 'showStack', None, None, 'show stack', 'show stack.'),
    Mnemonic('show_storage', 3001, [], 0, [], [], 'showStorage',None, None, 'show storage', 'show storage.'),

    # V T T functions to add
    # AL    ALIGN            Align points
    # AS    ASM                Add plain instructions
    # DS    DSTROKE            Control diagonal strokes
    # F        FIXDSTROKES        Touch the untouched points in a diagonal stroke
    # G        GRABHEREINX        Control the left and right sidebearing of small sizes
    # H        HEIGHT
    # IN    INTERSECT
    # IS    ISTROKE
    # M        MAINSTROKEANGLE
    # Q        QUIT            (Quit VTT)
    # SC    SCOOP
    # SE    SERIF
    #        SETITALICSTROKEANGLE
    #        SETITALICSTROKEPHASE
    # SM    SMOOTH
    # ST    STROKE
    #         VACUFORMLIMIT
    #        VACUFORMROUND
    # XA    XANCHOR
    # XDE    XDELTA
    # XDI    XDISTANCE
    # XDOU    XDOUBLEGRID
    # XDOW    XDOWNTOGRID
    # XH    XHALFGRID
    # XIN    XINTERPOLATE
    # XIP    XIPANCHOR
    # XL    XLINK
    # XM    XMOVE
    # XR    XROUND
    # XSH    XSHIFT
    # XST    XTROKE
    # XU    XUPTOGRID
    # YA    YANCHOR
    # YDE    YDELTA
    # YDI    YDIST
    # YDOU    YDOUBLEGRID
    # YDOW    YDOWNTOGRID
    # YH    YHALFGRID
    # YIN    YINTERPOLATE
    # TIP    YIPANCHOR
    # YL    YLINK
    # YM    YMOVE
    # YR    YROUND
    # YSH    YSHIFT
    # YST    YSTROKE
    # YU    YUPTOGRID
    )

    INSTRUCTIONS = {}
    CODES = {}
    FREENAMES = {}
    VTTSYNTAX = {}     # Key is the VTT mnemonic syntax
    BASESYNTAX = {}    # Key is the fonttools mnemonic syntax
    NPARAMS = {} # Collect instructions that have an "n" list as params
    HINTSEARCH = {}
    NAMEPARTS = {} # Storage of mnemonic name parts for faster lookup of sugguestions while typing
    FREEWORDINDEX = {} # Word index for free word mnemonic searc, depending on the descriptions

    for mnemonic in MNEMONICS:
        INSTRUCTIONS[mnemonic.id] = mnemonic
        CODES[mnemonic.code] = mnemonic
        VTTSYNTAX[mnemonic.vtt] = mnemonic
        BASESYNTAX[mnemonic.base] = mnemonic
        FREENAMES[mnemonic.freeName] = mnemonic

        # Select all mnemonics that need a length indicator in their params list.
        if mnemonic.popTypes is None:
            NPARAMS[mnemonic.base] = mnemonic

        if mnemonic.base is not None:
            '''
            Split the mnemonic into search parts, so the editor can recognize
            them, while the user doesn't have to type the complete and exact
            :mnemonic.

            @@@ This may have become obsolete, with the definition of NAMEPARTS
            '''
            s = ''
            for c in mnemonic.base:
                    if c.lower() in C.MNEMONICNAMECHARS:
                            s += c
                    else:
                            s += ' '
            HINTSEARCH[s.strip()] = mnemonic

        '''
        Build the free search index with name keys This is for identical
        matching of free names.
        '''
        if mnemonic.freeName is not None:
            wordsKey = TX.string2WordsKey(mnemonic.freeName)
            assert not wordsKey in FREEWORDINDEX, wordsKey
            FREEWORDINDEX[wordsKey] = mnemonic

        # Build suggested mnemonic name parts for faster lookup
        # This is to quickly find alternative matches.
        if mnemonic.freeName:
            for namepart in mnemonic.freeName.split(' '):
                if not namepart:
                    continue

                if not namepart in NAMEPARTS:
                    NAMEPARTS[namepart] = set()

                NAMEPARTS[namepart].add(mnemonic)

    @classmethod
    def vttpush(cls, base, params):
        params = [str(param) for param in params]

        if len(params) == 1:
            return 'PUSHB[] %s' % params[0]
        else:
            return 'NPUSHB[] %s %s' % (len(params), ' '.join(params))

    @classmethod
    def push(cls, params):
        """
        One single intelligen push call, that generates the
        pushes for all parameters.
        Rules:
        - Preferred to use the PUSHB
        - If there is a negative number, then that must be PUSHW
        - If the type changes, output the current set first
        - If the list is larger than 8, use NPUSH
        Answer the result as string with newlines and ending with a newline
        """
        output = []
        last = []
        stack = [last]

        for param in params:
            if not last:
                # Starting new, just add
                last.append(param)
            elif param < 0 or param > 255: # Must be a word
                if last[0] < 0 or last[0] > 255:
                    # It is a word and it was a word, just add
                    last.append(param)
                else: # Changed type, make new list
                    last = [param]
                    stack.append(last)
            else: # Must be a byte
                if 0 <= last[0] <= 255:
                    # It is a byte and it was a byte, just add
                    last.append(param)
                else: # Changed type, make a new list
                    last = [param]
                    stack.append(last)

        for types in stack:
            output.append(cls._push(types))

        return '\n'.join(output) + '\n'

    @classmethod
    def _push(cls, params):
        # Ignore pushed with no values.
        if not params:
            return ''

        # Negative  or large number goes into a word
        if params[0] < 0 or params[0] > 255:
            params = [str(param) for param in params]

            if len(params) <= 8:
                s = 'PUSHW[%s] %s' % (cls.NUM2BIT[len(params)-1], ' '.join(params))
            else:
                # TTX doesn't want the first parameter to be the length of params
                s = 'NPUSHW[] %s' % ' '.join(params)
        else:
            # Positive number goes into a byte
            params = [str(param) for param in params]

            if len(params) <= 8:
                s = 'PUSHB[%s] %s' % (cls.NUM2BIT[len(params)-1], ' '.join(params))
            else: # TTX doesn't want the first parameter to be the length of params
                s = 'NPUSHB[] %s' % ' '.join(params)

        return s

    """
    @classmethod
    def npushb(cls, base, params):
            params = [str(param) for param in params]
            return 'NPUSHB[] %s %s' % (len(params), ' '.join(params))

    push = npushb

    @classmethod
    def npushw(cls, base, params):
            params = [str(param) for param in params]
            return 'NPUSHW[] %s %s' % (len(params), ' '.join(params))

    @classmethod
    def pushb(cls, base, params):
            params = [str(param) for param in params]
            return 'PUSHB[%d] %s' % (len(params), ' '.join(params))

    @classmethod
    def pushw(cls, base, params):
            params = [str(param) for param in params]
            return 'PUSHW[%d] %s' % (len(params), ' '.join(params))

    @classmethod
    def push(cls, base, params):
            params = [str(param) for param in params]
            return 'PUSH %s' % ' '.join(params)
    """
    @classmethod
    def getMnemonic(cls, name, paramcount=1):
        """
        Answer the mnemonic by name, which can be either vtt, id or base mnemonic.
        """
        if not name:
            return None

        # Strip all white space from the token, since it can be between name and [ or inside parameters
        name = TX.removeWhiteSpace(name)
        # Convert name into a cap name, without damaging the parameters
        try:
            name = TX.mnemonicName2Upper(name)
        except Exception as e:
            print(traceback.format_exc())
            print(e, name)

        '''
        Check if the push need special treatment It no paramcount now, the
        parameters probably will be set later by the calling application, so for now
        just answer the generic PUSHB and PUSHW (wrongly attached to respectively
        PUSHB_1 and PUSHW_1 hex code, but TTX will sort it out and otherwise the
        application needs to add the params later anyway. Name lookup is
        dynamic in the winget.mnemonic, so it will automatically change the name upon
        retrieval.
        '''
        if name.startswith('PUSHB['):
            if not paramcount:
                name = 'PUSHB[]'
            else:
                name = 'PUSHB[%d]' % paramcount
        elif name.startswith('PUSHW['):
            if not paramcount:
                name = 'PUSHW[]'
            else:
                name = 'PUSHW[%d]' % paramcount

        # Try to recognize the right mnemonic syntax
        return cls.INSTRUCTIONS.get(name) or cls.BASESYNTAX.get(name) or cls.VTTSYNTAX.get(name)

    @classmethod
    def isMnemonic(cls, name, paramcount=1):
        return cls.getMnemonic(name, paramcount) is not None

    @classmethod
    def getInstruction(cls, mnemonic, params):
        # Take Mnemonic instance or name
        if isinstance(mnemonic, str):
            mnemonic = cls.getMnemonic(mnemonic, len(params))

        if mnemonic is None:
            return None

        instruction = []

        if params and not params == ['']:
            if mnemonic.method is not None:
                # There is a function definition here, instead of a fixed name
                if hasattr(cls, mnemonic.method):
                    instruction.append(getattr(cls, mnemonic.method)(mnemonic.base, params))
            elif mnemonic.base: # Is there an output token for base?
                pushb_mnemonic = cls.getMnemonic('PUSHB[]', len(params))
                instruction.append(pushb_mnemonic.base + ' ' + TX.list2SpacedString(params))
                instruction.append(mnemonic.base)
        elif mnemonic.base: # Is there an output token for base?
            instruction.append(mnemonic.base)
        return '\n'.join(instruction)

    # D E B U G G I N G .

    @classmethod
    def showStack(cls, base, params):
        pass

    @classmethod
    def showStorage(cls, base, params):
        pass

