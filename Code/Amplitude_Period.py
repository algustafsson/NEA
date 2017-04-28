""" Amplitude_Period
    v1.1: 2017-04-27,  ag765@nau.edu, A. Gustafsson & arw366@nau.edu, A. Weintraub
    
    This script loads in the output from ParsePPlc.py lightcurve data and determines the lower limit on both the amplitude and period.
    
    To use, enter on the command line:
    python Amplitude_Period.py
    
    requires:
    - numpy
    
    """

###################################
## Import all necessary packages ##
###################################
import numpy as np
import os
import glob

###################################
######## Import Data File #########
###################################
data_dir = "/Users/user/photometrypipeline/"
TestFile = "photometry_3199.dat.varformat"
time,mag,err = np.loadtxt(data_dir+TestFile,unpack=True)

###################################
####### Determine Amplitude #######
###################################
Length = len(mag)
print("--- There are %d exposures ---" % Length)

#### Sort Magnitude Vector ####
magSorted = np.sort(mag)

#### Find Max and Min ####
max1 = magSorted[0]
max2 = magSorted[1]
min1 = magSorted[Length-1]
min2 = magSorted[Length-2]

maxAmp = np.mean([max1,max2])
print("--- The Maximum Amplitude is %r magnitudes ---" % maxAmp)
minAmp = np.mean([min1,min2])
print("--- The Minimum Amplitude is %r magnitudes ---" % minAmp)

avgAmplitude = minAmp - maxAmp
print("--- The Lower Limit Amplitude is %r magnitudes ---" % avgAmplitude)

###################################
######### Determine Period ########
###################################
Imax1 = np.where(mag==max1)
Imax2 = np.where(mag==max2)
Imin1 = np.where(mag==min1)
Imin2 = np.where(mag==min2)

max1_time = time[Imax1]
max2_time = time[Imax2]
min1_time = time[Imin1]
min2_time = time[Imin2]

maxTime = np.mean([max1_time,max2_time])
print("--- The Maximum Time is %r Julian Days ---" % maxTime)
minTime = np.mean([min1_time,min2_time])
print("--- The Minimum Time is %r Julian Days ---" % minTime)

avgTime = minTime - maxTime
print("--- The Lower Limit Period is %r Julian Days ---" % avgTime)
day_hour = 24
hours = avgTime*day_hour
minutes = hours*60
print("--- The Lower Limit Period is %r Minutes ---" % minutes)

###################################
###### Determine Uncertainty ######
###################################
sigma = np.median(err)
uncertainty = (sigma/avgAmplitude)*100
if uncertainty >= 90:
    print("--- The Amplitude is within the Noise ---")

###################################
### Write Results to Text File ####
###################################

phot,string_name = TestFile.split("_")
objname,other = string_name.split(".dat")
filename = 'LCanalysis_'+objname+'.txt'

f= open(filename,"w+")

header1 = '# Asteroid' + ' ' + str(objname) + ' ' + 'Lightcurve Analysis Results' + '\n'
header2 = '# Amplitude (mag)' + ' ' + 'Period (min)' + '\n'
data_row = str(avgAmplitude) + ' ' + str(minutes) + '\n'

f.write(header1)
f.write(header2)
f.write(data_row)

f.close()

###################################
### Move output to new folder ####
###################################

LMIdata_dir = "/common/contrib/classroom/ast520/LMIdata/"
os.mkdir(LMIdata_dir+'/LCanalysis')

for filename in glob.iglob('LCanalysis_*.txt'):
    os.rename(filename,LMIdata_dir+'/LCanalysis/'+filename)


