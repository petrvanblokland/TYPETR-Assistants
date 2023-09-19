# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
import os
from tnbits.toolbox.transformer import TX

class CompileTX:
    """
    """

    @classmethod
    def getCompiler(cls):
        from ufo2fdk import OTFCompiler
        return OTFCompiler()

    @classmethod
    def compileOTF(cls, f, path):
        o = cls.getCompiler()
        o.compile(
                  f,
                  path,
                  checkOutlines = False,
                  autohint =False,
                  releaseMode = True,
                  )

    @classmethod
    def checkOutlines(cls, path, output=False):
        basePath, fileAndExt = os.path.split(path)
        outputFilePath = os.path.join(basePath, 'checkOutlines.log')
        # forget remove overlap
        try:
            TX.bash('checkOutlines -e -k -O %s' %(path))
        except:
            pass
        if not output and os.path.exists(outputFilePath):
            os.remove(outputFilePath)
        # forget path direction
        try:
            TX.bash('checkOutlines -e -k -V %s' %(path))
        except:
            pass
        if not output and os.path.exists(outputFilePath):
            os.remove(outputFilePath)

    @classmethod
    def fdkAutohint(cls, path, output=False):
        try:
            TX.bash('autohint -a -nb %s' %(path))
        except:
            pass
        basePath, fileAndExt = os.path.split(path)
        outputFilePath = os.path.join(basePath, 'autohint.log')
        if not output and os.path.exists(outputFilePath):
            os.remove(outputFilePath)


if __name__ == '__main__':
    from tnbits.toolbox.font import FontTX
    from tnbits.toolbox.file import File
    basePath = os.getcwd()
    paths = File.collect(basePath, extensionInclude=['.otf'])
    for path in paths:
        FontTX.compile.checkOutlines(path)
        FontTX.compile.fdkAutohint(path)
    print('done')



