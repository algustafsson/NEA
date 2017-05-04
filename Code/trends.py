""" Trends - Plots histograms of period and amplitude to look for general trends across asteroids in the MANOS data search.
    v1.0: 2017-4-20, ag765@nau.edu, A Gustafsson & M. Zeilnhofer
    
    To use, enter on the command line:
    python trends.py
    
    requires:
    - os
    - matplotlib
    - pyplot
    
    updates:
    -  None
    """

## Import all necessary packages ##
import os
import matplotlib.pyplot as plt
import numpy as np

## Import path ##
list_of_files = os.listdir(os.getcwd())


## Get Amplitude and Period ###
PER = []
AMP = []
for filename in list_of_files:
    print(filename)
    with open(filename) as infile:
        next(infile)
        next(infile)
        for line in infile:
            print(line)
            amplitude = float(line.split()[0])
            period = float(line.split()[1])
            AMP.append(amplitude)
            PER.append(period)
AMPLITUDE = np.array(AMP)
PERIOD = np.array(PER)
print(AMPLITUDE)
print(PERIOD)

AMP_std = np.std(AMPLITUDE))
AMP_mean = np.mean(AMPLITUDE))
PER_std = np.std(np.absolute(PERIOD)))
PER_mean = np.mean(np.absolute(PERIOD)))

#plt.hist(AMPLITUDE, bins=np.arange(min(AMPLITUDE), max(AMPLITUDE) + 0.05, 0.05))
#plt.xlabel('Amplitude (magnitudes)')
#plt.ylabel('Number')
#plt.title(r'Asteroid Lower Limit Amplitude Trends $\mu=AMP_mean,\ \sigma=AMP_std$')
#plt.axis([0, 0.5, 0, 20])
#plt.grid(True)
#plt.show()

plt.hist(np.absolute(PERIOD), bins=np.arange(min(AMPLITUDE), max(AMPLITUDE) + 1, 1))
plt.xlabel('Period (minutes)')
plt.ylabel('Number')
plt.title('Asteroid Lower Limit Period Trends $\mu=PER_mean,\ \sigma=PER_std$')
plt.axis([0, 18, 0, 15])
plt.grid(True)
plt.show()

