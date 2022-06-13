#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>

// GUItool: begin automatically generated code
AudioInputI2S            i2s1;           //xy=253,238
AudioAmplifier           amp1;           //xy=525,221
AudioAmplifier           amp2;           //xy=559,283
AudioOutputUSB           usb1;           //xy=810,244
AudioConnection          patchCord1(i2s1, 0, amp1, 0);
AudioConnection          patchCord2(i2s1, 1, amp2, 0);
AudioConnection          patchCord3(amp1, 0, usb1, 0);
AudioConnection          patchCord4(amp2, 0, usb1, 1);
// GUItool: end automatically generated code


void setup() {
  // put your setup code here, to run once:
    AudioMemoryUsageMax();
    AudioMemory(256);
    amp1.gain(1);
    amp2.gain(1);

}

void loop() {
  // put your main code here, to run repeatedly:

}
