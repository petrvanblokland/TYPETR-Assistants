# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
#     Copyright (c) 2023+ TYPETR
#     Usage by MIT License
# ..............................................................................

from copy import deepcopy

if __name__ == '__main__': # Used for doc tests to find assistantLib
    import os, sys
    PATH = '/'.join(__file__.split('/')[:-4]) # Relative path to this respository that holds AssistantLib
    if not PATH in sys.path:
        sys.path.append(PATH)

from assistantLib.assistantParts.glyphsets.glyphData import * #GD, TOP, TOP_, _BOTTOM, BOTTOM_ etc.

GREEK_SET_NAME = 'Greek'
GREEK_SET_NAME_ITALIC = 'Greek Italic'

# The "c" attributes are redundant, if the @uni or @hex are defined, but they offer easy searching in the source by char.

TONOS_LEFT = 'quotesingle' # Copy tonos glyphs leftmargin from here.

GREEK_SET = {

   'Alpha': GD(name='Alpha', uni=0x0391, hex='0391', c='Α', l='A', r='A', base='A', anchors=['bottom', 'topleft', 'top'], gid=535),
   'Alphatonos': GD(name='Alphatonos', uni=0x0386, hex='0386', c='Ά', l='A', r='A', anchorTopX='A', base='A', accents=['tonoscmb.uc'], anchors=['bottom', 'top'], gid=526),
   #'Archaicsampi': GD(name='Archaicsampi', uni=0x0372, hex='0372', c='Ͳ', l='T', r='T', srcName='T', gid=512),
   'Beta': GD(name='Beta', uni=0x0392, hex='0392', c='Β', l='H', r='B', base='B', anchors=['bottom', 'top'], gid=536),
   'Chi': GD(name='Chi', uni=0x03A7, hex='03A7', c='Χ', l='X', r='X', base='X', anchors=['bottom', 'top'], gid=556),
   #'Dei_coptic': GD(name='Dei_coptic', uni=0x03EE, hex='03EE', c='Ϯ', l='Bhook', l2r='Bhook', base='I', gid=627),
   'Delta': GD(name='Delta', uni=0x0394, hex='0394', c='Δ', l='off', l2r='Delta', gid=538, comment='∆ symmetric difference'),
   #'Digamma': GD(name='Digamma', uni=0x03DC, hex='03DC', c='Ϝ', r='F', base='F', gid=609),
   'Epsilon': GD(name='Epsilon', uni=0x0395, hex='0395', c='Ε', l='E', r='E', base='E', anchors=['bottom', 'topleft', 'top'], gid=539),
   'Epsilontonos': GD(name='Epsilontonos', uni=0x0388, hex='0388', c='Έ', l=TONOS_LEFT, r='E', anchorTopX='E', base='E', accents=['tonoscmb.uc'], anchors=['bottom', 'top'], gid=528),
   'Eta': GD(name='Eta', uni=0x0397, hex='0397', c='Η', l='H', r='H', base='H', anchors=['bottom', 'topleft', 'top'], gid=541),
   'Etatonos': GD(name='Etatonos', uni=0x0389, hex='0389', c='Ή', l=TONOS_LEFT, r='H', anchorTopX='H', base='H', accents=['tonoscmb.uc'], anchors=['bottom', 'top'], gid=529),
   #'Fei_coptic': GD(name='Fei_coptic', uni=0x03E4, hex='03E4', c='Ϥ', l='o', r='H', gid=617),
   'Gamma': GD(name='Gamma', uni=0x0393, hex='0393', c='Γ', l='L', r='L', srcName='L', anchors=['bottom', 'top'], gid=537),
   #'Gangia_coptic': GD(name='Gangia_coptic', uni=0x03EA, hex='03EA', c='Ϫ', l='Delta', r='Delta', gid=623),
   #'Heta': GD(name='Heta', uni=0x0370, hex='0370', c='Ͱ', r='hyphen', gid=510),
   #'Hori_coptic': GD(name='Hori_coptic', uni=0x03E8, hex='03E8', c='Ϩ', l='S', r='S', gid=621),
   'Iota': GD(name='Iota', uni=0x0399, hex='0399', c='Ι', l='I', r='I', base='I', anchors=['bottom', 'topleft', 'top'], gid=543),
   'Iotadieresis': GD(name='Iotadieresis', uni=0x03AA, hex='03AA', c='Ϊ', l='Idieresis', w='I', base='I', accents=['dieresiscmb.uc'], anchors=['bottom', 'top'], gid=559),
   'Iotatonos': GD(name='Iotatonos', uni=0x038A, hex='038A', c='Ί', l=TONOS_LEFT, r='I', anchorTopX='I', base='I', accents=['tonoscmb.uc'], anchors=['bottom', 'top'], gid=530),
   'Iotadieresistonos.sc': GD(name='Iotadieresistonos.sc', l='Idieresis.sc', r='Idieresis.sc', base='Iota.sc', accents=['dieresistonoscmb'], isLower=True,),
   'KaiSymbol': GD(name='KaiSymbol', uni=0x03CF, hex='03CF', c='Ϗ', l='H', r='K', srcName='K', gid=596),
   'Kappa': GD(name='Kappa', uni=0x039A, hex='039A', c='Κ', l='H', r='K', base='K', anchors=['bottom', 'top'], gid=544),
   #'Khei_coptic': GD(name='Khei_coptic', uni=0x03E6, hex='03E6', c='Ϧ', l='off', r='n', gid=619),
   #'Koppa': GD(name='Koppa', uni=0x03DE, hex='03DE', c='Ϟ', l='off', l2r='Koppa', gid=611),
   #'KoppaArchaic': GD(name='KoppaArchaic', uni=0x03D8, hex='03D8', c='Ϙ', l='O', r='O', gid=605),
   'Lambda': GD(name='Lambda', uni=0x039B, hex='039B', c='Λ', l='A', r='A', gid=545, comment='Λ', anchors=['bottom', 'top']),
   'Mu': GD(name='Mu', uni=0x039C, hex='039C', c='Μ', l='H', r='H', base='M', anchors=['bottom', 'top'], gid=546),
   'Nu': GD(name='Nu', uni=0x039D, hex='039D', c='Ν', l='H', r='N', base='N', anchors=['bottom', 'top'], gid=547),
   'Omega': GD(name='Omega', uni=0x03A9, hex='03A9', c='Ω', l='off', l2r='self', anchors=['bottom', 'topleft', 'top'], gid=558),
   'Omegatonos': GD(name='Omegatonos', uni=0x038F, hex='038F', c='Ώ', l=TONOS_LEFT, r='Omega', anchorTopX='Omega', base='Omega', accents=['tonoscmb.uc'], anchors=['bottom', 'top'], gid=533),
   'Omicron': GD(name='Omicron', uni=0x039F, hex='039F', c='Ο', l='O', r='O', base='O', anchors=['bottom', 'topleft', 'top'], gid=549),
   'Omicrontonos': GD(name='Omicrontonos', uni=0x038C, hex='038C', c='Ό', l=TONOS_LEFT, r='O', anchorTopX='O', base='O', accents=['tonoscmb.uc'], anchors=['bottom', 'top'], gid=531),
   #'Pamphyliandigamma': GD(name='Pamphyliandigamma', uni=0x0376, hex='0376', c='Ͷ', base='Ii-cy', anchors=['top'], gid=516),
   'Phi': GD(name='Phi', uni=0x03A6, hex='03A6', l='O', r='O', c='Φ',anchors=['bottom', 'top'], gid=555),
   'Pi': GD(name='Pi', uni=0x03A0, hex='03A0', c='Π', l='H', r='H', srcName='H', anchors=['bottom', 'top'], gid=550),
   'Psi': GD(name='Psi', uni=0x03A8, hex='03A8', c='Ψ', l='U', r='U', srcName='U', anchors=['bottom', 'top'], gid=557),
   'Rho': GD(name='Rho', uni=0x03A1, hex='03A1', c='Ρ', l='H', r='P', base='P', anchors=['bottom', 'middle', 'top'], gid=551),
   #'Sampi': GD(name='Sampi', uni=0x03E0, hex='03E0', c='Ϡ', r='O', r2l='C', gid=613),
   #'San': GD(name='San', uni=0x03FA, hex='03FA', c='Ϻ', base='M', l='M', r='M', gid=639),
   #'Shei_coptic': GD(name='Shei_coptic', uni=0x03E2, hex='03E2', c='Ϣ', l='H', r='H', gid=615),
   #'Shima_coptic': GD(name='Shima_coptic', uni=0x03EC, hex='03EC', c='Ϭ', l='O', r='o', gid=625),
   #'Sho': GD(name='Sho', uni=0x03F7, hex='03F7', c='Ϸ', base='Thorn', gid=636),
   'Sigma': GD(name='Sigma', uni=0x03A3, hex='03A3', c='Σ', l='summation', r='summation', anchors=['bottom', 'top'], gid=552),
   #'SigmaLunateDottedReversedSymbol': GD(name='SigmaLunateDottedReversedSymbol', uni=0x03FF, hex='03FF', c='Ͽ', l2r='SigmaLunateDottedSymbol', r2l='SigmaLunateDottedSymbol', base='SigmaLunateReversedSymbol', accents=['dotmiddlecmb'], gid=644),
   #'SigmaLunateDottedSymbol': GD(name='SigmaLunateDottedSymbol', uni=0x03FE, hex='03FE', c='Ͼ', l='C', r='C', base='C', accents=['dotmiddlecmb'], anchors=['bottom', 'middle', 'top'], gid=643),
   #'SigmaLunateReversedSymbol': GD(name='SigmaLunateReversedSymbol', uni=0x03FD, hex='03FD', c='Ͻ', l2r='C', r2l='C', anchors=['dot'], gid=642),
   #'SigmaLunateSymbol': GD(name='SigmaLunateSymbol', uni=0x03F9, hex='03F9', c='Ϲ', l='C', r='C', gid=638),
   #'Stigma': GD(name='Stigma', uni=0x03DA, hex='03DA', c='Ϛ', l='C', r='C', gid=607),
   'Tau': GD(name='Tau', uni=0x03A4, hex='03A4', c='Τ', l='T', r='T', base='T', anchors=['bottom', 'top'], gid=553),
   'Theta': GD(name='Theta', uni=0x0398, hex='0398', c='Θ', l='O', r='O', srcName='O', anchors=['bottom', 'top'], gid=542),
   #'ThetaSymbol': GD(name='ThetaSymbol', uni=0x03F4, hex='03F4', c='ϴ', l='O', r='O', base='Obarred-cy', anchors=['top'], gid=633),
   'Upsilon': GD(name='Upsilon', uni=0x03A5, hex='03A5', c='Υ', l='Y', r='Y', base='Y', anchors=['bottom', 'topleft', 'top'], gid=554),
   #'UpsilonacutehookSymbol': GD(name='UpsilonacutehookSymbol', uni=0x03D3, hex='03D3', c='ϓ', l='Y', r='r', base='UpsilonhookSymbol', accents=['tonoscmb.uc'], anchors=['top'], gid=600),
   'Upsilondieresis': GD(name='Upsilondieresis', uni=0x03AB, hex='03AB', c='Ϋ', l='Upsilon', r='Upsilon', base='Y', accents=['dieresiscmb.uc'], anchors=['bottom', 'top'], gid=560),
   # Tdieresis does exist as unicode. Capital T: U+0054 → T + Combining Diaeresis: U+0308 → ** ̈** = T̈
   # Included here as placeholder for smallcap [c2sc] conversion
   'Upsilondieresistonos': GD(name='Upsilondieresistonos', hex='03AB + 0301', c='Ϋ́', l='Upsilon', r='Upsilon', anchorTopX='Upsilon', base='Upsilon', accents=['dieresistonoscmb'], anchors=['bottom', 'middle', 'top'], comment='Ϋ́'),
   'Upsilondieresistonos.sc': GD(name='Upsilondieresistonos.sc', l='Upsilon.sc', r='Upsilon.sc', base='Upsilon.sc', accents=['dieresistonoscmb'], anchors=['bottom', 'top'], gid=560),
   #'UpsilondieresishookSymbol': GD(name='UpsilondieresishookSymbol', uni=0x03D4, hex='03D4', c='ϔ', l='Upsilon', r='Upsilon', base='UpsilonhookSymbol', accents=['dieresiscmb.uc'], anchors=['top'], gid=601),
   #'UpsilonhookSymbol': GD(name='UpsilonhookSymbol', uni=0x03D2, hex='03D2', c='ϒ', l='Upsilon', r='Upsilon', anchors=['tonos', 'top'], gid=599),
   'Upsilontonos': GD(name='Upsilontonos', uni=0x038E, hex='038E', c='Ύ', l=TONOS_LEFT, r='Y', anchorTopX='Y', base='Y', accents=['tonoscmb.uc'], anchors=['bottom', 'top'], gid=532),
   'Xi': GD(name='Xi', uni=0x039E, hex='039E', c='Ξ', r2l='E', r='E', gid=548),
   #'Yot': GD(name='Yot', uni=0x037F, hex='037F', c='Ϳ', l='J', r='J', base='J', anchors=['bottom', 'middle', 'top'], gid=523),
   'Zeta': GD(name='Zeta', uni=0x0396, hex='0396', c='Ζ', l='Z', r='Z', base='Z', anchors=['bottom', 'top'], gid=540),
   'alpha': GD(name='alpha', uni=0x03B1, hex='03B1', c='α', l='o', r='t', isLower=True, anchors=['bottom', 'top'], gid=566),
   'alphatonos': GD(name='alphatonos', uni=0x03AC, hex='03AC', c='ά', l='alpha', r='alpha', base='alpha', accents=['tonoscmb'], isLower=True, anchors=['bottom', 'top'], gid=561),
   'anoteleia': GD(name='anoteleia', uni=0x0387, hex='0387', c='·', l='period', r='period', isLower=True, gid=527),
   #'archaicsampi': GD(name='archaicsampi', uni=0x0373, hex='0373', c='ͳ', r='E', r2l='E', isLower=True, gid=513),
   'beta': GD(name='beta', uni=0x03B2, hex='03B2', c='β', isLower=True, r2l='j', r='o', anchors=['bottom', 'top'], anchorTopY='TopY', anchorTopX='TopX', gid=567),
   #'betaSymbol': GD(name='betaSymbol', uni=0x03D0, hex='03D0', c='ϐ', l='beta', r='beta', gid=597),
   'chi': GD(name='chi', uni=0x03C7, hex='03C7', c='χ', l='x', r='x', isLower=True, gid=588, anchors=['bottom', 'top'], comment='χ'),
   #'dei_coptic': GD(name='dei_coptic', uni=0x03EF, hex='03EF', c='ϯ', l='i', r='hyphen', isLower=True, gid=628),
   'delta': GD(name='delta', uni=0x03B4, hex='03B4', c='δ', l='o', r='o', isLower=True, anchors=['bottom', 'top'], gid=569),
   'dieresistonos': GD(name='dieresistonos', uni=0x0385, hex='0385', c='΅', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='dieresistonoscmb', isLower=True, anchors=[], gid=525),
   'dieresistonoscmb': GD(name='dieresistonoscmb', w=0, autoFixComponentPositions=False, autoFixMargins=False, anchors=['_top', 'top'], isLower=True),
   #'digamma': GD(name='digamma', uni=0x03DD, hex='03DD', c='ϝ', r='Fsmall', isLower=True, gid=610),
   'epsilon': GD(name='epsilon', uni=0x03B5, hex='03B5', c='ε', l='e', isLower=True, anchors=['bottom', 'top'], anchorTopY='TopY', anchorTopX='TopX', gid=570, comment='ε'),
   #'epsilonLunateReversedSymbol': GD(name='epsilonLunateReversedSymbol', uni=0x03F6, hex='03F6', c='϶', l2r='c', r2l='c', isLower=True, gid=635),
   #'epsilonLunateSymbol': GD(name='epsilonLunateSymbol', uni=0x03F5, hex='03F5', c='ϵ', l='c', r='c', isLower=True, gid=634),
   'epsilontonos': GD(name='epsilontonos', uni=0x03AD, hex='03AD', c='έ', l='epsilon', r='epsilon', base='epsilon', accents=['tonoscmb'], isLower=True, anchors=['top'], gid=562),
   'eta': GD(name='eta', uni=0x03B7, hex='03B7', c='η', l='off', r='jdotless', isLower=True, anchors=['bottom', 'top'], gid=572),
   'etatonos': GD(name='etatonos', uni=0x03AE, hex='03AE', c='ή', l='eta', r='eta', base='eta', accents=['tonoscmb'], isLower=True, anchors=['bottom', 'top'], gid=563),
   #'fei_coptic': GD(name='fei_coptic', uni=0x03E5, hex='03E5', c='ϥ', l='o', r='q', isLower=True, gid=618),
   'gamma': GD(name='gamma', uni=0x03B3, hex='03B3', c='γ', l='v', r='v', isLower=True, anchors=['bottom', 'top'], gid=568),
   #'gangia_coptic': GD(name='gangia_coptic', uni=0x03EB, hex='03EB', c='ϫ', l='Delta', r='Delta', isLower=True, gid=624),
   #'heta': GD(name='heta', uni=0x0371, hex='0371', c='ͱ', r='hyphen', isLower=True, gid=511),
   #'hori_coptic': GD(name='hori_coptic', uni=0x03E9, hex='03E9', c='ϩ', l2r='S', r2l='S', isLower=False, gid=622),
   'iota': GD(name='iota', uni=0x03B9, hex='03B9', c='ι', r2l='j', r='t', anchorTopX='off', isLower=True, anchors=['bottom', 'top'], gid=574, comment='ι'),
   'iotadieresis': GD(name='iotadieresis', uni=0x03CA, hex='03CA', c='ϊ', w='iota', bl='iota', base='iota', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=591),
   'iotadieresistonos': GD(name='iotadieresistonos', uni=0x0390, hex='0390', c='ΐ', w='iota', bl='iota', base='iota', accents=['dieresistonoscmb'], isLower=True, anchors=['top'], gid=534),
   'iotatonos': GD(name='iotatonos', uni=0x03AF, hex='03AF', c='ί', w='iota', bl='iota', base='iota', accents=['tonoscmb'], isLower=True, anchors=['top'], gid=564),
   'kaiSymbol': GD(name='kaiSymbol', uni=0x03D7, hex='03D7', c='ϗ', isLower=True, gid=604),
   'kappa': GD(name='kappa', uni=0x03BA, hex='03BA', c='κ', isLower=True, anchors=['bottom', 'top'], gid=575),
   #'kappaSymbol': GD(name='kappaSymbol', uni=0x03F0, hex='03F0', c='ϰ', l=100, isLower=True, gid=629),
   #'khei_coptic': GD(name='khei_coptic', uni=0x03E7, hex='03E7', c='ϧ', l=100, r='o', isLower=True, gid=620),
   #'koppa': GD(name='koppa', uni=0x03DF, hex='03DF', c='ϟ', l='100', r='100', isLower=True, gid=612),
   #'koppaArchaic': GD(name='koppaArchaic', uni=0x03D9, hex='03D9', c='ϙ', l='o', r='o', isLower=True, gid=606),
   'lambda': GD(name='lambda', uni=0x03BB, hex='03BB', c='λ', l='Delta', r='Delta', anchorTopX='TopX', isLower=True, anchors=['bottom', 'top'], gid=576),
   'lowernumeral_greek': GD(name='lowernumeral_greek', uni=0x0375, hex='0375', c='͵', l='minute', r='minute', base='minute', isLower=True, gid=515),
   'mu': GD(name='mu', uni=0x03BC, hex='03BC', c='μ', isLower=True, gid=577, anchors=['bottom', 'top'], anchorTopY='TopY', anchorTopX='TopX', comment='mu'),
   'nu': GD(name='nu', uni=0x03BD, hex='03BD', c='ν', isLower=True, anchors=['bottom', 'top'], gid=578),
   'numeral_greek': GD(name='numeral_greek', uni=0x0374, hex='0374', c='ʹ', l='minute', r='minute', base='minute', isLower=True, gid=514),
   'omega': GD(name='omega', uni=0x03C9, hex='03C9', c='ω', l='o', r='o', isLower=True, fixSpacing=False, anchors=['bottom', 'top'], gid=590, comment='ω'),
   'omegatonos': GD(name='omegatonos', uni=0x03CE, hex='03CE', c='ώ', l='omega', r='omega', base='omega', accents=['tonoscmb'], isLower=True, anchors=['bottom', 'top'], gid=595),
   'omicron': GD(name='omicron', uni=0x03BF, hex='03BF', c='ο', base='o', isLower=True, anchors=['bottom', 'top'], gid=580),
   'omicrontonos': GD(name='omicrontonos', uni=0x03CC, hex='03CC', c='ό', l='omicron', r='omicron', base='o', accents=['tonoscmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=593),
   #'pamphyliandigamma': GD(name='pamphyliandigamma', uni=0x0377, hex='0377', c='ͷ', base='ii-cy', isLower=True, anchors=['top'], gid=517),
   'phi': GD(name='phi', uni=0x03C6, hex='03C6', c='φ', r='o', l='o', isLower=True, anchors=['bottom', 'top'], gid=587),
   #'phiSymbol': GD(name='phiSymbol', uni=0x03D5, hex='03D5', c='ϕ', l='o', r='o', isLower=True, gid=602),
   'pi': GD(name='pi', uni=0x03C0, hex='03C0', c='π', isLower=True, anchors=['bottom', 'top'], gid=581),
   #'piSymbol': GD(name='piSymbol', uni=0x03D6, hex='03D6', c='ϖ', l='hyphen', l2r='piSymbol', isLower=True, gid=603),
   'psi': GD(name='psi', uni=0x03C8, hex='03C8', c='ψ', l='v', r='o', anchorTopX='TopX', anchorTopY='TopY', isLower=True, anchors=['bottom', 'top'], gid=589),
   'questiongreek': GD(name='questiongreek', uni=0x037E, hex='037E', c=';', l='semicolon', r='semicolon', base='semicolon', isLower=True, gid=522),
   'rho': GD(name='rho', uni=0x03C1, hex='03C1', c='ρ', l='beta', r='o', isLower=True, anchors=['bottom', 'top'], gid=582),
   #'rhoStrokeSymbol': GD(name='rhoStrokeSymbol', uni=0x03FC, hex='03FC', c='ϼ', r='o', bl='rho', base='rho', isLower=True, anchors=['top'], gid=641),
   #'rhoSymbol': GD(name='rhoSymbol', uni=0x03F1, hex='03F1', c='ϱ', l='rho', r='rho', isLower=True, gid=630),
   #'sampi': GD(name='sampi', uni=0x03E1, hex='03E1', c='ϡ', l='100', r='O', gid=614),
   #'san': GD(name='san', uni=0x03FB, hex='03FB', c='ϻ', l='Hsmall', r='Hsmall', isLower=True, gid=640),
   #'shei_coptic': GD(name='shei_coptic', uni=0x03E3, hex='03E3', c='ϣ', l2r='m', r2l='m', isLower=True, gid=616),
   #'shima_coptic': GD(name='shima_coptic', uni=0x03ED, hex='03ED', c='ϭ', l='O', r='o', gid=626),
   #'sho': GD(name='sho', uni=0x03F8, hex='03F8', c='ϸ', base='thorn', isLower=True, gid=637),
   'sigma': GD(name='sigma', uni=0x03C3, hex='03C3', c='σ', l='o', w='o', isLower=True, anchors=['bottom', 'top'], gid=584),
   #'sigmaLunateDottedReversedSymbol': GD(name='sigmaLunateDottedReversedSymbol', uni=0x037D, hex='037D', c='ͽ', l2r='sigmaLunateDottedSymbol', r2l='sigmaLunateDottedSymbol', base='oopen', accents=['dotmiddlecmb'], isLower=True, gid=521),
   #'sigmaLunateDottedSymbol': GD(name='sigmaLunateDottedSymbol', uni=0x037C, hex='037C', c='ͼ', l='c', r='c', base='c', accents=['dotmiddlecmb'], isLower=True, anchors=['bottom', 'middle', 'top'], gid=520),
   #'sigmaLunateReversedSymbol': GD(name='sigmaLunateReversedSymbol', uni=0x037B, hex='037B', c='ͻ', l2r='sigmaLunateDottedSymbol', r2l='sigmaLunateDottedSymbol', base='oopen', isLower=True, gid=519),
   #'sigmaLunateSymbol': GD(name='sigmaLunateSymbol', uni=0x03F2, hex='03F2', c='ϲ', l='c', r='c', base='c', isLower=True, anchors=['bottom', 'middle', 'top'], gid=631),
   'sigmafinal': GD(name='sigmafinal', uni=0x03C2, hex='03C2', c='ς', l='c', r='c', isLower=True, gid=583),
   'Sigmafinal.sc': GD(name='Sigmafinal.sc', base='Sigma.sc', l='Sigma', r='Sigma', isLower=True, gid=583),
   #'stigma': GD(name='stigma', uni=0x03DB, hex='03DB', c='ϛ', isLower=True, gid=608),
   'tau': GD(name='tau', uni=0x03C4, hex='03C4', c='τ', l='t', r='t', isLower=True, anchors=['bottom', 'top'], gid=585),
   'theta': GD(name='theta', uni=0x03B8, hex='03B8', c='θ', l='O', r='O', anchorTopX='TopX', anchorTopY='TopY', anchors=['bottom', 'top'], gid=573),
   #'thetaSymbol': GD(name='thetaSymbol', uni=0x03D1, hex='03D1', c='ϑ', l='hyphen', r='hyphen', gid=598),
   'tonos': GD(name='tonos', uni=0x0384, hex='0384', c='΄', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='tonoscmb', isLower=True, gid=524),
   'upsilon': GD(name='upsilon', uni=0x03C5, hex='03C5', c='υ', l='v', r='o', isLower=True, fixSpacing=False, anchors=['bottom', 'top'], gid=586),
   'upsilondieresis': GD(name='upsilondieresis', uni=0x03CB, hex='03CB', c='ϋ', l='upsilon', r='upsilon', base='upsilon', accents=['dieresiscmb'], isLower=True, anchors=['top'], gid=592),
   'upsilondieresistonos': GD(name='upsilondieresistonos', uni=0x03B0, hex='03B0', c='ΰ', l='upsilon', r='upsilon', base='upsilon', accents=['dieresistonoscmb'], isLower=True, anchors=['top'], gid=565),
   'upsilondieresistonos.sc': GD(name='upsilondieresistonos.sc', l='Ydieresis.sc', r='Ydieresis.sc', base='Ydieresis.sc', isLower=True, gid=565),
   'upsilontonos': GD(name='upsilontonos', uni=0x03CD, hex='03CD', c='ύ', l='upsilon', r='upsilon', base='upsilon', accents=['tonoscmb'], isLower=True, anchors=['top'], gid=594),
   'xi': GD(name='xi', uni=0x03BE, hex='03BE', c='ξ', anchorTopX='TopX', l='o', anchorBottomX='BottomX', anchorTopY='TopY', anchors=['bottom', 'top'], isLower=True, gid=579),
   #'yot': GD(name='yot', uni=0x03F3, hex='03F3', c='ϳ', l='j', r='j', base='j', isLower=True, anchors=['bottom', 'middle'], gid=632),
   #'ypogegrammeni': GD(name='ypogegrammeni', uni=0x037A, hex='037A', c='ͺ', w='0', base='ypogegrammenicmb', isLower=True, anchors=['bottom'], gid=518),
   'zeta': GD(name='zeta', uni=0x03B6, hex='03B6', c='ζ', l='o', isLower=True, anchors=['bottom', 'top'], gid=571),

   'tonos': GD(name='tonos', uni=0x0384, hex='0384', c='΄', l=GD.CAT_CENTER, w=GD.CAT_ACCENT_WIDTH, base='tonoscmb', anchors=[], isLower=True, gid=524),
   'tonoscmb': GD(name='tonoscmb', w=0, anchors=['_top'], srcName='gravecmb', autoFixComponentPositions=False, autoFixMargins=False, autoFixAnchorPositionY=False, isLower=True), # Lower case tonos just behaves as other diacritics
   'tonoscmb.uc': GD(name='tonoscmb.uc', w=0, srcName='acutecmb.uc', autoFixComponentPositions=False, autoFixMargins=False, autoFixAnchorPositionY=False, isLower=False, anchors=['_topleft'], gid=1709), # Capital tonos is right aligned on the tonos anchor.

}

GREEK_SET_ITALIC = deepcopy(GREEK_SET)

# Exceptions on the Greek italic set go here.
