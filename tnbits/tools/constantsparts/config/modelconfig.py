# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#    roboflightconfig.py
#
#    Install a local copy of this in site-packages for local dependencies of paths.
#    The file should be addressable as 
#    from tnbits.constantparts.config.config import Config
#    Otherwise this file will be used by inheriting the Constant class from it.
#    This config needs to be used for paths (such as installed applications) that
#    are different for setup of RoboFont and for the storage of login information
#    that should not become part of Git.
#
class Config:
    
    LOCAL = True

    USER = 'USER_NAME_HERE'
    
    HOST = 'localhost'
    PORT = None
    
