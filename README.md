# DIY_MEMS_SPL_Meter
A low-cost sound level meter using on MEMS microphone for Reverberation Time and Background Noise measurements.

## YouTube Tutorial 

[<img src="README Images/tutorial_screenshot.PNG">](https://www.youtube.com/watch?v=_loZrHiwyes&ab_channel=OneiroAcoustika)
> https://www.youtube.com/watch?v=_loZrHiwyes&ab_channel=OneiroAcoustika

## Requirements

Here is the list of the items you will need:

- I2S MEMS Microphone (in my case I’m using two microphones from a model called msm261s4030h0)
- Teensy 4.0 microcontroller
- Jumpers
- Mini-protoboard
- Micro USB cable
- 3D printed case (Optional)

You will also need the following software:

- [Arduino](https://www.arduino.cc/en/software) 
- [Teensyduino](https://www.pjrc.com/teensy/td_download.html)
- Python
- [PyTTa Toolbox](https://github.com/PyTTAmaster/PyTTa)

## 💻 Teensy config

Connect the devices as shown in the figure below. 

<img src="README Images/Teensy-MEMS connections.PNG">

Install Teensyduino and plug Teensy into the USB port and load the Arduino code into it. It will set the microcontroller to work as a mono or stereo microphone.

## 🚀 Installing PyTTa

To install the last version compiled to pip, which can be slightly behind of development branch, do:
```
>>> pip install pytta
```

## ☕ Using the Sound Level Meter function

U+1F50A ZZZ
🔉
### Recording sound signals

The code 'SPL_record' records the sound signals. It was set up to make calibrations and to record two channels separately. It can be changed to record only one channel if the user decides to.

Use the function pytta.list_devices() to check the sound devices connected to the computer. With this information, change the 'device' variable to the correct number.

```
pytta.list_devices()
```

Choose the recording time length and run the code to start the measurement and save it to the disk.

### SPL Calculations

Use the code 'SPL_Meter' to calculate and plot the sound pressure levels. Change the folder path to the one you want to analyze. 

To calibrate the device one can use a commercial calibrator along with a coupler for the MEMS microphone, use the calibration signal available in the 'Bkgn Meas 01' folder (but only if one uses the same microphone model I did), or use the sensitivity value to adjust the SPL curves. In the third case, the offset value is equal to the Acoustical Overload Point (AOP) minus 94 dB. Declare the 'sens_offset' value and the code will do the rest.

<img src="README Images/SPL_plot.PNG">

In the end, it will return the SPL plot with three different weightings and will print the equivalent sound levels.

## ☕ Using the Reverberation Time function  

To do the reverberation time measurements use the code 'roomIR_measurement', and, to perform the calculations, use 'roomRT_calculation'. 

In 'roomIR_measurement', run the code cell by cell. It will generate the sweep signals and measurement setup.  Declare the 'device' variable with the input and output ports.

There are four kinds of measurements: 
- Room Impulse Response, to measure reverberation time
- Noise floor
- Source calibration
- Microphone calibration
- Channel calibration

Once the measurement take is created run and save it by using:

```
takeMeasure.run() 
D.save_take(takeMeasure)
```

In 'roomRT_calculation' simply select the folder where you previously saved the measurements and run the code to get the results. 

<img src="Reverberation Time\RT Plots/TR.png">

## 📝 License

Feel free to use it and modify it in any way you want. If you want to give me credits, cite this repository. 

𝔉𝔞𝔯𝔢𝔴𝔢𝔩𝔩

[⬆ Top](#nome-do-projeto)<br>
