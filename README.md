# RadarScope
FMCW Radar data processing visualizer 


![image](https://user-images.githubusercontent.com/11905989/110249136-9cca3a00-7f42-11eb-9369-ca19e8c13fa8.png)

# Usage

Run TeencyFFT on a Teency 4.0 or similar. Keep the microcontroller connected to your computer via USB. The teency will sample pin 14 at 1000Hz.

ToneGen can be run on a second microcontroller to act as sample input. The varying tone will output to pin 14.

Run SerialMonitor.py to test the connection. A packet recieved rate in hertz should be displayed.

Execute RadarScope.py to display the FFT and a waterfall diaplay.



