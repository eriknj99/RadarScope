import threading
import numpy as np
import time 
import math

import FrequencyCounter
import RadarSP
import Logger

class SignalProcessor:
 
    # This function is called by AsyncSerialInput every time a new FFT is recieved. It stores the FFT and unblocks the signal processor  
    def FFTSync(self, real, imag):
        self.fq.tick()
        self.real = real 
        self.imag = imag 
        
        self.data_stream_started = True # Unblock the GUI
        self.new_data = True # Unblock Signal Processor


    # Perform all signal processing every time new data becomes available.
    # The time this function takes to execute must be shorter than the time between recieved packets!
    def run(self):

        while(True):
            # Wait until new data is recieved while checking if the thread has been stopped 
            while(not self.new_data):
                if(self.stop_thread):
                   return 
                time.sleep(0)
           
            self.new_data = False # Block the signal processor until the next new data set is recieved
            self.mag = self.getMagnitude(self.real, self.imag)
            self.bufferInFFT(self.mag)
            self.bufferInPeak(self.computePeak(self.mag))
            
            spData = RadarSP.SP(self.FFT_SIZE, self.SAMPLE_RATE, self.ffts, self.real, self.imag)
            range = spData[:1024]
            self.bufferInRanges(range)
            vel = spData[1024:]
            self.bufferInVels(vel)

    # Buffer peak into peaks without exceding MAX_PEAKS elements
    def bufferInPeak(self,peak):
        if(np.size(self.peaks) < self.MAX_PEAKS):
            self.peaks = np.append(peak, self.peaks)
        else:
            self.peaks = np.roll(self.peaks, 1)
            self.peaks[0] = peak

    # Buffer the FFT into ffts without exceding MAX_FFTS elements
    def bufferInFFT(self,FFT):
        if(np.shape(self.ffts)[0] < self.MAX_FFTS):
            self.ffts = np.append(self.ffts,[FFT],axis=0)
        else:
            self.ffts = np.roll(self.ffts,1,axis=0)
            self.ffts[0] = FFT

    # Buffer the range into ranges without exceding MAX_FFTS elements
    def bufferInRanges(self,range):
        if(np.shape(self.ranges)[0] < self.MAX_RANGES):
            self.ranges = np.append(self.ranges,[range],axis=0)
        else:
            self.ranges = np.roll(self.ranges,1,axis=0)
            self.ranges[0] = range
    
    # Buffer the vel into vels without exceding MAX_VELS elements
    def bufferInVels(self,vel):
        if(np.shape(self.vels)[0] < self.MAX_VELS):
            self.vels = np.append(self.vels,[vel],axis=0)
        else:
            self.vels = np.roll(self.vels,1,axis=0)
            self.vels[0] = vel


    # Calculate the magnitude of the FFT given its real and imaginary components
    def getMagnitude(self,real, imag):
        mag = np.zeros(self.FFT_SIZE)
        for i in range(self.FFT_SIZE):
            mag[i] = math.sqrt((real[i]**2) + (imag[i]**2)) 
        return mag
    
    # Returns the last recieved FFT packet
    def getHalfBinVals(self):
        return self.ffts[0][:int(self.FFT_SIZE/2)]

    # Calculates the frequency values of the FFT bins based on FFT_SIZE and SAMPLE_RATE
    def getFrequencies(self):
        out = np.zeros(int(self.FFT_SIZE/2))

        for i in range(0,int(self.FFT_SIZE/2)):
            out[i] = i * (self.SAMPLE_RATE / self.FFT_SIZE)     
        
        return out

    # Returns the frequency corresponding to a bin based on SAMPLE_RATE and FFT_SIZE
    def binToFreq(self,bin):
        return bin * (self.SAMPLE_RATE / self.FFT_SIZE) 
    
    # Get a 2D array of the last recieved FFT and its corresponding frequency values
    def getFFT(self):
        out =  np.array([(self.getHalfBinVals()), (self.getFrequencies())], dtype=float)
        return out
    def computeRanges(self):
        C = 3e8
        B = 100e6
        T = 8.7177e-3
        return self.getPeaks() * ((C * T) / (4*B))

    def getRanges(self):
        return self.ranges

    def getVels(self):
        return self.vels

    # Appends the frequency of the peak to self.peaks for a single FFT entry 
    def computePeak(self, FFT):
        return self.binToFreq(5+np.argmax(FFT[5:int(self.FFT_SIZE/2)])) 
    
    # Get a 1D array of all calculated peaks
    def getPeaks(self):
        return self.peaks

    def getSyncRate(self):
        return self.fq.getFreq()

    def cleanup(self):
        self.stop_thread = True
        self.spThread.join()

    def __init__(self, fftSize, sampleRate):
        self.MAX_FFTS = 200
        self.MAX_PEAKS = 200
        self.MAX_RANGES = 500
        self.MAX_VELS = 500
       
        self.FFT_SIZE = fftSize 
        self.SAMPLE_RATE = sampleRate 
        
        self.fq = FrequencyCounter.FrequencyCounter()

        self.peaks = np.array([])
        self.ranges = np.array(self.MAX_RANGES*[np.zeros(int(self.FFT_SIZE/2))])
        self.vels = np.array(self.MAX_VELS*[np.zeros(108)])
        self.ffts = np.array(self.MAX_FFTS*[np.zeros(self.FFT_SIZE)])
        
        self.real = np.array([])
        self.imag = np.array([])
        self.mag = np.array([])

        self.data_stream_started = False
        self.new_data = False
        
        self.stop_thread = False
        self.spThread = threading.Thread(target=self.run)
        self.spThread.start()

 
    
        

