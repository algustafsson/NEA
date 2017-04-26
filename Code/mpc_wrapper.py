#!/usr/bin/env python
""" mpc_wrapper
Reads in the photometry_****.dat file(s) and outputs them in the correct
format for MPC submission. Currently can handle all asteroids. Comet renaming
will come in the future as well as discovered object formats.

need:
- photometry_****.dat

requires:
- astropy
- os
- time

2017-04-24, Dan Avner, davner@nau.edu
"""

###############################################################################
# imports
from astropy.io import ascii
from astropy.io import fits
from astropy.time import Time
import os.path
from astropy.coordinates import Angle
import astropy.units as u
import time
import argparse

###############################################################################
# allows the user to enter the .dat file from terminal or *.dat
parser = argparse.ArgumentParser(
    description='create the mpc submission txt file with formatting')
parser.add_argument('phot', help='photometry.dat file (s)', nargs='+')
args = parser.parse_args()
photFiles = args.phot

###############################################################################
# constants
CONVERSION_KEY = (
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
CHAR_DICT = {'18':'I', '19':'J', '20':'K'}
MEASURER = 'Enter measurer...'
EMAIL = 'Enter email...'
OBSERVER = 'Enter observer...'
CODE = 'G37'

###############################################################################
"""
Reads the objects name and packs it to MPC format. For more information on what
the format needs to be, go to:
http://www.minorplanetcenter.net/iau/info/PackedDes.html
"""
def pack_name(objName):
    if len(objName.split()) == 2:
        if objName[:2] in CHAR_DICT:
            char1 = CHAR_DICT[objName[:2]]
            char23 = objName[2:4]
            char4 = objName[5]
            char7 = objName[6]

            if len(objName) == 7:
                char56 = "00"

            elif len(objName) == 8:
                char56 = "0%s" % objName[7]

            elif len(objName) == 9:
                char56 = objName[7:9]

            elif len(objName) == 10:
                char5 = CONVERSION_KEY[int(objName[7:9])]
                char6 = objName[9]
                char56 = '%s%s' % (char5, char6)

            finalName = (
                '%s%s%s%s%s' % (
                    char1,
                    char23,
                    char4,
                    char56,
                    char7))
        else: finalName = objName
        mpcFormat = 'long'


    elif int(objName) <= 99999:
        if len(objName) < 5:
            finalName = '%s' % objName.zfill(5)
        else: finalName = objName
        mpcFormat = 'short'

    elif int(objName) >= 100000:
        char1 = CONVERSION_KEY[int(objName[:2])]
        finalName = '%s%s' % (char1, objName[2:])
        mpcFormat = 'short'

    else:
        finalName = objName
        mpcFormat = 'long'

    return finalName, mpcFormat

###############################################################################
"""
Iterates through all photometry file(s) then reads line by line while writing
the mpc file.
"""
for phot in photFiles:
    photTxt = phot
    astTxtObj = photTxt.split('photometry_')[1].split('.')[0]
    txtTime = time.strftime('%Y.%m.%d %H:%M:%S')
    backupStamp = time.strftime('%Y%m%d%H%M%S')
    astTxt = 'mpc_%s.txt' % astTxtObj

    # if the output file exists, rename it with a timestamp
    if os.path.isfile(astTxt):
        BackupTxt = 'mpc_%s_%s.txt' % (astTxtObj, backupStamp)
        print ('Old mpc txt file exists, renaming...\n%s ---> %s' % (
            astTxt,
            BackupTxt))
        os.rename(astTxt, BackupTxt)

    print 'Writing astrometry and photometry for %s' % astTxtObj
    data = ascii.read(photTxt)
    # goes through the data by row and extracts important information
    for d in data:
        mag = d['ast_mag']
        ra = Angle(d['ast_ra'], unit = u.degree)
        ra = ra.to_string(unit = u.hour,
                          sep = ' ',
                          pad = True,
                          precision = 2)
        dec = Angle(d['ast_dec'], unit = u.degree)
        dec = dec.to_string(unit = u.degree,
                            sep = ' ',
                            pad = True,
                            precision = 1,
                            alwayssign = True)
        jd = Time(d['julian_date'], format = 'jd')
        tele = d['[9]']
        filt = d['[7]']
        cat = d['[6]'].split('_')[0]
        objName = (
            photTxt.split('photometry_')[1].split('.')[0].replace('_', ' '))
        finalName, mpcFormat = pack_name(objName)
        date = jd.iso.split()[0].replace('-', ' ')
        hour, minute, sec = jd.iso.split()[1].split(':')
        # MPC wants the decimal day
        decDay = (str(
            (float(hour) +
            (float(minute) / 60) +
            (float(sec)/ 3600)) / 24))
        obsDate = '%s.%.5s' % (date, decDay.split('.')[1])

        # if file does not exist write header
        if not os.path.isfile(astTxt):
            with open(astTxt, 'w') as file:
                header = (
                    'COD %s\n'
                    'TEL %s\n'
                    'OBS %s\n'
                    'MEA %s\n'
                    'ACK MPCReport file updated %s\n'
                    'AC2 %s\n'
                    'NET %s\n' % (
                        CODE,
                        tele,
                        OBSERVER,
                        MEASURER,
                        txtTime,
                        EMAIL,
                        cat))
                file.write(header)

        # write info line depending on name
        if mpcFormat == 'long':
            line = (
                    '     %s   %s %s %s          %.1f %s      %s\n' % (
                        finalName,
                        obsDate,
                        ra,
                        dec,
                        mag,
                        filt,
                        CODE))
        elif mpcFormat == 'short':
            line = (
                    '%s          %s %s %s          %.1f %s      %s\n' % (
                        finalName,
                        obsDate,
                        ra,
                        dec,
                        mag,
                        filt,
                        CODE))

        with open(astTxt, 'a') as file:
            file.write(line)

    # write closer
    with open(astTxt, 'a') as file:
        file.write('----- end -----')
    print 'Finished!'
###############################################################################
