import pytta
import numpy as np
import SPL_Functions as splfun
import matplotlib.pyplot as plt
import os

#%%======================================= SPL calc =====================================
# Open previous recording
cwd = os.path.dirname(__file__)  
os.chdir(cwd+'\Bkgn Meas 01') # Chose the folder you want to analyse, ex: (cwd+'\folder_name')

meas = pytta.read_wav("bkgn1.wav")
# uncalib_fig = meas.plot_freq(); plt.show()

#%% Calibration step
rcv = input("Do you want to load calibration signal to make corrections? (y/n) ")
if rcv == 'y':    
    # Open the calibration signal
    calib = pytta.read_wav("CalibSignal1.wav")    
    calib.plot_freq()
    
    meas.calib_pressure(0, calib) #pytta's function to calibrate
    # calib_fig = meas.plot_freq(); plt.show()

#%% Calculating LZeq, LAeq and LCeq

# Plot the frequency weight filters
fig, ax = splfun.plot_weightings(); plt.show()

# Sampling rate
fs = meas.samplingRate

meas_A = splfun.weight_signal(meas.timeSignal, fs, 'A')
meas_C = splfun.weight_signal(meas.timeSignal, fs, 'C')

# RMS levels
Prms_Z = splfun.rms(meas.timeSignal)
Prms_A = splfun.rms(meas_A)
Prms_C = splfun.rms(meas_C)

# # Leq calculation
p_ref = 20e-6
LZeq = 20*np.log10(Prms_Z/p_ref); print('\nLZeq = ', LZeq, 'dB')
LCeq = 20*np.log10(Prms_C/p_ref); print('LCeq = ', LCeq, 'dB')
LAeq = 20*np.log10(Prms_A/p_ref); print('LAeq = ', LAeq, 'dB')

#%% Octave filters

# Generate n/th octave bands frequency array
nth = 1
bands = splfun.band_freq_arr(nth)

# Covert signal array to pytta object so it can be filtered using pytta functions
med_A_pytta = pytta.SignalObj(signalArray = meas_A, domain='time', samplingRate = fs)
med_C_pytta = pytta.SignalObj(signalArray = meas_C, domain='time', samplingRate = fs)

# Sound level in octaves
LoctZ = splfun.octfilter(meas,nth,bands)
LoctA = splfun.octfilter(med_A_pytta,nth,bands)
LoctC = splfun.octfilter(med_C_pytta,nth,bands) 

#%% Plot SPL in octaves
freq = np.arange(1, np.size(bands)+1 , 1)
plt.xticks(freq, bands, rotation=90, fontsize=9.5);

plt.title(r'Sound Pressure Level with three different weightings') 
plt.xlabel('Frequency [Hz]')
plt.ylabel('SPL [dB ref.: 20$\mu$Pa]')
plt.ticklabel_format

Z = plt.bar(freq-0.25, LoctZ, label = 'LoctZ', width = 0.25)
C = plt.bar(freq, LoctC, label = 'LoctC', width = 0.25)
A = plt.bar(freq+0.25, LoctA, label = 'LoctA', width = 0.25)
plt.legend()

# Save figure
cwd = os.path.dirname(__file__)  
os.chdir(cwd+'\SPL Plots') 

plt.savefig('SPL plot.pdf',bbox_inches='tight') 
