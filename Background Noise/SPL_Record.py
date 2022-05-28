import pytta
import os

#%% Create a directory to save the current measurement
meas_name = 'Bkgn Meas 01'
os.mkdir(meas_name) # You'll get an error if trying to create a folder using same the names
os.chdir(os.path.join(os.getcwd(), meas_name)) # Changes to the newly created directory

#%% Signal recording function
def record_signal(save_name1, save_name2):
    for n in range(2):
        device = 1
        measurementParams = {
                'lengthDomain': 'time',
                'timeLength': timelen,
                'samplingRate': 51200,
                'freqMin': 20,
                'freqMax': 20000,
                'device': device,
                'inChannels': [n+1], # It measures each channel at time
                'comment': 'Parameters for the SPL measurement'
        }
        
        ms = pytta.generate.measurement('rec',
                                        **measurementParams)        
        #%% Start measurement
        input('>>Press Enter to measure channel '+str(n+1)+' ')                  
        meas = ms.run()
        
        #%% Shows the data
        meas.plot_time(); meas.plot_freq() # Plots
        # meas.play() # Reproduces the recorded sound
        
        #%% Save the measurement                
        # Saving the two recordings in separated files, for further analysis
        if n == 1:        
            pytta.save(save_name1, ms, meas) # Save PyTTaObj as HDF5 file
            pytta.write_wav(save_name1+'.wav', meas) # Export wave file of SignalObj
        else:
            pytta.save(save_name2, ms, meas) # Save PyTTaObj as HDF5 file
            pytta.write_wav(save_name2+'.wav', meas) # Export wave file of SignalObj
 
#%%%%%%%%%%%%%% CALIBRATION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
rcv = input('Do you want to calibrate your equipment? (y/n) ')
if rcv == 'y':
    timelen = 5 # How long one wants to record (seconds)
    print('\n ~~~Calibration measurement starting~~~')
    record_signal('CalibSignal1', 'CalibSignal2')

#%%%%%%%%%%%%%% BACKGROUND NOISE MEASUREMENT %%%%%%%%%%%%%%%%%%%
print('\n \n ~~~Background noise measurement starting~~~')
timelen = 5 # How long one wants to record (seconds)
record_signal('bkgn1', 'bkgn2')
