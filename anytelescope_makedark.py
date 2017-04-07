#!/usr/bin/env python

import argparse
import numpy, os
from astropy.io import fits

####### command line parser                                                    
                                    
# define command line arguments                                                
parser = argparse.ArgumentParser(description='create masterdark/bias')
parser.add_argument('images', help='dark/bias frames', nargs='+')
             
args = parser.parse_args()                         
filenames = args.images


data = []

# merge image data
for image in filenames:
    hdulist = fits.open(image)

    prime_header = hdulist[0].header
    prime_header.remove('BZERO')

    data.append(hdulist[0].data)

# combine images
os.remove('masterdark.fits') if os.path.exists('masterdark.fits') else None

combined_hdu = fits.PrimaryHDU(numpy.median(data, axis=0))

combined_hdu.header = prime_header
combined_hdu.header['HISTORY'] = 'combination of %d frames' \
                                 % len(data)
combined_hdu.writeto('masterdark.fits', output_verify='silentfix')

