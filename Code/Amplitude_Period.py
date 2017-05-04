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
import os.path
import glob
import shutil

###################################
######## Import Data File #########
###################################
LMIdata_dir = "/Volumes/Seagate/Research/Trilling/DCT/LMI/"
directories = [LMIdata_dir+"160530/", LMIdata_dir+"161129/", LMIdata_dir+"170325/", LMIdata_dir+"170403/"]
directory_filter = LMIdata_dir+"150920/" ##Multiple filters, handle differently

for directory in directories:
    object = os.listdir(directory)
    for pointing in object:
        if pointing.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            pass
            true_object = pointing
            object_dir = directory + true_object + "/"
            for filename in os.listdir(object_dir):
                data = directory + true_object + "/" + "photometry_" + true_object + ".dat.varformat"
                if os.path.exists(data) == True:
                    time,mag,err = np.loadtxt(data,unpack=True)
                else:
                    pass

###################################
###### Determine # of Points ######
###################################
            Length = len(mag)
            print("--- There are %d exposures ---" % Length)
            number = int(0.1*Length)
            if number == 1:
                number = 2
            if number == 0:
                number = 1

###################################
####### Determine Amplitude #######
###################################
#### Sort Magnitude Vector ####
            magSorted = np.sort(mag)

#### Find Max and Min ####
            maxAmp_list = []
            minAmp_list = []
            for i in range(0,number):
                maxAmp_list.append(magSorted[i])
                minAmp_list.append(magSorted[Length-1-i])

            maxAmp = np.mean(maxAmp_list)
            print("--- The Maximum Amplitude is %r magnitudes ---" % maxAmp)
            minAmp = np.mean(minAmp_list)
            print("--- The Minimum Amplitude is %r magnitudes ---" % minAmp)

            avgAmplitude = minAmp - maxAmp
            print("--- The Lower Limit Amplitude is %r magnitudes ---" % avgAmplitude)

###################################
######### Determine Period ########
###################################
            maxTime_list = []
            minTime_list = []
            for i in range(0,number):
                Imax_i = np.where(mag==maxAmp_list[i])
                Imin_i = np.where(mag==minAmp_list[i])

                maxTime_list.append(time[Imax_i][0])
                minTime_list.append(time[Imin_i][0])

            maxTime = np.mean(maxTime_list)
            print("--- The Maximum Time is %r Julian Days ---" % maxTime)
            minTime = np.mean(minTime_list)
            print("--- The Minimum Time is %r Julian Days ---" % minTime)

            avgTime = minTime - maxTime
            print("--- The Lower Limit Period is %r Julian Days ---" % avgTime)
            day_hour = 24
            hours = avgTime*day_hour
            minutes = hours*60
            print("--- The Lower Limit Period is %r Minutes ---" % minutes)

###################################
######## Constrain Values #########
###################################
            sigma = np.median(err)
            uncertainty = (sigma/avgAmplitude)*100
            if uncertainty >= 100:
                print("--- The Amplitude is within the Noise ---")
                avgAmplitude = 0

            stddev = np.std(time)
            if avgTime <= 2*stddev:
                avgTime = 0

###################################
### Write Results to Text File ####
###################################

            phot,string_name = data.split("_",1)
            objname,other = string_name.split(".dat")
            #outfile = 'LCanalysis_'+objname+'.txt'
            outfile = 'LCanalysis_'+true_object+'.txt'

            f= open(outfile,"w+")

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

            #directory = os.path.dirname('/Users/user/Desktop/LCanalysis') ##Test Directory
            if not os.path.exists(LMIdata_dir+'LCanalysis'):
                os.mkdir(LMIdata_dir+'LCanalysis')
            
            #for filename in glob.iglob('LCanalysis_*.txt'):
                #old_name = '/Users/user/Desktop/LCanalysis/'+filename ##Test Name
            new_name = LMIdata_dir+'/LCanalysis/' + outfile
            os.rename(outfile,new_name)



###################################
###################################
# REPEAT for 150920 in VR filter #
###################################
###################################

directory_filter = LMIdata_dir+"150920/" ##Multiple filters, handle differently

object = os.listdir(directory_filter)
print(object)
for pointing in object:
    if pointing.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
        true_object = pointing
        print(true_object)
        object_dir = directory_filter + true_object + "/" + true_object + "_VR/"
        for filename in os.listdir(object_dir):
            data = directory_filter + true_object + "/" + true_object + "_VR/" + "photometry_" + true_object + ".dat.varformat"
            if os.path.exists(data) == True:
                time,mag,err = np.loadtxt(data,unpack=True)
            else:
                mag = np.zeros(10)
                time = np.zeros(10)
                err = np.zeros(10)
                print(true_object, "has bad photometry")
    
        ###################################
        ###### Determine # of Points ######
        ###################################
        Length = len(mag)
        print("--- There are %d exposures ---" % Length)
        number = int(0.1*Length)
        if number == 1:
            number = 2
        if number == 0:
            number = 1
        
        ###################################
        ####### Determine Amplitude #######
        ###################################
        #### Sort Magnitude Vector ####
        magSorted = np.sort(mag)
        #### Find Max and Min ####
        maxAmp_list = []
        minAmp_list = []
        for i in range(0,number):
            maxAmp_list.append(magSorted[i])
            minAmp_list.append(magSorted[Length-1-i])
        
        maxAmp = np.mean(maxAmp_list)
        print("--- The Maximum Amplitude is %r magnitudes ---" % maxAmp)
        minAmp = np.mean(minAmp_list)
        print("--- The Minimum Amplitude is %r magnitudes ---" % minAmp)
        
        avgAmplitude = minAmp - maxAmp
        print("--- The Lower Limit Amplitude is %r magnitudes ---" % avgAmplitude)
        
        ###################################
        ######### Determine Period ########
        ###################################
        maxTime_list = []
        minTime_list = []
        for i in range(0,number):
            Imax_i = np.where(mag==maxAmp_list[i])
            Imin_i = np.where(mag==minAmp_list[i])
            
            maxTime_list.append(time[Imax_i][0])
            minTime_list.append(time[Imin_i][0])
        
        maxTime = np.mean(maxTime_list)
        print("--- The Maximum Time is %r Julian Days ---" % maxTime)
        minTime = np.mean(minTime_list)
        print("--- The Minimum Time is %r Julian Days ---" % minTime)
        
        avgTime = minTime - maxTime
        print("--- The Lower Limit Period is %r Julian Days ---" % avgTime)
        day_hour = 24
        hours = avgTime*day_hour
        minutes = hours*60
        print("--- The Lower Limit Period is %r Minutes ---" % minutes)
        
        ###################################
        ######## Constrain Values #########
        ###################################
        sigma = np.median(err)
        uncertainty = (sigma/avgAmplitude)*100
        if uncertainty >= 100:
            print("--- The Amplitude is within the Noise ---")
            avgAmplitude = 0
        
        stddev = np.std(time)
        if avgTime <= 2*stddev:
            avgTime = 0
        
        ###################################
        ### Write Results to Text File ####
        ###################################
        
        phot,string_name = data.split("_",1)
        objname,other = string_name.split(".dat")
        #outfile = 'LCanalysis_'+objname+'.txt'
        outfile = 'LCanalysis_'+true_object+'.txt'
        
        f= open(outfile,"w+")
        
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
        
        #directory = os.path.dirname('/Users/user/Desktop/LCanalysis') ##Test Directory
        if not os.path.exists(LMIdata_dir+'LCanalysis'):
            os.mkdir(LMIdata_dir+'LCanalysis')
        
        #for filename in glob.iglob('LCanalysis_*.txt'):
        #old_name = '/Users/user/Desktop/LCanalysis/'+filename ##Test Name
        new_name = LMIdata_dir+'/LCanalysis/' + outfile
        os.rename(outfile,new_name)
