# -*- coding: UTF-8 -*-
#
#    Assistant for RoboFont4
#    Belongs to Presti VF projects
#    Branche from Upgrade Sans Assistant 034
#
#    FontGoggles Sample for Presti
#    T~tlu1~mld2~bld4~brd3r~tru1y~tru1 P~blu3~bld2~brd3~tlu3~tld1r~blu1e~mld1s~tlu5t~bld4i~trd3~brd4
#

import sys
import os
import codecs
import vanilla
import merz
import weakref
import importlib
from random import choice
from copy import copy
from math import *
from AppKit import *

from mojo.events import extractNSEvent
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import AllFonts, OpenFont, RGlyph, RPoint
from mojo.subscriber import Subscriber, WindowController, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber

from fontTools.misc.transform import Transform

# Add paths to libs in sibling repositories
PATHS = ('../TYPETR-Assistants/',)
for path in PATHS:
    if not path in sys.path:
        print('@@@ Append to sys.path', path)
        sys.path.append(path)

import assistantLib
from assistantLib.toolbox.glyphAnalyzer import GlyphAnalyzer

importlib.reload(assistantLib.toolbox.glyphAnalyzer)
from assistantLib.toolbox.glyphAnalyzer import GlyphAnalyzer

GROUPGLYPH_COLOR = (0, 0, 0.6, 1)
GLYPHGLYPH_COLOR = (0, 0.4, 0, 1)

C = 0.5 # Off-curve factor. 0.64 for Bezier curves
T = 12 # Selection tolerance

NUM_DIMENSIONEER_ELEMENTS = 100 # Max number of layer elements in Dimensioneer
DIMENSIONEER_LABEL_SIZE = 14 # Point size of Dimensioneer measures

VERBOSE = False # Show calling of event methods
VERBOSE2 = False # Secudary functions start
VERBOSE3 = False # Mark which function did trigger change
VERBOSE4 = False # Very details inside functions

ARROW_KEYS = [NSUpArrowFunctionKey, NSDownArrowFunctionKey,
        NSLeftArrowFunctionKey, NSRightArrowFunctionKey, NSPageUpFunctionKey,
        NSPageDownFunctionKey, NSHomeFunctionKey, NSEndFunctionKey]
FUNCTION_KEYS = ('=', '+', 'y', 'h', 'H',
    'u', 'i', 'o', 'p', 'U', 'I', 'O', 'P', 
     'n', 'N', 'm', 'M', '.', ',', '<', '>', 
    '@', # Copy flourish from src.
)

# Connector types

# Receiving Latin connectors
cmR = set("""d.sans.cm0 d.sans.ct0  h.sans.cm0 h.sans.ct0  fi fl tbar oslashacute tcedilla f.salt_connect f.salt_noconnect d.sans hbar thorn ampersand a a.alt1 a.alt2 a.cm0 a.cm1 a.cm2 a.ct0 a.ct1 a.ct2 aacute abreve acircumflex adieresis ae aeacute agrave amacron aogonek aring aringacute atilde b b.alt1 b.alt2 b.ct0 b.ct1 b.ct2 b.cm0 b.cm1 b.cm2 b.sans b.sans.cm0 b.sans.ct0 c c.alt1 c.alt2 c.cm0 c.cm1 c.cm2 c.ct0 c.ct1 c.ct2 cacute ccaron ccedilla ccircumflex cdotaccent d d.alt1 d.alt2 d.cm0 d.cm1 d.cm2 d.ct0 d.ct1 d.ct2 dcaron dcroat e e.alt1 e.alt2 e.cm0 e.cm0b e.cm1 e.cm1b e.cm2 e.cm2b e.ct0 e.ct0b e.ct1 e.ct1b e.ct2 e.ct2b eacute ebreve ecaron ecircumflex edieresis edotaccent egrave emacron eogonek eth f f.alt1 f.alt2 f.cm0 f.cm1 f.cm2 f.ct0 f.ct1 f.ct2 g g.alt1 g.alt2 g.cm0 g.cm1 g.cm2 g.ct0 g.ct1 g.ct2 gbreve gcaron gcircumflex gcommaaccent gdotaccent h h.alt1 h.alt2 h.sans h.cm0 h.cm1 h.cm2 h.ct0 h.ct1 h.ct2 hcircumflex k k.alt1 k.alt2 k.sans k.sans.cm0 k.sans.ct0 k.cm0 k.cm1 k.cm2 k.ct0 k.ct1 k.ct2 kcommaaccent l l.alt1 l.alt2 l.sans l.sans.cm0 l.sans.ct0 l.cm0 l.cm1 l.cm2 l.ct0 l.ct1 l.ct2 lacute lcaron lcommaaccent ldot lacute.sans lcaron.sans lcommaaccent.sans ldot.sans o o.alt1 o.alt2 o.cm0 o.cm1 o.cm2 o.ct0 o.ct1 o.ct2 oe oacute obreve ocircumflex odieresis ograve ohungarumlaut omacron oslash otilde q q.alt1 q.alt2 q.cm0 q.cm1 q.cm2 q.ct0 q.ct1 q.ct2 t t.alt1 t.alt2 t.cm0 t.cm1 t.cm2 t.ct0 t.ct1 t.ct2 tcaron tcommaaccent""".split(' '))
ctR = set("""y yacute ydieresis ycircumflex ygrave y.ct0 y.ct1 y.ct2 y.cm0 y.cm1 y.cm2 y.alt1 y.alt2 p.cm0 p.cm1 p.cm2 p.ct0 p.ct1 p.ct2 zdotaccent germandbls eng itilde idotless idotless.alt1 idotless.alt2 idotless.cm0 idotless.cm1 idotless.cm2 idotless.ct0 idotless.ct1 idotless.ct2 i i.alt1 i.alt2 i.cm0 i.cm1 i.cm2 i.ct0 i.ct1 i.ct2 i.trk iacute ibreve icircumflex idieresis igrave ij imacron iogonek jdotless idotless.cm0 j j.alt1 j.alt2 jdotless.ct0 jcircumflex m m.alt1 m.alt2 m.cm0 m.cm1 m.cm2 m.ct0 m.ct1 m.ct2 n n.alt1 n.alt2 n.cm0 n.cm1 n.cm2 n.ct0 n.ct1 n.ct2 nacute ncaron ncommaaccent ntilde p p.alt1 p.alt2 r r.alt1 r.alt2 r.cm0 r.cm1 r.cm2 r.ct0 r.ct1 r.ct2 racute rcaron rcommaaccent u u.alt1 u.alt2 u.cm0 u.cm1 u.cm2 u.ct0 u.ct1 u.ct2 uacute ubreve ucircumflex udieresis ugrave uhungarumlaut umacron uogonek uring utilde v v.alt1 v.alt2 v.cm0 v.cm1 v.cm2 v.ct0 v.ct1 v.ct2 w w.alt1 w.alt2 w.cm0 w.cm1 w.cm2 w.ct0 w.ct1 w.ct2 wacute wcircumflex wdieresis wgrave x x.alt1 x.alt2 x.cm0 x.cm1 x.cm2 x.ct0 x.ct1 x.ct2 y y.alt1 y.alt2 y.ct0 y.ct1 y.ct2 yacute ycircumflex ydieresis ygrave z z.alt1 z.alt2 z.cm0 z.cm1 z.cm2 z.ct0 z.ct1 z.ct2 zacute zcaron zdotaccent]""".split(' '))
cmLatin1 = 'n.cm0' # Left
ctLatin1 = 'n.ct0'
cmConnectors = set("""A.cm0 A.cm1 A.cm2 B.cm0 B.cm1 B.cm2 C.cm0 C.cm1 C.cm2 D.cm0 D.cm1 D.cm2 E.cm0 E.cm1 E.cm2 G.cm0 G.cm1 G.cm2 H.cm0 H.cm1 H.cm2 I.cm0 I.cm1 I.cm2 J.cm0 J.cm1 J.cm2 J.base.cm0 K.cm0 K.cm1 K.cm2 L.cm0 L.cm1 L.cm2 M.cm0 M.cm1 M.cm2 # No N O.cm0 O.cm1 O.cm2 P.cm0 P.cm1 P.cm2 # No Q R.cm0 R.cm1 R.cm2 S.cm0 S.cm1 S.cm2 T.cm0 T.cm1 T.cm2 # No U # No V # No W X.cm0 X.cm1 X.cm2 Y.cm0 Y.cm1 Y.cm2 Z.cm0 Z.cm1 Z.cm2 a.cm0 a.cm1 a.cm2 b.cm0 b.cm1 b.cm2 b.sans.cm0 c.cm0 c.cm1 c.cm2 d.cm0 d.cm1 d.cm2 e.cm0 e.cm1 e.cm2 f.cm0 f.cm1 f.cm2 g.cm0 g.cm1 g.cm2 h.cm0 h.cm1 h.cm2 h.sans.cm0 i.cm0 i.cm1 i.cm2 idotless.cm0 idotless.cm1 idotless.cm2 j.cm0 j.cm1 j.cm2 jdotless.cm0 k.cm0 k.cm1 k.cm2 k.sans.cm0 l.cm0 l.cm1 l.cm2 l.sans.cm0 m.cm0 m.cm1 m.cm2 n.cm0 n.cm1 n.cm2 o.cm0 o.cm1 o.cm2 p.cm0 p.cm1 p.cm2 q.cm0 q.cm1 q.cm2 r.cm0 r.cm1 r.cm2 s.cm0 s.cm1 s.cm2 t.cm0 t.cm1 t.cm2 u.cm0 u.cm1 u.cm2 v.cm0 v.cm1 v.cm2 w.cm0 w.cm1 w.cm2 x.cm0 x.cm1 x.cm2 y.cm0 y.cm1 y.cm2 z.cm0 z.cm1 z.cm2""".split(' '))
ctConnectors = set("""A.ct0 A.ct1 A.ct2 B.ct0 B.ct1 B.ct2 C.ct0 C.ct1 C.ct2 D.ct0 D.ct1 D.ct2 E.ct0 E.ct1 E.ct2 G.ct0 G.ct1 G.ct2 H.ct0 H.ct1 H.ct2 I.ct0 I.ct1 I.ct2 J.ct0 J.ct1 J.ct2 J.base.ct0 K.ct0 K.ct1 K.ct2 L.ct0 L.ct1 L.ct2 M.ct0 M.ct1 M.ct2 O.ct0 O.ct1 O.ct2 P.ct0 P.ct1 P.ct2 R.ct0 R.ct1 R.ct2 S.ct0 S.ct1 S.ct2 T.ct0 T.ct1 T.ct2 X.ct0 X.ct1 X.ct2 Y.ct0 Y.ct1 Y.ct2 Z.ct0 Z.ct1 Z.ct2 a.ct0 a.ct1 a.ct2 b.ct0 b.ct1 b.ct2 b.sans.ct0 c.ct0 c.ct1 c.ct2 d.ct0 d.ct1 d.ct2 e.ct0 e.ct1 e.ct2 f.ct0 f.ct1 f.ct2 g.ct0 g.ct1 g.ct2 h.ct0 h.ct1 h.ct2 h.sans.ct0 i.ct0 i.ct1 i.ct2 idotless.ct0 idotless.ct1 idotless.ct2 j.ct0 j.ct1 j.ct2 jdotless.ct0 k.ct0 k.ct1 k.ct2 k.sans.ct0 l.ct0 l.ct1 l.ct2 l.sans.ct0 m.ct0 m.ct1 m.ct2 n.ct0 n.ct1 n.ct2 o.ct0 o.ct1 o.ct2 p.ct0 p.ct1 p.ct2 q.ct0 q.ct1 q.ct2 r.ct0 r.ct1 r.ct2 s.ct0 s.ct1 s.ct2 t.ct0 t.ct1 t.ct2 u.ct0 u.ct1 u.ct2 v.ct0 v.ct1 v.ct2 w.ct0 w.ct1 w.ct2 x.ct0 x.ct1 x.ct2 y.ct0 y.ct1 y.ct2 z.ct0 z.ct1 z.ct2""".split(' '))
cmLatin2 = 'o' # Right
ctLatin2 = 'n'
# Receiving Greek connectors
cmGreekR = set("""alpha alpha.alt1 alpha.alt2 alpha.cm0 alpha.cm1 alpha.cm2 alpha.ct0 alpha.ct1 alpha.ct2 alphatonos alphatonos.alt1 alphatonos.alt2 alphatonos.cm0 alphatonos.cm1 alphatonos.cm2 alphatonos.ct0 alphatonos.ct1 alphatonos.ct2 beta beta.alt1 beta.alt2 beta.cm0 beta.cm1 beta.cm2 beta.ct0 beta.ct1 beta.ct2 delta delta.alt1 delta.alt2 delta.cm0 delta.cm1 delta.cm2 delta.ct0 delta.ct1 delta.ct2 zeta zeta.alt1 zeta.alt2 zeta.cm0 zeta.cm1 zeta.cm2 zeta.ct0 zeta.ct1 zeta.ct2 theta theta.alt1 theta.alt2 theta.cm0 theta.cm1 theta.cm2 theta.ct0 theta.ct1 theta.ct2 xi xi.alt1 xi.alt2 xi.cm0 xi.cm1 xi.cm2 xi.ct0 xi.ct1 xi.ct2 omicron omicron.alt1 omicron.alt2 omicron.cm0 omicron.cm1 omicron.cm2 omicron.ct0 omicron.ct1 omicron.ct2 omicrontonos omicrontonos.alt1 omicrontonos.alt2 omicrontonos.cm0 omicrontonos.cm1 omicrontonos.cm2 omicrontonos.ct0 omicrontonos.ct1 omicrontonos.ct2 rho rho.alt1 rho.alt2 rho.cm0 rho.cm1 rho.cm2 rho.ct0 rho.ct1 rho.ct2 sigma sigma.alt1 sigma.alt2 sigma.cm0 sigma.cm1 sigma.cm2 sigma.ct0 sigma.ct1 sigma.ct2 sigma1 sigma1.alt1 sigma1.alt2 phi phi.alt1 phi.alt2""".split(' '))
ctGreekR = set("""gamma gamma.alt1 gamma.alt2 gamma.cm0 gamma.cm1 gamma.cm2 gamma.ct0 gamma.ct1 gamma.ct2 eta eta.alt1 eta.alt2 eta.cm0 eta.cm1 eta.cm2 eta.ct0 eta.ct1 eta.ct2 etatonos etatonos.alt1 etatonos.alt2 etatonos.cm0 etatonos.cm1 etatonos.cm2 etatonos.ct0 etatonos.ct1 etatonos.ct2 iota iota.alt1 iota.alt2 iota.cm0 iota.cm1 iota.cm2 iota.ct0 iota.ct1 iota.ct2 iotadieresistonos iotadieresistonos.alt1 iotadieresistonos.alt2 iotadieresistonos.cm0 iotadieresistonos.cm1 iotadieresistonos.cm2 iotadieresistonos.ct0 iotadieresistonos.ct1 iotadieresistonos.ct2 iotatonos iotatonos.alt1 iotatonos.alt2 iotatonos.cm0 iotatonos.cm1 iotatonos.cm2 iotatonos.ct0 iotatonos.ct1 iotatonos.ct2 iotadieresis iotadieresis.alt1 iotadieresis.alt2 iotadieresis.cm0 iotadieresis.cm1 iotadieresis.cm2 iotadieresis.ct0 iotadieresis.ct1 iotadieresis.ct2 kappa kappa.alt1 kappa.alt2 kappa.cm0 kappa.cm1 kappa.cm2 kappa.ct0 kappa.ct1 kappa.ct2 mu mu.alt1 mu.alt2 mu.cm0 mu.cm1 mu.cm2 mu.ct0 mu.ct1 mu.ct2 nu nu.alt1 nu.alt2 nu.cm0 nu.cm1 nu.cm2 nu.ct0 nu.ct1 nu.ct2 pi pi.alt1 pi.alt2 pi.cm0 pi.cm1 pi.cm2 pi.ct0 pi.ct1 pi.ct2 tau tau.alt1 tau.alt2 tau.cm0 tau.cm1 tau.cm2 tau.ct0 tau.ct1 tau.ct2 upsilon upsilon.alt1 upsilon.alt2 upsilon.ct0 upsilon.ct1 upsilon.ct2 upsilondieresistonos upsilondieresistonos.alt1 upsilondieresistonos.alt2 upsilondieresistonos.ct0 upsilondieresistonos.ct1 upsilondieresistonos.ct2 upsilondieresis upsilondieresis.alt1 upsilondieresis.alt2 upsilondieresis.ct0 upsilondieresis.ct1 upsilondieresis.ct2 upsilontonos upsilontonos.alt1 upsilontonos.alt2 upsilontonos.ct0 upsilontonos.ct1 upsilontonos.ct2 chi chi.alt1 chi.alt2 chi.cm0 chi.cm1 chi.cm2 chi.ct0 chi.ct1 chi.ct2 psi psi.alt1 psi.alt2 psi.cm0 psi.cm1 psi.cm2 psi.ct0 psi.ct1 psi.ct2 omega omega.alt1 omega.alt2 omega.cm0 omega.cm1 omega.cm2 omega.ct0 omega.ct1 omega.ct2 omegatonos omegatonos.alt1 omegatonos.alt2 omegatonos.cm0 omegatonos.cm1 omegatonos.cm2 omegatonos.ct0 omegatonos.ct1 omegatonos.ct2""".split(' '))
cmGreek1 = 'eta.cm0' # Left
ctGreek1 = 'eta.ct0'
cmGreekConnectors = set("""Alpha.cm0 Alpha.cm1 Alpha.cm2 Alpha.cm0 Alpha.cm1 Alpha.cm2 Alphatonos.cm0 Alphatonos.cm1 Alphatonos.cm2 Alphatonos.cm0 Alphatonos.cm1 Alphatonos.cm2 Beta.cm0 Beta.cm1 Beta.cm2 Beta.cm0 Beta.cm1 Beta.cm2 Delta.cm0 Delta.cm1 Delta.cm2 Delta.cm0 Delta.cm1 Delta.cm2 Epsilon.cm0 Epsilon.cm1 Epsilon.cm2 Epsilon.cm0 Epsilon.cm1 Epsilon.cm2 Epsilontonos.cm0 Epsilontonos.cm1 Epsilontonos.cm2 Epsilontonos.cm0 Epsilontonos.cm1 Epsilontonos.cm2 Zeta.cm0 Zeta.cm1 Zeta.cm2 Zeta.cm0 Zeta.cm1 Zeta.cm2 Eta.cm0 Eta.cm1 Eta.cm2 Eta.cm0 Eta.cm1 Eta.cm2 Etatonos.cm0 Etatonos.cm1 Etatonos.cm2 Etatonos.cm0 Etatonos.cm1 Etatonos.cm2 Theta.cm0 Theta.cm1 Theta.cm2 Theta.cm0 Theta.cm1 Theta.cm2 Iota.cm0 Iota.cm1 Iota.cm2 Iota.cm0 Iota.cm1 Iota.cm2 Iotatonos.cm0 Iotatonos.cm1 Iotatonos.cm2 Iotatonos.cm0 Iotatonos.cm1 Iotatonos.cm2 Iotadieresis.cm0 Iotadieresis.cm1 Iotadieresis.cm2 Iotadieresis.cm0 Iotadieresis.cm1 Iotadieresis.cm2 Kappa.cm0 Kappa.cm1 Kappa.cm2 Kappa.cm0 Kappa.cm1 Kappa.cm2 Lambda.cm0 Lambda.cm1 Lambda.cm2 Lambda.cm0 Lambda.cm1 Lambda.cm2 Mu.cm0 Mu.cm1 Mu.cm2 Nu.cm0 Nu.cm1 Nu.cm2 Tau.cm0 Tau.cm1 Tau.cm2 Xi.cm0 Xi.cm1 Xi.cm2 Xi.cm0 Xi.cm1 Xi.cm2 Omicron.cm0 Omicron.cm1 Omicron.cm2 Omicron.cm0 Omicron.cm1 Omicron.cm2 Omicrontonos.cm0 Omicrontonos.cm1 Omicrontonos.cm2 Omicrontonos.cm0 Omicrontonos.cm1 Omicrontonos.cm2 Pi.cm0 Pi.cm1 Pi.cm2 Pi.cm0 Pi.cm1 Pi.cm2 Rho.cm0 Rho.cm1 Rho.cm2 Rho.cm0 Rho.cm1 Rho.cm2 Sigma.cm0 Sigma.cm1 Sigma.cm2 Sigma.cm0 Sigma.cm1 Sigma.cm2 Chi.cm0 Chi.cm1 Chi.cm2 Chi.cm0 Chi.cm1 Chi.cm2 Psi.cm0 Psi.cm1 Psi.cm2 Psi.cm0 Psi.cm1 Psi.cm2 Omega.cm0 Omega.cm1 Omega.cm2 Omega.cm0 Omega.cm1 Omega.cm2 Omegatonos.cm0 Omegatonos.cm1 Omegatonos.cm2 Omegatonos.cm0 Omegatonos.cm1 Omegatonos.cm2 Upsilon.cm0 Upsilon.cm1 Upsilon.cm2 Upsilon.cm0 Upsilon.cm1 Upsilon.cm2 Upsilondieresis.cm0 Upsilondieresis.cm1 Upsilondieresis.cm2 Upsilondieresis.cm0 Upsilondieresis.cm1 Upsilondieresis.cm2 Upsilontonos.cm0 Upsilontonos.cm1 Upsilontonos.cm2 Upsilontonos.cm0 Upsilontonos.cm1 Upsilontonos.cm2  alpha.cm0 alpha.cm1 alpha.cm2 alpha.cm0 alpha.cm1 alpha.cm2 alphatonos.cm0 alphatonos.cm1 alphatonos.cm2 alphatonos.cm0 alphatonos.cm1 alphatonos.cm2 beta.cm0 beta.cm1 beta.cm2 beta.cm0 beta.cm1 beta.cm2 gamma.cm0 gamma.cm1 gamma.cm2 gamma.cm0 gamma.cm1 gamma.cm2 delta.cm0 delta.cm1 delta.cm2 delta.cm0 delta.cm1 delta.cm2 epsilon.cm0 epsilon.cm1 epsilon.cm2 epsilon.cm0 epsilon.cm1 epsilon.cm2 epsilontonos.cm0 epsilontonos.cm1 epsilontonos.cm2 epsilontonos.cm0 epsilontonos.cm1 epsilontonos.cm2 zeta.cm0 zeta.cm1 zeta.cm2 zeta.cm0 zeta.cm1 zeta.cm2 eta.cm0 eta.cm1 eta.cm2 eta.cm0 eta.cm1 eta.cm2 etatonos.cm0 etatonos.cm1 etatonos.cm2 etatonos.cm0 etatonos.cm1 etatonos.cm2 theta.cm0 theta.cm1 theta.cm2 theta.cm0 theta.cm1 theta.cm2 iota.cm0 iota.cm1 iota.cm2 iota.cm0 iota.cm1 iota.cm2 iotadieresistonos.cm0 iotadieresistonos.cm1 iotadieresistonos.cm2 iotadieresistonos.cm0 iotadieresistonos.cm1 iotadieresistonos.cm2 iotatonos.cm0 iotatonos.cm1 iotatonos.cm2 iotatonos.cm0 iotatonos.cm1 iotatonos.cm2 iotadieresis.cm0 iotadieresis.cm1 iotadieresis.cm2 iotadieresis.cm0 iotadieresis.cm1 iotadieresis.cm2 kappa.cm0 kappa.cm1 kappa.cm2 kappa.cm0 kappa.cm1 kappa.cm2 lambda.cm0 lambda.cm1 lambda.cm2 lambda.cm0 lambda.cm1 lambda.cm2 mu.cm0 mu.cm1 mu.cm2 mu.cm0 mu.cm1 mu.cm2 nu.cm0 nu.cm1 nu.cm2 nu.cm0 nu.cm1 nu.cm2 xi.cm0 xi.cm1 xi.cm2 xi.cm0 xi.cm1 xi.cm2 omicron.cm0 omicron.cm1 omicron.cm2 omicron.cm0 omicron.cm1 omicron.cm2 omicrontonos.cm0 omicrontonos.cm1 omicrontonos.cm2 omicrontonos.cm0 omicrontonos.cm1 omicrontonos.cm2 pi.cm0 pi.cm1 pi.cm2 pi.cm0 pi.cm1 pi.cm2 rho.cm0 rho.cm1 rho.cm2 rho.cm0 rho.cm1 rho.cm2 sigma.cm0 sigma.cm1 sigma.cm2 sigma.cm0 sigma.cm1 sigma.cm2 tau.cm0 tau.cm1 tau.cm2 tau.cm0 tau.cm1 tau.cm2   upsilon.cm0 upsilon.cm1 upsilon.cm2 upsilondieresistonos.cm0 upsilondieresistonos.cm1 upsilondieresistonos.cm2   upsilondieresis.cm0 upsilondieresis.cm1 upsilondieresis.cm2   upsilontonos.cm0 upsilontonos.cm1 upsilontonos.cm2 chi.cm0 chi.cm1 chi.cm2 chi.cm0 chi.cm1 chi.cm2 psi.cm0 psi.cm1 psi.cm2 psi.cm0 psi.cm1 psi.cm2 omega.cm0 omega.cm1 omega.cm2 omega.cm0 omega.cm1 omega.cm2 omegatonos.cm0 omegatonos.cm1 omegatonos.cm2 omegatonos.cm0 omegatonos.cm1 omegatonos.cm2""".split(' '))
ctGreekConnectors = set("""Alpha.ct0 Alpha.ct1 Alpha.ct2 Alpha.ct0 Alpha.ct1 Alpha.ct2 Alphatonos.ct0 Alphatonos.ct1 Alphatonos.ct2 Alphatonos.ct0 Alphatonos.ct1 Alphatonos.ct2 Beta.ct0 Beta.ct1 Beta.ct2 Beta.ct0 Beta.ct1 Beta.ct2 Delta.ct0 Delta.ct1 Delta.ct2 Delta.ct0 Delta.ct1 Delta.ct2 Epsilon.ct0 Epsilon.ct1 Epsilon.ct2 Epsilon.ct0 Epsilon.ct1 Epsilon.ct2 Epsilontonos.ct0 Epsilontonos.ct1 Epsilontonos.ct2 Epsilontonos.ct0 Epsilontonos.ct1 Epsilontonos.ct2 Zeta.ct0 Zeta.ct1 Zeta.ct2 Zeta.ct0 Zeta.ct1 Zeta.ct2 Eta.ct0 Eta.ct1 Eta.ct2 Eta.ct0 Eta.ct1 Eta.ct2 Etatonos.ct0 Etatonos.ct1 Etatonos.ct2 Etatonos.ct0 Etatonos.ct1 Etatonos.ct2 Theta.ct0 Theta.ct1 Theta.ct2 Theta.ct0 Theta.ct1 Theta.ct2 Iota.ct0 Iota.ct1 Iota.ct2 Iota.ct0 Iota.ct1 Iota.ct2 Iotatonos.ct0 Iotatonos.ct1 Iotatonos.ct2 Iotatonos.ct0 Iotatonos.ct1 Iotatonos.ct2 Iotadieresis.ct0 Iotadieresis.ct1 Iotadieresis.ct2 Iotadieresis.ct0 Iotadieresis.ct1 Iotadieresis.ct2 Kappa.ct0 Kappa.ct1 Kappa.ct2 Kappa.ct0 Kappa.ct1 Kappa.ct2 Lambda.ct0 Lambda.ct1 Lambda.ct2 Lambda.ct0 Lambda.ct1 Lambda.ct2 Mu.ct0 Mu.ct1 Mu.ct2 Nu.ct0 Nu.ct1 Nu.ct2 Tau.ct0 Tau.ct1 Tau.ct2 Xi.ct0 Xi.ct1 Xi.ct2 Xi.ct0 Xi.ct1 Xi.ct2 Omicron.ct0 Omicron.ct1 Omicron.ct2 Omicron.ct0 Omicron.ct1 Omicron.ct2 Omicrontonos.ct0 Omicrontonos.ct1 Omicrontonos.ct2 Omicrontonos.ct0 Omicrontonos.ct1 Omicrontonos.ct2 Pi.ct0 Pi.ct1 Pi.ct2 Pi.ct0 Pi.ct1 Pi.ct2 Rho.ct0 Rho.ct1 Rho.ct2 Rho.ct0 Rho.ct1 Rho.ct2 Sigma.ct0 Sigma.ct1 Sigma.ct2 Sigma.ct0 Sigma.ct1 Sigma.ct2 Chi.ct0 Chi.ct1 Chi.ct2 Chi.ct0 Chi.ct1 Chi.ct2 Psi.ct0 Psi.ct1 Psi.ct2 Psi.ct0 Psi.ct1 Psi.ct2 Omega.ct0 Omega.ct1 Omega.ct2 Omega.ct0 Omega.ct1 Omega.ct2 Omegatonos.ct0 Omegatonos.ct1 Omegatonos.ct2 Omegatonos.ct0 Omegatonos.ct1 Omegatonos.ct2 Upsilon.ct0 Upsilon.ct1 Upsilon.ct2 Upsilon.ct0 Upsilon.ct1 Upsilon.ct2 Upsilondieresis.ct0 Upsilondieresis.ct1 Upsilondieresis.ct2 Upsilondieresis.ct0 Upsilondieresis.ct1 Upsilondieresis.ct2 Upsilontonos.ct0 Upsilontonos.ct1 Upsilontonos.ct2 Upsilontonos.ct0 Upsilontonos.ct1 Upsilontonos.ct2  alpha.ct0 alpha.ct1 alpha.ct2 alpha.ct0 alpha.ct1 alpha.ct2 alphatonos.ct0 alphatonos.ct1 alphatonos.ct2 alphatonos.ct0 alphatonos.ct1 alphatonos.ct2 beta.ct0 beta.ct1 beta.ct2 beta.ct0 beta.ct1 beta.ct2 gamma.ct0 gamma.ct1 gamma.ct2 gamma.ct0 gamma.ct1 gamma.ct2 delta.ct0 delta.ct1 delta.ct2 delta.ct0 delta.ct1 delta.ct2 epsilon.ct0 epsilon.ct1 epsilon.ct2 epsilon.ct0 epsilon.ct1 epsilon.ct2 epsilontonos.ct0 epsilontonos.ct1 epsilontonos.ct2 epsilontonos.ct0 epsilontonos.ct1 epsilontonos.ct2 zeta.ct0 zeta.ct1 zeta.ct2 zeta.ct0 zeta.ct1 zeta.ct2 eta.ct0 eta.ct1 eta.ct2 eta.ct0 eta.ct1 eta.ct2 etatonos.ct0 etatonos.ct1 etatonos.ct2 etatonos.ct0 etatonos.ct1 etatonos.ct2 theta.ct0 theta.ct1 theta.ct2 theta.ct0 theta.ct1 theta.ct2 iota.ct0 iota.ct1 iota.ct2 iota.ct0 iota.ct1 iota.ct2 iotadieresistonos.ct0 iotadieresistonos.ct1 iotadieresistonos.ct2 iotadieresistonos.ct0 iotadieresistonos.ct1 iotadieresistonos.ct2 iotatonos.ct0 iotatonos.ct1 iotatonos.ct2 iotatonos.ct0 iotatonos.ct1 iotatonos.ct2 iotadieresis.ct0 iotadieresis.ct1 iotadieresis.ct2 iotadieresis.ct0 iotadieresis.ct1 iotadieresis.ct2 kappa.ct0 kappa.ct1 kappa.ct2 kappa.ct0 kappa.ct1 kappa.ct2 lambda.ct0 lambda.ct1 lambda.ct2 lambda.ct0 lambda.ct1 lambda.ct2 mu.ct0 mu.ct1 mu.ct2 mu.ct0 mu.ct1 mu.ct2 nu.ct0 nu.ct1 nu.ct2 nu.ct0 nu.ct1 nu.ct2 xi.ct0 xi.ct1 xi.ct2 xi.ct0 xi.ct1 xi.ct2 omicron.ct0 omicron.ct1 omicron.ct2 omicron.ct0 omicron.ct1 omicron.ct2 omicrontonos.ct0 omicrontonos.ct1 omicrontonos.ct2 omicrontonos.ct0 omicrontonos.ct1 omicrontonos.ct2 pi.ct0 pi.ct1 pi.ct2 pi.ct0 pi.ct1 pi.ct2 rho.ct0 rho.ct1 rho.ct2 rho.ct0 rho.ct1 rho.ct2 sigma.ct0 sigma.ct1 sigma.ct2 sigma.ct0 sigma.ct1 sigma.ct2 tau.ct0 tau.ct1 tau.ct2 tau.ct0 tau.ct1 tau.ct2   upsilon.ct0 upsilon.ct1 upsilon.ct2 upsilondieresistonos.ct0 upsilondieresistonos.ct1 upsilondieresistonos.ct2   upsilondieresis.ct0 upsilondieresis.ct1 upsilondieresis.ct2   upsilontonos.ct0 upsilontonos.ct1 upsilontonos.ct2 chi.ct0 chi.ct1 chi.ct2 chi.ct0 chi.ct1 chi.ct2 psi.ct0 psi.ct1 psi.ct2 psi.ct0 psi.ct1 psi.ct2 omega.ct0 omega.ct1 omega.ct2 omega.ct0 omega.ct1 omega.ct2 omegatonos.ct0 omegatonos.ct1 omegatonos.ct2 omegatonos.ct0 omegatonos.ct1 omegatonos.ct2""".split(' '))
cmGreek2 = 'omicron' # Right
ctGreek2 = 'eta'
# Receiving Cyrillic connectors
clCyrR = set("""elcyrillic elcyrillic.alt1 elcyrillic.alt2 elcyrillic.cl0 elcyrillic.cm0 elcyrillic.cm1 elcyrillic.cm2 elcyrillic.ct0 elcyrillic.ct1 elcyrillic.ct2 iacyrillic iacyrillic.alt1 iacyrillic.alt2 iacyrillic.cl0 iacyrillic.cm0 iacyrillic.cm1 iacyrillic.cm2 iacyrillic.ct0 iacyrillic.ct1 iacyrillic.ct2 ljecyrillic ljecyrillic.alt1 ljecyrillic.alt2 ljecyrillic.cl0 ljecyrillic.cm0 ljecyrillic.cm1 ljecyrillic.cm2 ljecyrillic.ct0 ljecyrillic.ct1 ljecyrillic.ct2 emcyrillic emcyrillic.alt1 emcyrillic.alt2 emcyrillic.cl0 emcyrillic.cm0 emcyrillic.cm1 emcyrillic.cm2 emcyrillic.ct0 emcyrillic.ct1 emcyrillic.ct2 gheupturncyrillic gheupturncyrillic.alt1 gheupturncyrillic.alt2 zhecyrillic zhecyrillic.alt1 zhecyrillic.alt2 zhecyrillic.cl0 zhecyrillic.cm0 zhecyrillic.cm1 zhecyrillic.cm2 zhecyrillic.ct0 zhecyrillic.ct1 zhecyrillic.ct2 zhedescendercyrillic zhedescendercyrillic.alt1 zhedescendercyrillic.alt2 zhedescendercyrillic.cl0 zhedescendercyrillic.cm0 zhedescendercyrillic.cm1 zhedescendercyrillic.cm2 zhedescendercyrillic.ct0 zhedescendercyrillic.ct1 zhedescendercyrillic.ct2""".split(' '))
cmCyrR = set("""acyrillic acyrillic.alt1 acyrillic.alt2 acyrillic.cl0 acyrillic.cm0 acyrillic.cm1 acyrillic.cm2 acyrillic.ct0 acyrillic.ct1 acyrillic.ct2 becyrillic becyrillic.alt1 becyrillic.alt2 becyrillic.cl0 becyrillic.cm0 becyrillic.cm1 becyrillic.cm2 becyrillic.ct0 becyrillic.ct1 becyrillic.ct2 decyrillic decyrillic.alt1 decyrillic.alt2 decyrillic.cl0 decyrillic.cm0 decyrillic.cm1 decyrillic.cm2 decyrillic.ct0 decyrillic.ct1 decyrillic.ct2 djecyrillic djecyrillic.alt1 djecyrillic.alt2 djecyrillic.cl0 djecyrillic.cm0 djecyrillic.cm1 djecyrillic.cm2 djecyrillic.ct0 djecyrillic.ct1 djecyrillic.ct2 ecyrillic ecyrillic.alt1 ecyrillic.alt2 ecyrillic.cl0 ecyrillic.cm0 ecyrillic.cm1 ecyrillic.cm2 ecyrillic.ct0 ecyrillic.ct1 ecyrillic.ct2 efcyrillic efcyrillic.alt1 efcyrillic.alt2 efcyrillic.cl0 efcyrillic.cm0 efcyrillic.cm1 efcyrillic.cm2 efcyrillic.ct0 efcyrillic.ct1 efcyrillic.ct2 escyrillic escyrillic.alt1 escyrillic.alt2 escyrillic.cl0 escyrillic.cm0 escyrillic.cm1 escyrillic.cm2 escyrillic.ct0 escyrillic.ct1 escyrillic.ct2 iecyrillic iecyrillic.alt1 iecyrillic.alt2 iecyrillic.cl0 iecyrillic.cm0 iecyrillic.cm1 iecyrillic.cm2 iecyrillic.ct0 iecyrillic.ct1 iecyrillic.ct2 iegravecyrillic iegravecyrillic.alt1 iegravecyrillic.alt2 iegravecyrillic.cl0 iegravecyrillic.cm0 iegravecyrillic.cm1 iegravecyrillic.cm2 iegravecyrillic.ct0 iegravecyrillic.ct1 iegravecyrillic.ct2 iocyrillic iocyrillic.alt1 iocyrillic.alt2 iocyrillic.cl0 iocyrillic.cm0 iocyrillic.cm1 iocyrillic.cm2 iocyrillic.ct0 iocyrillic.ct1 iocyrillic.ct2 ocyrillic ocyrillic.alt1 ocyrillic.alt2 ocyrillic.cl0 ocyrillic.cm0 ocyrillic.cm1 ocyrillic.cm2 ocyrillic.ct0 ocyrillic.ct1 ocyrillic.ct2 tshecyrillic tshecyrillic.alt1 tshecyrillic.alt2 tshecyrillic.cl0 tshecyrillic.cm0 tshecyrillic.cm1 tshecyrillic.cm2 tshecyrillic.ct0 tshecyrillic.ct1 tshecyrillic.ct2 vecyrillic vecyrillic.alt1 vecyrillic.alt2 vecyrillic.cl0 vecyrillic.cl0 vecyrillic.cm0 vecyrillic.cm1 vecyrillic.cm2 vecyrillic.ct0 vecyrillic.ct1 vecyrillic.ct2""".split(' '))
ctCyrR = set("""iucyrillic.ct2 checyrillic checyrillic.alt1 checyrillic.alt2 checyrillic.cl0 checyrillic.cm0 checyrillic.cm1 checyrillic.cm2 checyrillic.ct0 checyrillic.ct1 checyrillic.ct2 chedescendercyrillic chedescendercyrillic.alt1 chedescendercyrillic.alt2 chedescendercyrillic.cl0 chedescendercyrillic.cm0 chedescendercyrillic.cm1 chedescendercyrillic.cm2 chedescendercyrillic.ct0 chedescendercyrillic.ct1 chedescendercyrillic.ct2 dzhecyrillic dzhecyrillic.alt1 dzhecyrillic.alt2 dzhecyrillic.cl0 dzhecyrillic.cm0 dzhecyrillic.cm1 dzhecyrillic.cm2 dzhecyrillic.ct0 dzhecyrillic.ct1 dzhecyrillic.ct2 encyrillic encyrillic.alt1 encyrillic.alt2 encyrillic.cl0 encyrillic.cm0 encyrillic.cm1 encyrillic.cm2 encyrillic.ct0 encyrillic.ct1 encyrillic.ct2 ercyrillic ercyrillic.alt1 ercyrillic.alt2 ercyrillic.cl0 ercyrillic.cm0 ercyrillic.cm1 ercyrillic.cm2 ercyrillic.ct0 ercyrillic.ct1 ercyrillic.ct2 hardsigncyrillic hardsigncyrillic.alt1 hardsigncyrillic.alt2 hardsigncyrillic.cl0 hardsigncyrillic.cm0 hardsigncyrillic.cm1 hardsigncyrillic.cm2 hardsigncyrillic.ct0 hardsigncyrillic.ct1 hardsigncyrillic.ct2 icyrillic icyrillic.alt1 icyrillic.alt2 icyrillic.cl0 icyrillic.cm0 icyrillic.cm1 icyrillic.cm2 icyrillic.ct0 icyrillic.ct1 icyrillic.ct2 igravecyrillic igravecyrillic.alt1 igravecyrillic.alt2 igravecyrillic.cl0 igravecyrillic.cm0 igravecyrillic.cm1 igravecyrillic.cm2 igravecyrillic.ct0 igravecyrillic.ct1 igravecyrillic.ct2 iicyrillic iicyrillic.alt1 iicyrillic.alt2 iicyrillic.cl0 iicyrillic.cm0 iicyrillic.cm1 iicyrillic.cm2 iicyrillic.ct0 iicyrillic.ct1 iicyrillic.ct2 iishortcyrillic iishortcyrillic.alt1 iishortcyrillic.alt2 iishortcyrillic.cl0 iishortcyrillic.cm0 iishortcyrillic.cm1 iishortcyrillic.cm2 iishortcyrillic.ct0 iishortcyrillic.ct1 iishortcyrillic.ct2 iucyrillic iucyrillic.alt1 iucyrillic.alt2 iucyrillic.cl0 iucyrillic.cm0 iucyrillic.cm1 iucyrillic.cm2 iucyrillic.ct0 iucyrillic.ct1 iucyrillic.ct2 jecyrillic jecyrillic.alt1 jecyrillic.alt2 jecyrillic.cl0 jecyrillic.cm0 jecyrillic.cm1 jecyrillic.cm2 jecyrillic.ct0 jecyrillic.ct1 jecyrillic.ct2 kacyrillic kacyrillic.alt1 kacyrillic.alt2 kacyrillic.cl0 kacyrillic.cm0 kacyrillic.cm1 kacyrillic.cm2 kacyrillic.ct0 kacyrillic.ct1 kacyrillic.ct2 kadescendercyrillic kadescendercyrillic.alt1 kadescendercyrillic.alt2 kadescendercyrillic.cl0 kadescendercyrillic.cm0 kadescendercyrillic.cm1 kadescendercyrillic.cm2 kadescendercyrillic.ct0 kadescendercyrillic.ct1 kadescendercyrillic.ct2 kjecyrillic kjecyrillic.alt1 kjecyrillic.alt2 kjecyrillic.cl0 kjecyrillic.cm0 kjecyrillic.cm1 kjecyrillic.cm2 kjecyrillic.ct0 kjecyrillic.ct1 kjecyrillic.ct2 njecyrillic njecyrillic.alt1 njecyrillic.alt2 njecyrillic.cl0 njecyrillic.cm0 njecyrillic.cm1 njecyrillic.cm2 njecyrillic.ct0 njecyrillic.ct1 njecyrillic.ct2 pecyrillic pecyrillic.alt1 pecyrillic.alt2 pecyrillic.cl0 pecyrillic.cm0 pecyrillic.cm1 pecyrillic.cm2 pecyrillic.ct0 pecyrillic.ct1 pecyrillic.ct2 shacyrillic shacyrillic.alt1 shacyrillic.alt2 shacyrillic.cl0 shacyrillic.cm0 shacyrillic.cm1 shacyrillic.cm2 shacyrillic.ct0 shacyrillic.ct1 shacyrillic.ct2 shchacyrillic shchacyrillic.alt1 shchacyrillic.alt2 shchacyrillic.cl0 shchacyrillic.cm0 shchacyrillic.cm1 shchacyrillic.cm2 shchacyrillic.ct0 shchacyrillic.ct1 shchacyrillic.ct2 softsigncyrillic softsigncyrillic.alt1 softsigncyrillic.alt2 softsigncyrillic.cl0 softsigncyrillic.cm0 softsigncyrillic.cm1 softsigncyrillic.cm2 softsigncyrillic.ct0 softsigncyrillic.ct1 softsigncyrillic.ct2 tsecyrillic tsecyrillic.alt1 tsecyrillic.alt2 tsecyrillic.cl0 tsecyrillic.cm0 tsecyrillic.cm1 tsecyrillic.cm2 tsecyrillic.ct0 tsecyrillic.ct1 tsecyrillic.ct2 tecyrillic tecyrillic.alt1 tecyrillic.alt2 tecyrillic.cl0 tecyrillic.cm0 tecyrillic.cm1 tecyrillic.cm2 tecyrillic.ct0 tecyrillic.ct1 tecyrillic.ct2 tshecyrillic tshecyrillic.alt1 tshecyrillic.alt2 tshecyrillic.cl0 tshecyrillic.cm0 tshecyrillic.cm1 tshecyrillic.cm2 tshecyrillic.ct0 tshecyrillic.ct1 tshecyrillic.ct2 ucyrillic ucyrillic.alt1 ucyrillic.alt2 ucyrillic.cl0 ucyrillic.cm0 ucyrillic.cm1 ucyrillic.cm2 ucyrillic.ct0 ucyrillic.ct1 ucyrillic.ct2 ushortcyrillic ushortcyrillic.alt1 ushortcyrillic.alt2 ushortcyrillic.cl0 ushortcyrillic.cm0 ushortcyrillic.cm1 ushortcyrillic.cm2 ushortcyrillic.ct0 ushortcyrillic.ct1 ushortcyrillic.ct2 ustraightstrokecyrillic ustraightstrokecyrillic.alt1 ustraightstrokecyrillic.alt2 ustraightstrokecyrillic.cl0 ustraightstrokecyrillic.cm0 ustraightstrokecyrillic.cm1 ustraightstrokecyrillic.cm2 ustraightstrokecyrillic.ct0 ustraightstrokecyrillic.ct1 ustraightstrokecyrillic.ct2 yericyrillic yericyrillic.alt1 yericyrillic.alt2 yericyrillic.cl0 yericyrillic.cm0 yericyrillic.cm1 yericyrillic.cm2 yericyrillic.ct0 yericyrillic.ct1 yericyrillic.ct2 yicyrillic yicyrillic.alt1 yicyrillic.alt2 yicyrillic.cl0 yicyrillic.cm0 yicyrillic.cm1 yicyrillic.cm2 yicyrillic.ct0 yicyrillic.ct1 yicyrillic.ct2""".split(' '))
# Targets
clCyrillic1 = 'pecyrillic.cl0' # Leftxzz
cmCyrillic1 = 'pecyrillic.cm0'
ctCyrillic1 = 'pecyrillic.ct0'
# Cyrillic connectors
clCyrillicConnectors = set("""Acyrillic.cl0 Becyrillic.cl0 Checyrillic.cl0 Djecyrillic.cl0 Dzecyrillic.cl0 Ecyrillic.cl0 Efcyrillic.cl0 Elcyrillic.cl0 Emcyrillic.cl0 Encyrillic.cl0 Ereversedcyrillic.cl0 Escyrillic.cl0 Hardsigncyrillic.cl0 IAcyrillic.cl0 IEgravecyrillic.cl0 IUcyrillic.cl0 Icyrillic.cl0 Iecyrillic.cl0 Igravecyrillic.cl0 Iicyrillic.cl0 Iishortcyrillic.cl0 Iocyrillic.cl0 Jecyrillic.cl0 Kacyrillic.cl0 Khacyrillic.cl0 Kjecyrillic.cl0 Ljecyrillic.cl0 Njecyrillic.cl0 Ocyrillic.cl0 Pecyrillic.cl0 Softsigncyrillic.cl0 Tecyrillic.cl0 Tshecyrillic.cl0 Vecyrillic.cl0 Yericyrillic.cl0 Yicyrillic.cl0 Zecyrillic.cl0 Zhecyrillic.cl0 acyrillic.cl0 becyrillic.cl0 checyrillic.cl0 chedescendercyrillic.cl0 decyrillic.cl0 djecyrillic.cl0 dzecyrillic.cl0 dzhecyrillic.cl0 ecyrillic.cl0 efcyrillic.cl0 elcyrillic.cl0 emcyrillic.cl0 encyrillic.cl0 ercyrillic.cl0 ereversedcyrillic.cl0 escyrillic.cl0 gecyrillic.cl0 gjecyrillic.cl0 hadescendercyrillic.cl0 hardsigncyrillic.cl0 iacyrillic.cl0 icyrillic.cl0 iecyrillic.cl0 iegravecyrillic.cl0 igravecyrillic.cl0 iicyrillic.cl0 iishortcyrillic.cl0 iocyrillic.cl0 iucyrillic.cl0 jecyrillic.cl0 kacyrillic.cl0 kadescendercyrillic.cl0 khacyrillic.cl0 kjecyrillic.cl0 ljecyrillic.cl0 njecyrillic.cl0 ocyrillic.cl0 pecyrillic.cl0 shacyrillic.cl0 shchacyrillic.cl0 softsigncyrillic.cl0 tecyrillic.cl0 tsecyrillic.cl0 tshecyrillic.cl0 ucyrillic.cl0 ushortcyrillic.cl0 ustraightstrokecyrillic.cl0 vecyrillic.cl0 yericyrillic.cl0 yicyrillic.cl0 zecyrillic.cl0 zhecyrillic.cl0 zhedescendercyrillic.cl0""".split(' '))
cmCyrillicConnectors = set("""Acyrillic.cm0 Acyrillic.cm1 Acyrillic.cm2 Becyrillic.cm0 Becyrillic.cm1 Becyrillic.cm2 Checyrillic.cm0 Checyrillic.cm1 Checyrillic.cm2 Djecyrillic.cm0 Djecyrillic.cm1 Djecyrillic.cm2 Dzecyrillic.cm0 Dzecyrillic.cm1 Dzecyrillic.cm2 Ecyrillic.cm0 Ecyrillic.cm1 Ecyrillic.cm2 Efcyrillic.cm0 Efcyrillic.cm1 Efcyrillic.cm2 Elcyrillic.cm0 Elcyrillic.cm1 Elcyrillic.cm2 Emcyrillic.cm0 Emcyrillic.cm1 Emcyrillic.cm2 Encyrillic.cm0 Encyrillic.cm1 Encyrillic.cm2 Ercyrillic.cm0 Ercyrillic.cm1 Ercyrillic.cm2 Ereversedcyrillic.cm0 Ereversedcyrillic.cm1 Ereversedcyrillic.cm2 Escyrillic.cm0 Escyrillic.cm1 Escyrillic.cm2 Hardsigncyrillic.cm0 Hardsigncyrillic.cm1 Hardsigncyrillic.cm2 IAcyrillic.cm0 IAcyrillic.cm1 IAcyrillic.cm2 IEgravecyrillic.cm0 IEgravecyrillic.cm1 IEgravecyrillic.cm2 IUcyrillic.cm0 IUcyrillic.cm1 IUcyrillic.cm2 Icyrillic.cm0 Icyrillic.cm1 Icyrillic.cm2 Iecyrillic.cm0 Iecyrillic.cm1 Iecyrillic.cm2 Igravecyrillic.cm0 Igravecyrillic.cm1 Igravecyrillic.cm2 Iicyrillic.cm0 Iicyrillic.cm1 Iicyrillic.cm2 Iishortcyrillic.cm0 Iishortcyrillic.cm1 Iishortcyrillic.cm2 Iocyrillic.cm0 Iocyrillic.cm1 Iocyrillic.cm2 Jecyrillic.cm0 Jecyrillic.cm1 Jecyrillic.cm2 Kacyrillic.cm0 Kacyrillic.cm1 Kacyrillic.cm2 Khacyrillic.cm0 Khacyrillic.cm1 Khacyrillic.cm2 Kjecyrillic.cm0 Kjecyrillic.cm1 Kjecyrillic.cm2 Ljecyrillic.cm0 Ljecyrillic.cm1 Ljecyrillic.cm2 Njecyrillic.cm0 Njecyrillic.cm1 Njecyrillic.cm2 Ocyrillic.cm0 Ocyrillic.cm1 Ocyrillic.cm2 Pecyrillic.cm0 Pecyrillic.cm1 Pecyrillic.cm2 Softsigncyrillic.cm0 Softsigncyrillic.cm1 Softsigncyrillic.cm2 Tecyrillic.cm0 Tecyrillic.cm1 Tecyrillic.cm2 Tshecyrillic.cm0 Tshecyrillic.cm1 Tshecyrillic.cm2 Ucyrillic.cm0 Ucyrillic.cm1 Ucyrillic.cm2 Ushortcyrillic.cm0 Ushortcyrillic.cm1 Ushortcyrillic.cm2 Vecyrillic.cm0 Vecyrillic.cm1 Vecyrillic.cm2 Yericyrillic.cm0 Yericyrillic.cm1 Yericyrillic.cm2 Yicyrillic.cm0 Yicyrillic.cm1 Yicyrillic.cm2 Zecyrillic.cm0 Zecyrillic.cm1 Zecyrillic.cm2 Zhecyrillic.cm0 Zhecyrillic.cm1 Zhecyrillic.cm2 acyrillic.cm0 acyrillic.cm1 acyrillic.cm2 becyrillic.cm0 becyrillic.cm1 becyrillic.cm2 checyrillic.cm0 checyrillic.cm1 checyrillic.cm2 chedescendercyrillic.cm0 chedescendercyrillic.cm1 chedescendercyrillic.cm2 decyrillic.cm0 decyrillic.cm1 decyrillic.cm2 djecyrillic.cm0 djecyrillic.cm1 djecyrillic.cm2 dzecyrillic.cm0 dzecyrillic.cm1 dzecyrillic.cm2 dzhecyrillic.cm0 dzhecyrillic.cm1 dzhecyrillic.cm2 ecyrillic.cm0 ecyrillic.cm1 ecyrillic.cm2 efcyrillic.cm0 efcyrillic.cm1 efcyrillic.cm2 elcyrillic.cm0 elcyrillic.cm1 elcyrillic.cm2 emcyrillic.cm0 emcyrillic.cm1 emcyrillic.cm2 encyrillic.cm0 encyrillic.cm1 encyrillic.cm2 ercyrillic.cm0 ercyrillic.cm1 ercyrillic.cm2 ereversedcyrillic.cm0 ereversedcyrillic.cm1 ereversedcyrillic.cm2 escyrillic.cm0 escyrillic.cm1 escyrillic.cm2 gecyrillic.cm0 gecyrillic.cm1 gecyrillic.cm2 gjecyrillic.cm0 gjecyrillic.cm1 gjecyrillic.cm2 hadescendercyrillic.cm0 hadescendercyrillic.cm1 hadescendercyrillic.cm2 hardsigncyrillic.cm0 hardsigncyrillic.cm1 hardsigncyrillic.cm2 iacyrillic.cm0 iacyrillic.cm1 iacyrillic.cm2 icyrillic.cm0 icyrillic.cm1 icyrillic.cm2 iecyrillic.cm0 iecyrillic.cm1 iecyrillic.cm2 iegravecyrillic.cm0 iegravecyrillic.cm1 iegravecyrillic.cm2 igravecyrillic.cm0 igravecyrillic.cm1 igravecyrillic.cm2 iicyrillic.cm0 iicyrillic.cm1 iicyrillic.cm2 iishortcyrillic.cm0 iishortcyrillic.cm1 iishortcyrillic.cm2 iocyrillic.cm0 iocyrillic.cm1 iocyrillic.cm2 iucyrillic.cm0 iucyrillic.cm1 iucyrillic.cm2 jecyrillic.cm0 jecyrillic.cm1 jecyrillic.cm2 kacyrillic.cm0 kacyrillic.cm1 kacyrillic.cm2 kadescendercyrillic.cm0 kadescendercyrillic.cm1 kadescendercyrillic.cm2 khacyrillic.cm0 khacyrillic.cm1 khacyrillic.cm2 kjecyrillic.cm0 kjecyrillic.cm1 kjecyrillic.cm2 ljecyrillic.cm0 ljecyrillic.cm1 ljecyrillic.cm2 njecyrillic.cm0 njecyrillic.cm1 njecyrillic.cm2 ocyrillic.cm0 ocyrillic.cm1 ocyrillic.cm2 pecyrillic.cm0 pecyrillic.cm1 pecyrillic.cm2 shacyrillic.cm0 shacyrillic.cm1 shacyrillic.cm2 shchacyrillic.cm0 shchacyrillic.cm1 shchacyrillic.cm2 softsigncyrillic.cm0 softsigncyrillic.cm1 softsigncyrillic.cm2 tecyrillic.cm0 tecyrillic.cm1 tecyrillic.cm2 tsecyrillic.cm0 tsecyrillic.cm1 tsecyrillic.cm2 tshecyrillic.cm0 tshecyrillic.cm1 tshecyrillic.cm2 ucyrillic.cm0 ucyrillic.cm1 ucyrillic.cm2 ushortcyrillic.cm0 ushortcyrillic.cm1 ushortcyrillic.cm2 ustraightstrokecyrillic.cm0 ustraightstrokecyrillic.cm1 ustraightstrokecyrillic.cm2 vecyrillic.cm0 vecyrillic.cm1 vecyrillic.cm2 yericyrillic.cm0 yericyrillic.cm1 yericyrillic.cm2 yicyrillic.cm0 yicyrillic.cm1 yicyrillic.cm2 zecyrillic.cm0 zecyrillic.cm1 zecyrillic.cm2 zhecyrillic.cm0 zhecyrillic.cm1 zhecyrillic.cm2 zhedescendercyrillic.cm0 zhedescendercyrillic.cm1 zhedescendercyrillic.cm2""".split(' '))
ctCyrillicConnectors = set("""Acyrillic.ct0 Acyrillic.ct1 Acyrillic.ct2 Becyrillic.ct0 Becyrillic.ct1 Becyrillic.ct2 Checyrillic.ct0 Checyrillic.ct1 Checyrillic.ct2 Djecyrillic.ct0 Djecyrillic.ct1 Djecyrillic.ct2 Dzecyrillic.ct0 Dzecyrillic.ct1 Dzecyrillic.ct2 Ecyrillic.ct0 Ecyrillic.ct1 Ecyrillic.ct2 Efcyrillic.ct0 Efcyrillic.ct1 Efcyrillic.ct2 Elcyrillic.ct0 Elcyrillic.ct1 Elcyrillic.ct2 Emcyrillic.ct0 Emcyrillic.ct1 Emcyrillic.ct2 Encyrillic.ct0 Encyrillic.ct1 Encyrillic.ct2 Ercyrillic.ct0 Ercyrillic.ct1 Ercyrillic.ct2 Ereversedcyrillic.ct0 Ereversedcyrillic.ct1 Ereversedcyrillic.ct2 Escyrillic.ct0 Escyrillic.ct1 Escyrillic.ct2 Hardsigncyrillic.ct0 Hardsigncyrillic.ct1 Hardsigncyrillic.ct2 IAcyrillic.ct0 IAcyrillic.ct1 IAcyrillic.ct2 IEgravecyrillic.ct0 IEgravecyrillic.ct1 IEgravecyrillic.ct2 IUcyrillic.ct0 IUcyrillic.ct1 IUcyrillic.ct2 Icyrillic.ct0 Icyrillic.ct1 Icyrillic.ct2 Iecyrillic.ct0 Iecyrillic.ct1 Iecyrillic.ct2 Igravecyrillic.ct0 Igravecyrillic.ct1 Igravecyrillic.ct2 Iicyrillic.ct0 Iicyrillic.ct1 Iicyrillic.ct2 Iishortcyrillic.ct0 Iishortcyrillic.ct1 Iishortcyrillic.ct2 Iocyrillic.ct0 Iocyrillic.ct1 Iocyrillic.ct2 Jecyrillic.ct0 Jecyrillic.ct1 Jecyrillic.ct2 Kacyrillic.ct0 Kacyrillic.ct1 Kacyrillic.ct2 Khacyrillic.ct0 Khacyrillic.ct1 Khacyrillic.ct2 Kjecyrillic.ct0 Kjecyrillic.ct1 Kjecyrillic.ct2 Ljecyrillic.ct0 Ljecyrillic.ct1 Ljecyrillic.ct2 Njecyrillic.ct0 Njecyrillic.ct1 Njecyrillic.ct2 Ocyrillic.ct0 Ocyrillic.ct1 Ocyrillic.ct2 Pecyrillic.ct0 Pecyrillic.ct1 Pecyrillic.ct2 Softsigncyrillic.ct0 Softsigncyrillic.ct1 Softsigncyrillic.ct2 Tecyrillic.ct0 Tecyrillic.ct1 Tecyrillic.ct2 Tshecyrillic.ct0 Tshecyrillic.ct1 Tshecyrillic.ct2 Ucyrillic.ct0 Ucyrillic.ct1 Ucyrillic.ct2 Ushortcyrillic.ct0 Ushortcyrillic.ct1 Ushortcyrillic.ct2 Vecyrillic.ct0 Vecyrillic.ct1 Vecyrillic.ct2 Yericyrillic.ct0 Yericyrillic.ct1 Yericyrillic.ct2 Yicyrillic.ct0 Yicyrillic.ct1 Yicyrillic.ct2 Zecyrillic.ct0 Zecyrillic.ct1 Zecyrillic.ct2 Zhecyrillic.ct0 Zhecyrillic.ct1 Zhecyrillic.ct2 acyrillic.ct0 acyrillic.ct1 acyrillic.ct2 becyrillic.ct0 becyrillic.ct1 becyrillic.ct2 checyrillic.ct0 checyrillic.ct1 checyrillic.ct2 chedescendercyrillic.ct0 chedescendercyrillic.ct1 chedescendercyrillic.ct2 decyrillic.ct0 decyrillic.ct1 decyrillic.ct2 djecyrillic.ct0 djecyrillic.ct1 djecyrillic.ct2 dzecyrillic.ct0 dzecyrillic.ct1 dzecyrillic.ct2 dzhecyrillic.ct0 dzhecyrillic.ct1 dzhecyrillic.ct2 ecyrillic.ct0 ecyrillic.ct1 ecyrillic.ct2 efcyrillic.ct0 efcyrillic.ct1 efcyrillic.ct2 elcyrillic.ct0 elcyrillic.ct1 elcyrillic.ct2 emcyrillic.ct0 emcyrillic.ct1 emcyrillic.ct2 encyrillic.ct0 encyrillic.ct1 encyrillic.ct2 ercyrillic.ct0 ercyrillic.ct1 ercyrillic.ct2 ereversedcyrillic.ct0 ereversedcyrillic.ct1 ereversedcyrillic.ct2 escyrillic.ct0 escyrillic.ct1 escyrillic.ct2 gecyrillic.ct0 gecyrillic.ct1 gecyrillic.ct2 gjecyrillic.ct0 gjecyrillic.ct1 gjecyrillic.ct2 hadescendercyrillic.ct0 hadescendercyrillic.ct1 hadescendercyrillic.ct2 hardsigncyrillic.ct0 hardsigncyrillic.ct1 hardsigncyrillic.ct2 iacyrillic.ct0 iacyrillic.ct1 iacyrillic.ct2 icyrillic.ct0 icyrillic.ct1 icyrillic.ct2 iecyrillic.ct0 iecyrillic.ct1 iecyrillic.ct2 iegravecyrillic.ct0 iegravecyrillic.ct1 iegravecyrillic.ct2 igravecyrillic.ct0 igravecyrillic.ct1 igravecyrillic.ct2 iicyrillic.ct0 iicyrillic.ct1 iicyrillic.ct2 iishortcyrillic.ct0 iishortcyrillic.ct1 iishortcyrillic.ct2 iocyrillic.ct0 iocyrillic.ct1 iocyrillic.ct2 iucyrillic.ct0 iucyrillic.ct1 iucyrillic.ct2 jecyrillic.ct0 jecyrillic.ct1 jecyrillic.ct2 kacyrillic.ct0 kacyrillic.ct1 kacyrillic.ct2 kadescendercyrillic.ct0 kadescendercyrillic.ct1 kadescendercyrillic.ct2 khacyrillic.ct0 khacyrillic.ct1 khacyrillic.ct2 kjecyrillic.ct0 kjecyrillic.ct1 kjecyrillic.ct2 ljecyrillic.ct0 ljecyrillic.ct1 ljecyrillic.ct2 njecyrillic.ct0 njecyrillic.ct1 njecyrillic.ct2 ocyrillic.ct0 ocyrillic.ct1 ocyrillic.ct2 pecyrillic.ct0 pecyrillic.ct1 pecyrillic.ct2 shacyrillic.ct0 shacyrillic.ct1 shacyrillic.ct2 shchacyrillic.ct0 shchacyrillic.ct1 shchacyrillic.ct2 softsigncyrillic.ct0 softsigncyrillic.ct1 softsigncyrillic.ct2 tecyrillic.ct0 tecyrillic.ct1 tecyrillic.ct2 tsecyrillic.ct0 tsecyrillic.ct1 tsecyrillic.ct2 tshecyrillic.ct0 tshecyrillic.ct1 tshecyrillic.ct2 ucyrillic.ct0 ucyrillic.ct1 ucyrillic.ct2 ushortcyrillic.ct0 ushortcyrillic.ct1 ushortcyrillic.ct2 ustraightstrokecyrillic.ct0 ustraightstrokecyrillic.ct1 ustraightstrokecyrillic.ct2 vecyrillic.ct0 vecyrillic.ct1 vecyrillic.ct2 yericyrillic.ct0 yericyrillic.ct1 yericyrillic.ct2 yicyrillic.ct0 yicyrillic.ct1 yicyrillic.ct2 zecyrillic.ct0 zecyrillic.ct1 zecyrillic.ct2 zhecyrillic.ct0 zhecyrillic.ct1 zhecyrillic.ct2 zhedescendercyrillic.ct0 zhedescendercyrillic.ct1 zhedescendercyrillic.ct2""".split(' '))
clCyrillic2 = 'elcyrillic' # Right
cmCyrillic2 = 'ocyrillic' 
ctCyrillic2 = 'pecyrillic'

#mmm = []
#f = CurrentFont()
#for gName in clCyrillicConnectors:
#    if gName in f:
#        mmm.append(gName)
#print(' '.join(sorted(mmm)))
 
# ULCWORDS has list of words

W, H = 250, 250
M = 32
SPACE_MARKER_R = 16
POINT_MARKER_R = 6
FAR = 100000 # Put drawing stuff outside the window
KERN_LINE_LENGTH = 32 # Number of glyphs on kerning line
KERN_SCALE = 0.15 #0.2

NO_MARKER = (1, 1, 1, 1)
#VISITED_MARKER = (0, 0.5, 0.5, 0.5)
if __file__.startswith('/Users/petr/Desktop/TYPETR-git'):
    VISITED_MARKER = 40/255, 120/255, 255/255, 1 # "Final" marker Blue (for others)
    print('Using Petr color')
else:
    VISITED_MARKER = 92/255, 149/255, 190/255, 1 # "Final" marker (for Petr)
    print('Using Tilmann/Graeme color')

WindowClass = vanilla.Window
WindowClass = vanilla.FloatingWindow
        
assistant = None # Little cheat, to make the assistant available from the window

class ConnectorAssistant(Subscriber):

    debug = True
    
    controller = None
    
    #    B U I L D I N G
    
    def build(self):
        global assistant
        assistant = self

        self.isUpdating = False
        
        self.glyph2Group1 = {}
        self.glyph2Group2 = {}

        f = CurrentFont()
        assert f is not None
        for groupName, group in f.groups.items():
            if 'kern1' in groupName:
                for gName in group:
                    self.glyph2Group1[gName] = groupName
            elif 'kern2' in groupName:
                for gName in group:
                    self.glyph2Group2[gName] = groupName
                                
        glyphEditor = self.getGlyphEditor()
        
        assert glyphEditor is not None
        
        self.foregroundContainer = container = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.foreground",
            location="foreground",
            clear=True
        )
        
        self.backgroundContainer = glyphEditor.extensionContainer(
            identifier="com.roboFont.Assistant.background",
            location="background",
            clear=True
        )
        # Previewing current glyphs on left/right side.        
        self.previewGlyphLeft = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=(0, 0, 0, 0.6),
        )
        self.previewGlyph = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=(0, 0, 0, 0.6),
        )
        self.previewGlyphRight = container.appendPathSublayer(
            position=(FAR, 0),
            fillColor=(0, 0, 0, 0.6),
        )

        self.kerning1Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning1Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning1Value.setHorizontalAlignment('center')
        self.kerning2Value = self.backgroundContainer.appendTextLineSublayer(
            name="kerning2Value",
            position=(FAR, 0),
            text='xxx\nxxx',
            font='Courier',
            pointSize=32,
            fillColor=(1, 0, 0, 1),
        )
        self.kerning2Value.setHorizontalAlignment('center')
        
        #    E V E N T S
        
    def started(self):
        pass
            
    def destroy(self):
        pass
                                    
    def glyphEditorDidSetGlyph(self, info):
        #self.backgroundContainer.clearSublayers()
        #self.foregroundContainer.clearSublayers()
        g = info["glyph"]
        if g is None:
            return
        self.updatePreview(g)
        #self.glyphEditorGlyphDidChange(info)
        #self.glyphEditorGlyphDidChangeInfo(info)
        #self.glyphEditorGlyphDidChangeOutline(info)
        #self.glyphEditorGlyphDidChangeComponents(info)
        #self.glyphEditorGlyphDidChangeAnchors(info)
        #self.glyphEditorGlyphDidChangeGuidelines(info)
        #self.glyphEditorGlyphDidChangeImage(info)
        #self.glyphEditorGlyphDidChangeMetrics(info)
        #self.glyphEditorGlyphDidChangeContours(info)

    def glyphEditorDidKeyDown(self, info):
        g = info['glyph']
        if VERBOSE:
            print('--- glyphEditorDidKeyDown', g.name) 
                
        event = extractNSEvent(info['NSEvent'])
        characters = event['keyDown']
        #print(event.keys())
        #print(characters)
        
        commandDown = event['commandDown']
        shiftDown = event['shiftDown']
        controlDown = event['controlDown']
        optionDown = event['optionDown']
        self.capLock = event['capLockDown']

        changed = False
        updatePreview = False
        
        if characters in 'Gg':
            self.snapSelectionToNearestPoint(g)
            if VERBOSE3:
                print('+++ glyphEditorDidKeyDown/snapSelectionToNearestPoint', )
            changed = True

        #elif characters in 'Ff':
        #    if characters == 'F': # or not g.contours: # If contours, then capital-F to force this function
        #        self.fixGlyphAnchorsCallback()
        #    elif characters == 'f':
        #        print('... Copy anchors from base of /%s' % g.name)
        #        self.copyAnchorPositionsFromBase(g)
        #        #print('### Fix anchors only for clean composites or for with "F" for /%s' % glyph.name)
            
        #print('... Key down', info['locationInGlyph'], info['NSEvent'].characters)
        elif characters in 'Pp': # Increment right margin
            if shiftDown:
                self._adjustRightMargin(g, 5)
            else:
                self._adjustRightMargin(g, 1)
            changed = True            
            updatePreview = True
            
        elif characters in 'Oo': # Decrement right margin
            if shiftDown:
                self._adjustRightMargin(g, -5)
            else:
                self._adjustRightMargin(g, -1)
            changed = True            
            updatePreview = True
        
        elif characters in 'Ii': # Increment left margin
            if shiftDown:
                self._adjustLeftMargin(g, 5)
            else:
                self._adjustLeftMargin(g, 1)            
            changed = True            
            updatePreview = True
        
        elif characters in 'Uu': # Decrement left margin
            if shiftDown:
                self._adjustLeftMargin(g, -5)
            else:
                self._adjustLeftMargin(g, -1)            
            changed = True            
            updatePreview = True

        # Adjust kerning

        elif characters in 'bB': # Increment right kerning
            if shiftDown:
                self._adjustRightKerning(g, 5) # 20
            else:
                self._adjustRightKerning(g, 1) # 4           
            changed = True            
            updatePreview = True
        
        elif characters in 'nN': # Decrement right kerning
            if shiftDown:
                self._adjustRightKerning(g, -5) # 20
            else:
                self._adjustRightKerning(g, -1) # 4
            changed = True            
            updatePreview = True
        
        elif characters in 'cC': # Decrement left kerning
            if shiftDown:
                self._adjustLeftKerning(g, -5) # 20
            else:
                self._adjustLeftKerning(g, -1) # 4           
            changed = True            
            updatePreview = True
        
        elif characters in 'vV': # Increment left kerning
            if shiftDown:
                self._adjustLeftKerning(g, 5) # 20
            else:
                self._adjustLeftKerning(g, 1) # 4           
            changed = True            
            updatePreview = True
        
        if updatePreview:
            #print('Preview key down', g.name)
            self.updatePreview(g)
    
    def glyphEditorGlyphDidChange(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChange', g.name)

    def glyphEditorGlyphDidChangeInfo(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeInfo', g.name)
             
    def glyphEditorGlyphDidChangeOutline(self, info):
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeOutline', g.name)
        self.updatePreview(g)
            
    def glyphEditorGlyphDidChangeContours(self, info):
        """Event also calls glyphEditorGlyphDidChangeOutline"""
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeContours', g.name)        
             
    def glyphEditorGlyphDidChangeComponents(self, info):
        """Event also calls glyphEditorGlyphDidChangeOutline"""
        g = info['glyph']
        if g is None:
            return
        if VERBOSE:
            print('--- glyphEditorGlyphDidChangeComponents', g.name)
                      
    #    S P A C I N G
    
    def _adjustLeftMargin(self, g, value):
        if self.isUpdating:
            return
        f = g.font
        unit = 1
        #self.isUpdating = True
        g.angledLeftMargin = int(round(g.angledLeftMargin/unit) + value) * unit
        #self.isUpdating = False
                        
    def _adjustRightMargin(self, g, value):
        if self.isUpdating:
            return
        f = g.font
        unit = 1
        #self.isUpdating = True
        g.angledRightMargin = int(round(g.angledRightMargin/unit) + value) * unit
        #self.isUpdating = False

    def _adjustLeftKerning(self, g, value):
        """    
            3 = glyph<-->glyph # Not used
            2 = group<-->glyph
            1 = glyph<-->group
            0 or None = group<-->group
        """
        f = g.font
        unit = 4
        
        left, right = self.getLeftRightGlyphs(g)
        print('Kerning left', left, g.name, right, value)
        if left is not None:
            group1 = self.glyph2Group1.get(left)
            group2 = self.glyph2Group2.get(g.name)
            if group1 is not None and group2 is not None:
                k = f.kerning.get((group1, group2), 0)
                print('kerning left', group1, group2, k)
                k = int(round(k/unit))*unit + value * unit
                if k:
                    f.kerning[(group1, group2)] = k
                    print(f'... Set left kerning ({group1}, {group2}) to {k}')
                elif f.kerning.get((group1, group2)) is not None:
                    del f.kerning[(group1, group2)]
                    print(f'... Delete left kerning ({group1}, {group2}')
                                        
    def _adjustRightKerning(self, g, value):
        """    
            3 = glyph<-->glyph # Not used
            2 = group<-->glyph
            1 = glyph<-->group
            0 or None = group<-->group
        """
        f = g.font
        unit = 4
        left, right = self.getLeftRightGlyphs(g)
        print('Kerning right', left, g.name, right, value)
        if right is not None:
            group1 = self.glyph2Group1.get(g.name)
            group2 = self.glyph2Group2.get(right)
            print('XXXX', group1, group2)
            if group1 is not None and group2 is not None:
                k = f.kerning.get((group1, group2), 0)
                k = int(round(k/unit))*unit + value * unit
                if k:
                    f.kerning[(group1, group2)] = k
                    print(f'... Set right kerning ({group1}, {group2}) to {k}')
                elif f.kerning.get((group1, group2)) is not None:
                    del f.kerning[(group1, group2)]
                    print(f'... Delete right kerning ({group1}, {group2}')
                    
    def getLeftRightGlyphs(self, g):
        
        if g.name in cmR:
            left = cmLatin1
        elif g.name in ctR:
            left = ctLatin1
        elif g.name in cmGreekR:
            left = cmGreek1
        elif g.name in ctGreekR:
            left = ctGreek1
        elif g.name in clCyrR:
            left = clCyrillic1
        elif g.name in cmCyrR:
            left = cmCyrillic1
        elif g.name in ctCyrR:
            left = ctCyrillic1
        else:
            left = None
            
        if '.cm' in g.name and g.name in cmConnectors:
            right = cmLatin2
        elif '.ct' in g.name and g.name in ctConnectors:
            right = ctLatin2
        elif '.cm' in g.name and g.name in cmGreekConnectors:
            right = cmGreek2
        elif '.ct' in g.name and g.name in ctGreekConnectors:
            right = ctGreek2
        elif '.cl' in g.name and g.name in clCyrillicConnectors:
            right = clCyrillic2
        elif '.cm' in g.name and g.name in cmCyrillicConnectors:
            right = cmCyrillic2
        elif '.ct' in g.name and g.name in ctCyrillicConnectors:
            right = ctCyrillic2
        else:
            right = None
            
        return left, right

    def updatePreview(self, g):

        if self.controller is None: # In case no longer available
            return
                
        f = g.font

        y4 = -150 # Position of current kerning values

        k =  0
        left, right = self.getLeftRightGlyphs(g)
        print(left, right)
        if left is not None:
            leftG = f[left]  
            group1 = self.glyph2Group1.get(left)
            group2 = self.glyph2Group2.get(g.name)
            if group1 is not None and group2 is not None:
                k = f.kerning.get((group1, group2), 0)

            self.previewGlyphLeft.setPosition((-leftG.width - k, 0))
            self.previewGlyphLeft.setPath(leftG.getRepresentation("merz.CGPath"))
        else:
            self.previewGlyphLeft.setPosition((FAR, 0))

        if k < 0:
            self.kerning1Value.setFillColor((1, 0, 0, 1))
        elif k > 0:
            self.kerning1Value.setFillColor((0, 0.5, 0, 1))
        else:
            self.kerning1Value.setFillColor((0.6, 0.6, 0.6, 1))
        self.kerning1Value.setPosition((k/2, y4))
        self.kerning1Value.setText('%d' % k)
            
        self.previewGlyph.setPosition((0, 0))
        self.previewGlyph.setPath(g.getLayer('foreground').getRepresentation("merz.CGPath"))
         
        k =  0
        if right is not None:
            rightG = f[right]
            group1 = self.glyph2Group1.get(g.name)
            group2 = self.glyph2Group2.get(right)
            if group1 is not None and group2 is not None:
                k = f.kerning.get((group1, group2), 0)

            self.previewGlyphRight.setPosition((g.width + k, 0))
            self.previewGlyphRight.setPath(rightG.getRepresentation("merz.CGPath"))
        else:
            self.previewGlyphRight.setPosition((FAR, 0))

        if k < 0:
            self.kerning2Value.setFillColor((1, 0, 0, 1))
        elif k > 0:
            self.kerning2Value.setFillColor((0, 0.5, 0, 1))
        else:
            self.kerning2Value.setFillColor((0.6, 0.6, 0.6, 1))
        self.kerning2Value.setPosition((g.width + k/2, y4))
        self.kerning2Value.setText('%d' % k)
                            
    def setGlyphGuides(self, g):
        f = g.font
        md = getMasterData(f)
        if md is None:
            print('### No masterdata for', f.path)
            return
        gd = getGlyphData(f, g.name)
        if gd is None:
            print('### No glyphdata for', g.name)
            return
        g.clearGuidelines()
        overshoot = md.metrics[gd.overshoot] # Get the right kind of overshoot for thi glyph
        baseline = md.metrics[gd.baseline]
        height = md.metrics[gd.height] # Get the right type of height, specific or this glyph

        if 'exclam' in g.name or 'question' in g.name:
            overshoot = 8 # alternative overshoot here
        elif g.name in ('dollar', 'dollar.tab', 'dollar.alt1', 'dollar.alt1.tab', 'bitcoin', 'bitcoin.tab'):
            g.appendGuideline((-300, -112), 0, name='Bottom of bars (%d)' % -112)
            g.appendGuideline((-300, 770), 0, name='Top of bars (%d)' % 770)
                   
        #if g.name == 'i.sups':
        #    print(gd.asCode())
        #    print('asassa', overshoot, height, baseline)
        if baseline: # Don't show main baseline
            g.appendGuideline((-200, baseline), 0, name='Baseline (%d)' % baseline)
        g.appendGuideline((-300, baseline - overshoot), 0, name='Overshoot (%d/%d)' % (baseline - overshoot, overshoot))
        if height not in (f.info.xHeight, f.info.capHeight): #  Don't show main xHeight or capHeigh
            g.appendGuideline((-200, baseline + height), 0, name='xHeight (%d)' % (baseline + height))
        g.appendGuideline((-300, baseline + height + overshoot), 0, name='Overshoot (%d/%d)' % (baseline + height + overshoot, overshoot))
        g.appendGuideline((-300, baseline + int(round(height/2))), 0, name='Middle (%d)' % (baseline + int(round(height/2))))
        
        if 'cmb' in g.name:
            g.appendGuideline((-300, md.metrics[TOP_OF_BOTTOM_CMB]), 0, name='Top of bottom CMB (%d)' % md.metrics[TOP_OF_BOTTOM_CMB])
            g.appendGuideline((-300, md.metrics[BOTTOM_OF_TOP_CMB]), 0, name='Bottom of top CMB (%d)' % md.metrics[BOTTOM_OF_TOP_CMB])
            g.appendGuideline((-300, int(round(f.info.xHeight/2+overshoot/2))), 0, name='Middle+overshoot/2 CMB (%d)' % int(round(f.info.xHeight/2+overshoot/2)))
        if '.lc' in g.name or '.tab_lc' in g.name:
            g.appendGuideline((-300, md.metrics[LC_FIG_BOTTOM]), 0, name='Bottom lowercase figures (%d)' % md.metrics[LC_FIG_BOTTOM])
        elif '.sups' in g.name:
            g.appendGuideline((-300, md.metrics[SUPS_ASCENDER]), 0, name='SUPS Ascender (%d)' % md.metrics[SUPS_ASCENDER])
            g.appendGuideline((-300, md.metrics[SUPS_DESCENDER]), 0, name='SUPS Descender (%d)' % md.metrics[SUPS_DESCENDER])
        elif '.sinf' in g.name:
            g.appendGuideline((-300, md.metrics[SINF_ASCENDER]), 0, name='SINF Ascender (%d)' % md.metrics[SINF_ASCENDER])
            g.appendGuideline((-300, md.metrics[SINF_DESCENDER]), 0, name='SINF Descender (%d)' % md.metrics[SINF_DESCENDER])

class ConnectorAssistantController(WindowController):
        
    assistantGlyphEditorSubscriberClass = ConnectorAssistant
    
    NAME = 'Connector Assistant'

    def build(self):        

        y = M
        self.w = WindowClass((W, H), self.NAME, minSize=(W, H))
        self.w.open()

    def started(self):
        #print("started")
        self.assistantGlyphEditorSubscriberClass.controller = self
        registerGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)

    def destroy(self):
        #print("windowClose")
        unregisterGlyphEditorSubscriber(self.assistantGlyphEditorSubscriberClass)
        self.assistantGlyphEditorSubscriberClass.controller = None


if __name__ == '__main__':
    OpenWindow(ConnectorAssistantController)

  