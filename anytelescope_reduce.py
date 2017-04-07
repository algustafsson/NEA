#!/usr/bin/env python

import argparse
import numpy, os
from astropy.io import fits
rootpath = '/Users/user/photometrypipeline'
execfile(rootpath+'/setup/telescopes.py')

def dateobs_to_jd(date):
    date = date.split('T')
    time = date[1].split(':')
    date = date[0].split('-')
    a = (14 - float(date[1]))//12
    y = float(date[0]) + 4800 - a
    m = float(date[1]) + 12*a - 3
    return float(date[2]) + ((153*m + 2)//5) + 365*y + y//4 - y//100 + y//400 - \
        32045.5 + float(time[0])/24. + float(time[1])/1440. + float(time[2])/86400.


####### command line parser                                                    
                                    
# define command line arguments                                                
parser = argparse.ArgumentParser(description='reduce raw science image(s)')
parser.add_argument('-dark', help='masterdark file')             
parser.add_argument('-flat', help='masterflat file') 
parser.add_argument('-flipx', help='flip image x axis', action="store_true")
parser.add_argument("instrument", choices=['Bok90Prime', 'LutzCCD', 'DCTLMI', 'LOWELL72','MAGIMACS'], help="instrument with which the data have been taken")
parser.add_argument('image', help='raw science image(s)', nargs='+')
             
args = parser.parse_args()                         
masterdark = args.dark
masterflat = args.flat                        
instrument = args.instrument
imagefiles = args.image  
flipx = args.flipx

###### MAIN

if instrument == 'Bok90Prime':
    obsparam = bok90prime_param
if instrument == 'LutzCCD':
    obsparam = lutzccd_param
if instrument == 'DCTLMI':
    obsparam = dctlmi_param    
if instrument == 'LOWELL72':
    obsparam = lowell72_param
if instrument == 'MAGIMACS':
    obsparam = magimacs_param

    
for image in imagefiles:
    print image

    hdulist = fits.open(image)

    prime_header = hdulist[0].header
    data = hdulist[0].data
        
        
        
    ###### subtract bias

    if masterdark is not None:
        # read in masterdark data
        hdulist = fits.open(masterdark)
        masterdark_data = hdulist[0].data
        if masterdark_data.shape != data.shape:
            print 'different sizes of science and bias:', data.shape, masterdark_data.shape
            os.abort()
        # subtract bias
        data = data - masterdark_data

    ###### divide by flat

    if masterflat is not None:
        # read in masterflat data
        hdulist = fits.open(masterflat)
        masterflat_data = hdulist[0].data
        if masterflat_data.shape != data.shape:
            print 'different sizes of science and flat:', data.shape, masterflat_data.shape
            os.abort()
        # divide by flat
        data = data / masterflat_data


    #### crop final image if necessary
    # if instrument == 'DCTLMI':
    #     trimsec = header['TRIMSEC'].replace('[', '').replace(']', '').split(',')
    #     #trimsec = header['TRIM01'].replace('[', '').replace(']', '').split(',')
    #     data = data[int(float(trimsec[1].split(':')[0]))-1:int(float(trimsec[1].split(':')[1]))-1,int(float(trimsec[0].split(':')[0]))-1:int(float(trimsec[0].split(':')[1]))-1]
    #     #data = data[int(float(trimsec[0].split(':')[0]))-1:int(float(trimsec[0].split(':')[1]))-1,int(float(trimsec[1].split(':')[0]))-1:int(float(trimsec[1].split(':')[1]))-1]


    ### write final merged and corrected image

    final = fits.PrimaryHDU(data)
    final.header = prime_header

    os.remove('r'+image) if os.path.exists('r'+image) else None
    final.writeto('r'+image, output_verify='silentfix')

