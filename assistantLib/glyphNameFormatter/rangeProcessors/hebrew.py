# Edited in March 2016 by Daniel Grumer
# Spelling of Cantillation Marks were adjusted according to Wikipedia (https://en.wikipedia.org/wiki/Cantillation)


def process(self):
    # Those are ligatures. They can be used for both Hebrew and Yiddish, no need for language indication. 
    self.replace("HEBREW LIGATURE YIDDISH DOUBLE VAV", "vav_vav") 
    self.replace("HEBREW LIGATURE YIDDISH VAV YOD", "vav_yod") 
    self.replace("HEBREW LIGATURE YIDDISH DOUBLE YOD", "yod_yod")
    
    # This is a change that was not created by me, but seems totally fine. I also have no idea what those marks are used for (will try to find out)
    self.replace("HEBREW MARK UPPER DOT", "dotupper")
    self.replace("HEBREW MARK LOWER DOT", "dotlower")
        
    # Those are changes in spelling, to match the Ashkenazi naming as they appear in Wikipedia:
    self.edit("ATNAH HAFUKH", "atnachHafukh")
    self.edit("MUNAH", "munach")
    self.edit("MAHAPAKH", "mahpach")
    self.edit("MERKHA KEFULA", "merchaKefulah")
    self.edit("MERKHA", "mercha")
    self.edit("QARNEY PARA", "qarneFarah")       
    self.edit("TELISHA GEDOLA", "telishaGedolah")
    self.edit("TELISHA QETANA", "telishaQetannah")
    self.edit("TIPEHA", "tifcha")
    self.edit("YERAH BEN YOMO", "yerachBenYomo")
    self.edit("ZINOR", "tsinnorit")                  
    self.edit("HOLAM HASER FOR VAV", "holamHaser")
    self.edit("DAGESH OR MAPIQ", "dagesh")
    self.edit("MARK MASORA CIRCLE", "masoraCircle")

    # Those are just adding the word-separation
    self.edit("GERESH MUQDAM", "gereshMuqdam")
    self.edit("ZAQEF QATAN", "zaqefQatan")
    self.edit("ZAQEF GADOL", "zaqefGadol")
    self.edit("SOF PASUQ", "sofPasuq")
    self.edit("HATAF SEGOL", "hatafSegol")
    self.edit("HATAF PATAH", "hatafPatah")
    self.edit("HATAF QAMATS", "hatafQamats")
    self.edit("SIN DOT", "sinDot")
    self.edit("SHIN DOT", "shinDot")
    self.edit("NUN HAFUKHA", "nunHafukha")
    self.edit("QAMATS QATAN", "qamatsQatan")

    # avoid multiple names
    self.edit("ACCENT SEGOL", "segolta")                 # different name chosen to avoid multiples         
    self.edit("ACCENT GERSHAYIM", "SheneGerishin")       # different name chosen to avoid multiples  
    self.edit("ACCENT GERESH", "azla" )                  # different name chosen to avoid multiples    

    # used in alphabetic presentation forms
    self.edit("WIDE", "wide")
    self.edit("JUDEO-SPANISH", 'judeospanish')
    self.edit("HEBREW LIGATURE YIDDISH YOD YOD PATAH", "yod_yod_patah")
    self.edit("ALTERNATIVE", "alt")

    # cleanup
    self.edit("POINT")          # 'Nikud' marks        Vowel-pointing system
    self.edit("ACCENT")         # Cantillation marks   Used in religious texts, to indicate how to sing     
    self.edit("PUNCTUATION")    # Puncutation marks    Used in religious texts (regular texts use the latin period, comma, colon etc)
    self.edit("MARK")           # Other marks          I couldn't find what they are used for

    if self.has("YIDDISH"):
        if self.replace("YIDDISH"):
            self.suffix("yiddish")
    if self.has("PUNCTUATION"):
        self.replace("PUNCTUATION")

    self.edit("HEBREW LETTER")
    self.edit('HEBREW')
    self.edit("LETTER")
    self.lower()
    self.compress()
    self.scriptPrefix()

if __name__ == "__main__":
    from assistantLib.glyphNameFormatter.exporters import printRange
    printRange("Hebrew")
