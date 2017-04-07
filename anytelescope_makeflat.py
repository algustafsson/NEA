#!/usr/bin/env python

import argparse
import numpy, os
from astropy.io import fits

####### command line parser                                                    
                                    
# define command line arguments                                                
parser = argparse.ArgumentParser(description='create masterflat')
parser.add_argument('dark', help='masterdark/bias image')
parser.add_argument('images', help='flat frames', nargs='+')
             
args = parser.parse_args()                         
masterdark = args.dark
filenames = args.images

###### MAIN

# read in masterdark
hdulist = fits.open(masterdark)
dark_data = hdulist[0].data

norm_flat_data = []

# merge image data
for image in filenames:
    hdulist = fits.open(image)

    prime_header = hdulist[0].header
    prime_header.remove('BZERO')

    data = hdulist[0].data

    # subtract dark image
    data = data - dark_data
 
    # mask saturated areas
    saturation = numpy.ma.masked_where(data > 60000, data)
    saturation.fill_value = numpy.median(data)
    data = saturation.data

    # normalize data 
    print image, 'median =', numpy.median(data)
    norm_flat_data.append(data / numpy.median(data))


# combine images
os.remove('masterflat.fits') if os.path.exists('masterflat.fits') else None

combined_hdu = fits.PrimaryHDU(numpy.median(norm_flat_data, axis=0))

combined_hdu.header = prime_header
combined_hdu.header['HISTORY'] = 'combination of %d frames' \
                                 % len(norm_flat_data)
combined_hdu.writeto('masterflat.fits', output_verify='silentfix')
