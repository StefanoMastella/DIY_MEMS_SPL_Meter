"""
@author: Stéfano Mastella (last update: 28/05/2022)
"""

import pytta
import os
from pytta import roomir as rmr

# %% Changes the python's  current work directory to this script folder
cwd = os.path.dirname(__file__)  # Get the current folder
os.chdir(cwd+'\RT_Meas_01') # Chose the folder you want to analyse, ex: (cwd+'\folder_name')

# %% Measurement load
meas_name = 'roomres_S1-R1_O1-Mic1_varredura18_1.hdf5' # Write the name of the measurement (don't forget the ".hdf5")

roomres = rmr._h5_load(meas_name)
roomres = roomres.get(meas_name[:-5])
roomres = roomres.measuredSignals
y1t = roomres[0]; y2t = roomres[1]

fmin = 100; fmax = 10000;

xt = pytta.generate.sweep(
    freqMin=fmin,
    freqMax=fmax,
    fftDegree=20,
    startMargin=0.05,
    stopMargin=1,
    method='logarithmic',
    windowing='hann',
    samplingRate=44100)

# Impulse Response
h1t = pytta.ImpulsiveResponse(xt, y1t, regularization=True, method='linear')
h2t = pytta.ImpulsiveResponse(xt, y2t, regularization=True, method='linear')

#%% Using RoomAnalysis to get Reverberation Time
TR1 = pytta.RoomAnalysis(h1t, nthOct=3, minFreq=fmin, maxFreq=fmax)
TR2 = pytta.RoomAnalysis(h2t, nthOct=3, minFreq=fmin, maxFreq=fmax)

# %% Print information and plot the results
print()
print("Parameters from impulse response are:")
print("\n", TR1.parameters, "\n")
print("Access directly by RoomAnalysis().PNAME")
print("Or view it in a bar plot by RoomAnalysis().plot_PNAME")
print("where PNAME is the name of the desired parameter, as shown above.")
print()
print(f"{TR1.T20=}")

fig = TR1.plot_T20()
fig_2 = TR2.plot_T20()
fig.show()