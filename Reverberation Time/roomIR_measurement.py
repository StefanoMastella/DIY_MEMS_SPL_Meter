"""
@author: mtslazarin

Editted by Stéfano (28/05/2022)

For more information check PyTTa repository: https://github.com/PyTTAmaster/PyTTa
"""
# %% Initializing

import pytta
from pytta import roomir as rmr
import os

# %% Changes the python's  current work directory to this script folder

cwd = os.path.dirname(__file__) # Get the current folder
os.chdir(cwd)

tempHumid = None  # None when LabJack is offline
fs = 44100

# %% Sweep signals generation

excitationSignals = {}
excitationSignals['varredura18'] = pytta.generate.sweep(
        freqMin=100,
        freqMax=10000,
        fftDegree=18,
        startMargin=0.05,
        stopMargin=1,
        method='logarithmic',
        windowing='hann',
        samplingRate=fs)

excitationSignals['varredura17'] = pytta.generate.sweep(
        freqMin=20,
        freqMax=20000,
        fftDegree=17,
        startMargin=0.05,
        stopMargin=1,
        method='logarithmic',
        windowing='hann',
        samplingRate=fs)

# %% Create a new measurement setup and initialize the data object, which manages 
#MeasurementSetup and measurement data on disk

MS = rmr.MeasurementSetup(name='RT_Meas_01',  # Measurement name
        samplingRate=fs,  # [Hz]
        # Sintax : device = [<in>,<out>] ou <in/out>
        # Use pytta.list_devices() to get the audio devices 
        device=[1,10], # [Teensy, PreSonus]
        noiseFloorTp=5,  # [s] How long is the background noise measurement 
        calibrationTp=2,  # [s] How long is the calibration process 
        excitationSignals=excitationSignals,  
        
        # Number of averages per measurement takes: for large number of averages, 
        # it is recommended to divide them into a few different takes.
        averages=2,  
        pause4Avg=True,  # Pause between averages
        freqMin=100,  # [Hz]
        freqMax=10000,  # [Hz]
        
        # Input and Output channels dictionaries
        inChannels={'Mic1': (1, 'Mic 1'),
                    'Mic2': (2, 'Mic 2')},
        outChannels={'O1': (1, 'Dodecaedro 1')},  
        
        # Input and Output channels and compensations (just in case)
        # inCompensations={'Mic1': (mSensFreq, mSensdBMag)},              
        inCompensations={},       
        # outCompensations={'O2': (sSensFreq, sSensdBMag)})
        outCompensations={})
D = rmr.MeasurementData(MS)

# %% Creates a new Impulse Response take

takeMeasure = rmr.TakeMeasure(MS=MS,
        tempHumid=tempHumid, # LabJack info
        kind='roomres',
        inChSel=['Mic2'],
        receiversPos=['R1'], 
        excitation='varredura18', # Choose the excitation signal
        outChSel='O1',
        outputAmplification=-3, # [dB] Output gain (to avoid clipping)
        sourcePos='S1') # Source position

# %% Creates a new Background noise take

takeMeasure = rmr.TakeMeasure(MS=MS,
        kind='noisefloor',
        inChSel=['Mic1','Mic2'],
        receiversPos=['R1','R1'])

# %% Creates a new source calibration take

takeMeasure = rmr.TakeMeasure(MS=MS,
        tempHumid=tempHumid,
        kind='sourcerecalibration',
        inChSel=['Mic1'], 
        excitation='varredura18',
        outChSel='O2',
        outputAmplification=-6) # [dB]

# %% Creates a new microphone calibration take

takeMeasure = rmr.TakeMeasure(MS=MS,
        tempHumid=tempHumid,
        kind='miccalibration',
        inChSel=['Mic1'])

# %% Creates a new channel calibration take

takeMeasure = rmr.TakeMeasure(MS=MS,
        tempHumid=tempHumid,
        kind='channelcalibration',
        inChSel=['Mic1'],
        excitation='varredura17',
        outChSel='O1',
        outputAmplification=-30) # [dB]

# %% Starts measurement 

takeMeasure.run() 

# %% Save take on disk

D.save_take(takeMeasure)
