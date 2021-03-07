#include "arduinoFFT.h"
#define SAMPLES 1024            //The number of FFT bins. Must be a power of 2
int SAMPLING_FREQUENCY = 1000;  //Hz, must be less than 62500 due to ADC


arduinoFFT FFT = arduinoFFT();

unsigned int sampling_period_us;
unsigned long microseconds;


double sReal[SAMPLES];
double sImag[SAMPLES];

double vReal[SAMPLES];
double vImag[SAMPLES];

byte SOT[] = {0x02, 0x03, 0x04, 0x05};

float out[SAMPLES];

int timer;

void setup() {
    // Enable serial and set the baud rate
    Serial.begin(115200);

    // Calculate the sampling period from the desired SAMPLING_FREQUENCY
    sampling_period_us = round(1000000*(1.0/SAMPLING_FREQUENCY));

    // Perform one full sample to populate the sample arrays
    fullSample();
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
  Serial.print(100000.0/t);
  Serial.println("Hz)");
}

void fullSample(){
   for(int i=0; i<SAMPLES; i++)
    {
        microseconds = micros();   
     
        sReal[i] = analogRead(A0);
        sImag[i] = 0;

        //  Delay with microsecond accuracy.
        while(micros() < (microseconds + sampling_period_us)){}
    }
}
//Perform a single sample and add it to the end of the sampled data. This can be used to compute one FFT per sample
void singleSample(){
   //Wait until its time to sample
   while(micros() < (microseconds + sampling_period_us)){}
   //Save the time of the sample
   microseconds = micros();
   
   //Sample the analog pin
   double sample = analogRead(A0);
   
   //Shift the data in the sample array
   for(int i = 0; i < SAMPLES - 1; i++){
    sReal[i] = sReal[i+1];
    sImag[i] = 0;
   }
   //Add the sample to the sample array 
   sReal[SAMPLES - 1] = sample;
   sImag[SAMPLES - 1] = 0;
}
// Perform n samples and add it to the end of the sampled data. This can be used to compute on FFT per n samples
// TODO: Make this function more efficent.
void multiSample(int n){
   for(int i = 0; i < n; i++){
      singleSample();
   }
}
// Compute an FFT on the data in sReal and sImag. The data is copied to vReal and vImag before processing to preserve the sampled data.
//Output is saved to out
void computeFFT(){
    // Copy the values of the sampled data to the arrays that will be worked on
    for(int i = 0; i < SAMPLES; i++){
      vReal[i] = sReal[i];
      vImag[i] = sImag[i];
    }
    
    //Compute the FFT
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
    
    //double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
    
    //Prepare the output data for transmission
    for(int i = 0; i < SAMPLES; i++){
      out[i] = sqrt(vReal[i]*vReal[i])+(vImag[i]*vImag[i]);
      //out[i] = i*i;
    }
   
}

//Transmit the output of the FFT as a byte array with a start of transmission packet: SOT
void transmit(){
    Serial.write(SOT,sizeof(SOT));
    Serial.write((byte*)&out, sizeof(float) * SAMPLES);
}

void loop() {
  //16 samples per FFT results in a ~60Hz output rate. 
  multiSample(16);
  computeFFT();
  transmit();
}
