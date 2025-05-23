
import statistics
import math
import numpy
from defcon import addRepresentationFactory, registerRepresentationFactory
import defcon


from numpy import dot
from numpy.linalg import norm
from assistantLib.glyphNameFormatter.reader import u2r, u2c
from .multipleMarginPen import MultipleMarginPen
import fontTools.unicodedata

def NormalizedGlyphProfileFactory(glyph, clip=200):
    la, ra, profile = makeNormalizedProfile(glyph, clip=clip)
    return profile

normalizedProfileKey = "com.letterror.similarity.normalizedGlyphProfile"

defcon.Glyph.representationFactories[normalizedProfileKey] = dict(
    factory=NormalizedGlyphProfileFactory, 
    destructiveNotifications=("Contour.PointsChanged",),
    clip=200,
    )

SimilarGlyphsKey = "com.letterror.similarity.similarGlyphs"


def SimilarityRepresentationFactory(glyph, threshold=0.99, 
                sameUnicodeClass=True, 
                sameUnicodeRange=False, 
                sameUnicodeScript=True,
                zones=None, 
                side="left", 
                clip=200, 
                ):
    # return the glyphs that are similar on the left
    thisUnicodeClass = u2c(glyph.unicode)
    if glyph.unicode is not None:
        thisUnicodeScript = fontTools.unicodedata.script(glyph.unicode)
    else:
        thisUnicodeScript = None
    hits = {}
    font = glyph.font
    for other in font:
        
        if other.unicode is not None:
            otherUnicodeClass = u2c(other.unicode)
            otherUnicodeScript = fontTools.unicodedata.script(other.unicode)
            if sameUnicodeClass and (otherUnicodeClass != thisUnicodeClass) and thisUnicodeClass is not None:
                #print(f"A ----- {glyph.name}: {otherUnicodeScript} {thisUnicodeScript}")                
                continue
            if sameUnicodeScript and (otherUnicodeScript != thisUnicodeScript) and thisUnicodeScript is not None:
                #print(f"B ----- {glyph.name}: {otherUnicodeScript} {thisUnicodeScript}")
                continue

        # the other.unicode is None
        # skip comparisons between a glyph that has a unicode and the other that does not.
        # this may skip some alternates.
        # this may need to be addressed with pseudo-unicodes
        if glyph.unicode is not None and glyph.unicode is None:
            #print(f"\tD ----- {glyph.name}: {glyph.unicode} / {other.name} {other.unicode}")
            continue
        if glyph.unicode is None:
            continue
                
        #print(f"C ----- {glyph.name}: {glyph.unicode} / {other.name} {other.unicode}")                
        # ok here we should only have the glyphs with same unicode script and class if we want to be selective
        score = cosineSimilarity(glyph, other, side=side, zones=zones, clip=clip)
        if score is not None:
            if threshold is not None:
                if score >= threshold:
                    if not score in hits:
                        hits[score] = []
                    hits[score].append(other.name)
            else:
                if not score in hits:
                    hits[score] = []
                hits[score].append(other.name)
    return hits
    
defcon.Glyph.representationFactories[SimilarGlyphsKey] = dict(
    factory=SimilarityRepresentationFactory, 
    destructiveNotifications=("Contour.PointsChanged",),
    threshold=0.99, 
    sameUnicodeClass=True, 
    sameUnicodeScript=True, 
    zones=None, 
    side="left"
    )
        
def stepRange(mn, mx, parts):
    # return a list of parts between mn, mx
    # stepRange(0,10,2)
    # [0.0, 5.0, 10.0]
    v = []
    for i in range(parts+1):
        v.append(mn+(i/(parts)*(mx-mn)))
    return v

def makeNormalizedProfile(glyph, clip=200):
    # make a normalized profile of left and right side of glyph
    # make samples from font.info.descender to font.info.ascender, in stepSize increments
    # ignore samples that are clip distance away from left or right margin
    # de-skew if there is an italic angle set.
    # 
    shift = 30    # test value to add to all sampled values to differentiate with 0, non-samples
    leftValues = []
    rightValues = []
    if glyph is None:
        return None, None, None
    font = glyph.font
    a = font.info.italicAngle
    if a is None:
        a = 0
    profile = []
    sections = [
        (0, font.info.descender, 5),
        (0, font.info.xHeight, 50),
        (font.info.xHeight, font.info.unitsPerEm, 25)
    ]
    sampleHeights = []
    for mn,mx,step in sections:
        [sampleHeights.append(v) for v in stepRange(mn,mx,step) if v not in sampleHeights]
    sampleHeights.sort()
    mmp = MultipleMarginPen(glyph.font, sampleHeights)
    glyph.draw(mmp)
    hits = mmp.getMargins()
    for h in sampleHeights:
        if a != 0:
            ta = math.tan(math.radians(-a)) * h
        else:
            ta = 0
        m = hits.get(h)
        if m is None:
            profile.append((h, None, None))
        else:
            mn = min(m)-ta
            if mn > clip:
                # replace sample with None if clipped
                mn = None
            mx = max(m)-ta
            if mx < (glyph.width-clip):
                # replace sample with None if clipped
                mx = None
            profile.append((h, mn, mx))
    leftValues = []
    rightValues = []
    # calculate the averages
    for i, v in enumerate(profile):
        y, mn, mx = v
        if mn is not None:
            leftValues.append(mn)
        if mx is not None:    
            rightValues.append(mx)
    if not leftValues:
        leftAverage = 0
    else:
        leftAverage = statistics.median_grouped(leftValues)
    if not rightValues:
        rightAverage = 0
    else:
        rightAverage = statistics.median_grouped(rightValues)
    normalized = []
    for i, v in enumerate(profile):
        y, mn, mx = v
        if mn is not None:
            mn -= leftAverage - shift
        else:
            mn = 0
        if mx is not None:            
            mx -= rightAverage - shift
        else:
            mx = 0
        normalized.append((y, mn, mx))      
    return leftAverage, rightAverage, normalized

def getRange(values, zones):
    if zones is None: return values
    ok = []
    for v in values:
        for mn, mx in zones:
            if mn <= v <= mx:
                if v not in ok:
                    ok.append(v)
    ok.sort()
    return ok
        
def cosineSimilarity(first, second, side="left", zones=None, clip=200):
    sides = {}
    firstProfile = first.getRepresentation(normalizedProfileKey, clip=clip)
    secondProfile = second.getRepresentation(normalizedProfileKey, clip=clip)
    leftResult = rightResult = None            
    heights = [a for a,b,c in firstProfile] # the sample heights
    zoned = getRange(heights, zones)
    # we need to manage the numpy error levels for this operation
    # in some cases it will raise a lot of RuntimeWarning: invalid value encountered in double_scalars
    # https://numpy.org/doc/stable/reference/generated/numpy.seterr.html
    # we will store the original settings
    old_settings = numpy.seterr(all='ignore')  #seterr to known value
    result = None
    if side == "left":
        firstLeftProfile = [b for a,b,c in firstProfile if a in zoned]
        secondLeftProfile = [b for a,b,c in secondProfile if a in zoned]
        if firstLeftProfile and secondLeftProfile:
            try:
                result = float(dot(firstLeftProfile, secondLeftProfile)/(norm(firstLeftProfile)*norm(secondLeftProfile)))
            except ValueError:
                return None
    elif side=="right":
        firstRightProfile = [c for a,b,c in firstProfile if a in zoned]
        secondRightProfile = [c for a,b,c in secondProfile if a in zoned]
        if firstRightProfile and secondRightProfile:
            try:
                result = float(dot(firstRightProfile, secondRightProfile)/(norm(firstRightProfile)*norm(secondRightProfile)))
            except ValueError:
                return None
    numpy.seterr(**old_settings)  # reset to default
    return result

def compareGlyphs(font, members, side="left", zones=None):
    # see if the members of this group look like each other
    # returns a dict with comparisons between each of the members
    sideResult = {}
    done = []
    for first in members:
        for second in members:
            key = [first, second]
            key.sort()
            key = tuple(key)
            if first == second: continue
            if key in done: continue
            similarityValue = cosineSimilarity(font[key[0]], font[key[1]], side=side, zones=zones)
            sideResult[key] = similarityValue
            done.append(key)
    return sideResult

