#include "arduinoFFT.h"

#include <ADC.h>
#include <ADC_util.h>

const int SAMPLE_FREQUENCY = 50000;   // Sampling frequency in Hz
const int FFT_SIZE = 2048;            // Number of FFT Bins

byte SOT[] = {0x02, 0x03, 0x04, 0x05}; // The Start Of Transmission packet

ADC *adc = new ADC();

arduinoFFT FFT = arduinoFFT();

int sampling_period_us;
IntervalTimer sampleTimer; 

int buff[FFT_SIZE * 2];
int* bp = buff;
int side = 0;
int sideLast = 0;
double sReal[FFT_SIZE];
double sImag[FFT_SIZE];
float out[FFT_SIZE];

int timer = 0; // This is used by the helper timer functions.

void setup() {
  timerStart();

  Serial.begin(115200);

  pinMode(A0,INPUT);
  adc->startSingleRead(A0, ADC_0);

  //Calculate the sampling period in microseconds
  sampling_period_us = round(1000000*(1.0/SAMPLE_FREQUENCY));

  //Start the sampling inturupt timer
  sampleTimer.begin(sample, sampling_period_us);
}

//Copy the data from the currently unused side of the buffer into sReal and popilate sImag with 0s
void populate(){
  int* cpyPtr;
  int* endPtr;
  if(side == 0){
    cpyPtr = &buff[FFT_SIZE];
    endPtr = &buff[FFT_SIZE * 2];
  }else{
    cpyPtr = buff;
    endPtr = &buff[FFT_SIZE];
  }
  
  double* rp = sReal;
  double* ip = sImag;

  while(cpyPtr != endPtr){
     *ip = 0.0;
     *rp = static_cast<double>(*cpyPtr);
     rp++;
     ip++;
     cpyPtr++;
  }
  
}

// Compute an FFT on the data in sReal and sImag.
// Output is saved to out
void computeFFT(){
    //Compute the FFT
    FFT.Windowing(sReal, FFT_SIZE, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.Compute(sReal, sImag, FFT_SIZE, FFT_FORWARD);
    FFT.ComplexToMagnitude(sReal, sImag, FFT_SIZE);
    
    //double peak = FFT.MajorPeak(vReal, FFT_SIZE, SAMPLING_FREQUENCY);
    
    //Prepare the output data for transmission
    for(int i = 0; i < FFT_SIZE; i++){
      out[i] = sqrt((sReal[i]*sReal[i])+(sImag[i]*sImag[i]));
    }
   
}

//Transmit the output of the FFT as a byte array with a start of transmission packet: SOT
void transmit(){
    Serial.write(SOT,sizeof(SOT));
    Serial.write((byte*)&out, sizeof(float) * FFT_SIZE);
}

void loop() {
  //Wait until the side changes, then compute the FFT and transmit.
  if(sideLast != side){
    sideLast = side;
    populate();
    computeFFT();
    transmit();
  }
}

//This function is called by the interupt timer at a consistant interval.
void sample(){
  //Save the last sample to the buffer
  *bp = adc->readSingle();
  bp++;

  //Set the current side if needed.
  if(bp == &buff[FFT_SIZE]){
    side = 1;
  }

  //Loop back to the beginning
  if(bp == &buff[FFT_SIZE * 2]){
    bp = buff;
    side = 0;
  }

  //Start the ADC. This will return imediatly. The value will be saved next time the function runs. 
  adc->startSingleRead(A0, ADC_0);
}


// Timer functions for debugging
void timerStart(){
  timer = micros();
}
void timerEnd(){
  Serial.print("Timer : ");
  int t = micros() - timer;
  Serial.print(micros() - timer);
  Serial.print(" uS (");
  Serial.print(1000000.0/t);
  Serial.println("Hz)");
}
