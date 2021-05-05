# RadarScope
The real time signal processing and visualization componenet of my FMCW radar senior design project.

## Setup 
1. Install required dependencies

2. Run TeensyFFTHighSpeed on a Teensy 4.0 or similar. Keep the microcontroller connected to your computer via USB. The teency will sample pin 14 at 50KHz, compute 2048 point FFTs, and transmit the data to AsyncSerialInput via USB.

3. Connect the output of your radar to pin 14 on the teensy.

If you don't have a radar, ToneGen can be run on a second microcontroller to act as sample input. The varying tone will output to pin 14.

5. Execute main.py to process and visualize the data in real time.

## Usage

Run the program.
```
python main.py 
```

Run the program and save the FFT data to be played back later
```
python main.py --save <name>
```

Run the program using saved data as input
```
python main.py --replay <name>
```

## Customization 
There are a number of functions in ModularScope.py that can display the data in different ways. You can call these function from main.py to change what graphs you want to display. 


## Dependencies
- pyserial
- numpy
- scipy
- pyqtgraph
- termcolor

## Group Members
- Eli Clark 
- Jack Guida
- Jinzhi Cai 


