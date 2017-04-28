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

plt.hist(AMPLITUDE)
plt.xlabel('Amplitude (magnitudes)')
plt.ylabel('Number')
plt.title('Asteroid Lower Limit Amplitude Trends')
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()

#plt.hist(PERIOD)
#plt.xlabel('Period (minutes)')
#plt.ylabel('Number')
#plt.title('Asteroid Lower Limit Period Trends')
#plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
#plt.grid(True)
#plt.show()

