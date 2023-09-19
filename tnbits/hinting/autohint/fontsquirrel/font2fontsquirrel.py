# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2014+ Type Network
#
#     T N  B I T S
#     No distribution without permission.
#
# -----------------------------------------------------------------------------
#
#            font2fontsquirrel.py
#

import sys
import os
import os.path
import re
import subprocess
import string
import easygui

from fbhint.autohintbase import AutohintBase

class Font2FontSquirrel(AutohintBase):
    u'''
    @@@ Make this to work
    This script prepares fonts for Font Squirrel by
    - changing the Vendor ID from FBI to XXX
    - spitting out a file with the <name> table

    Once the fonts have been run through Font Squirrel this script:
    - Changes Vendor ID back to FBI
    - replaces the <name> table with the table from the original fonts

    MR 120130

    Requires: TTX & EasyGUI
    '''

    def bash(cmd,cwd=None):
        u'''runs a command in the bash shell'''
        print(cmd)
        retVal = subprocess.Popen(cmd, shell=True, \
            stdout=subprocess.PIPE, cwd=cwd).stdout.read().strip('\n').split('\n')
        if retVal==['']:
            return(0)
        else:
            return(retVal)

    def convertToTTXandDelete(file):
        # convert file to TTX
        bash('ttx "' + file+'"')

        # Delete the TTF/OTF file (we'll rebuild it later)
        bash('rm "' + file+'"')

    print('-')
    # Get the folder with the fonts:
    selectFolder = easygui.diropenbox(msg='choose a folder', title='Select Folder', default='~/Desktop/')
    listing = os.listdir(selectFolder)

    for selectFile in listing:

        if selectFile[-4:] == '.ttf':

            if selectFile[-12:] =='-webfont.ttf':

    # POST FONT SQUIRREL

                print('Converting Font Squirreled font: '+ selectFile)
                selectFile = selectFolder + "/"    + selectFile
                convertToTTXandDelete(selectFile)

                # Open the newly created ttx file
                ttxFileFile = selectFile[:-4] + '.ttx'
                ttxFile = open(ttxFileFile, 'r')

                # Read the file
                text = ttxFile.read()

                # Close the file (so we can overwrite it later)
                ttxFile.close()

            # FIX STUFF

                # Replace VENDOR ID in text
                text = re.sub('<achVendID value="XXX "/>', '<achVendID value="FBI "/>', text)

                # Remove Font Squirrel tag in <name>
                # Not needed if we're replacing the entire <name> table
                #text = re.sub('<namerecord nameID="200" platformID="3" platEncID="1" langID="0x409">\n(.*)\n(.*)', '', text)

                # Reopen the original file and replace it with the new text
                ttxFile = open(ttxFileFile, "w")
                ttxFile.writelines(text)
                ttxFile.close()

            # FIX FILE NAME

                # Get the PostScript Name by finding the: Windows something something Name string and the next line
                fontPSString = re.search('<namerecord nameID="6" platformID="3" platEncID="1" langID="0x409">\n(.*)', text)
                fontPSName = fontPSString.group()
                # Isolate the Font Name
                fontPSName = fontPSName[74:]
                # sets the file name with .ttx extension
                corrected_file_name = fontPSName + '.ttx'

                # Get the path to the file
                path = os.path.dirname(os.path.abspath(ttxFileFile))
                corrected_file = path +'/'+ corrected_file_name

                #Rename file using Font Name
                bash('mv "'+ ttxFileFile + '" "' + path +'/'+ corrected_file_name+'"')

                convertToTTXandDelete(corrected_file)

        # MERGE WITH NAME FILE

                ttxNameFile = path + '/' + corrected_file_name[:-4] + '_name' + '.ttx'
                if ttxNameFile:
                    print('Merging', selectFile)

                    corrected_file = corrected_file[:-4] + '.ttf'

                    # TTX Merge command
                    bash('ttx -m "'+corrected_file+'" "'+ttxNameFile+'"')

                    bash('rm "' + corrected_file+'"')
                    bash('rm "' + ttxNameFile+'"')

                    #ttxNameFile[:-4] + '.ttf'
                    #ttxNameFile[:-9] + '.ttf'


                    # Now rename the merged font
                    bash('mv "'+ ttxNameFile[:-4] + '.ttf' + '" "' + ttxNameFile[:-9] + '.ttf'+'"')

                else:
                    print('!No name file found. Not merging', selectFile)


    # PRE FONT SQUIRREL

            else:

                print('Preparing '+selectFile+ ' for Font Squirrel')


                selectFile = selectFolder + "/"    + selectFile


                # GET NAME TABLE (we'll use this after the fonts are converted)

                #spit out the name table
                bash('ttx -t name "' + selectFile+'"')
                # Rename the name table so it doesn't get mucked up with other ttx files
                ttxNameFile = selectFile[:-4] + '_name' + '.ttx'

                #Rename file using new name
                bash('mv "' + selectFile[:-4] + '.ttx' + '" "' + ttxNameFile + '"')


                # CONVERT TO TTX

                convertToTTXandDelete(selectFile)


                # Open the newly created ttx file

                ttxFileFile = selectFile[:-4] + '.ttx'
                ttxFile = open(ttxFileFile, 'r')


                # Read the file
                text = ttxFile.read()

                # Close the file (so we can overwrite it later)
                ttxFile.close()

                #REPLACE STUFF

                # Replace string in text
                text = re.sub('<achVendID value="FBI "/>', '<achVendID value="XXX "/>', text)

                # Reopen the original file and replace it with the new text
                ttxFile = open(ttxFileFile, "w")
                ttxFile.writelines(text)
                ttxFile.close()

                convertToTTXandDelete(ttxFileFile)

                # Fix that _name file so we can find it again
                # Get the PostScript Name by finding the: Windows somethingsomething Name string and the next line
                fontPSString = re.search('<namerecord nameID="6" platformID="3" platEncID="1" langID="0x409">\n(.*)', text)
                fontPSName = fontPSString.group()
                # Isolate the Font Name
                fontPSName = fontPSName[74:]
                # Get the path
                path = os.path.dirname(os.path.abspath(ttxNameFile))

                # sets the file name with .ttx extension
                ttx_name_file_corrected = fontPSName + '_name' + '.ttx'

                bash('mv "' + ttxNameFile + '" "' + path +'/'+ ttx_name_file_corrected + '"')

        else:    # IF it's not a .ttf
            pass

    print('\nFinished.')
