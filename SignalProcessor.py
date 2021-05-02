import AsyncSerialInput
import FrequencyCounter
import numpy as np
import RadarSP


class SignalProcessor:
 
    # This function is called by AsyncSerialInput every time a new FFT is recieved. It stores the FFT and calls all signal processing functions 
    def FFTSync(self, FFT):
        self.fq.tick()
        self.real = self.ds.getReal()
        self.imag = self.ds.getImag()

        self.bufferInFFT(FFT);     
        self.bufferInPeak(self.computePeak(FFT))
        self.writeRawToFile()
        spData = RadarSP.SP(self.FFT_SIZE, self.SAMPLE_RATE, self.ffts, self.real, self.imag)
        self.range = spData[:1024]
        self.bufferInRanges(self.range)
        vel = spData[1024:]
        self.bufferInVels(vel)
        
    
    def writeMagToFile(self,FFT):
        line = ""
        for i  in FFT:
            line += str(i) + ","
        self.OUTPUT_FILE.write(line + "\n")

    def writeRawToFile(self):
        line = ""
        for i  in self.real:
            line += str(i) + ","
        self.OUTPUT_REAL.write(line + "\n")

        line = ""

        for i  in self.imag:
            line += str(i) + ","
        self.OUTPUT_IMAG.write(line + "\n")

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

    def __init__(self):
        self.OUTPUT_FILE = open("output.csv", "a")
        self.OUTPUT_REAL = open("real.csv", "a")
        self.OUTPUT_IMAG = open("imag.csv", "a")

        self.MAX_FFTS = 200
        self.MAX_PEAKS = 200
        self.MAX_RANGES = 500
        self.MAX_VELS = 500
        #self.numFFTs = 0

        self.ds = AsyncSerialInput.AsyncSerialInput(self)
        self.fq = FrequencyCounter.FrequencyCounter()

        self.peaks = np.array([])
        self.ranges = np.array(self.MAX_RANGES*[np.zeros(int(self.ds.getFFTSize()/2))])
        self.vels = np.array(self.MAX_VELS*[np.zeros(108)])
        self.ffts = np.array(self.MAX_FFTS*[np.zeros(self.ds.getFFTSize())])
        
        self.real = np.array([])
        self.imag = np.array([])

        self.FFT_SIZE = self.ds.getFFTSize()
        self.SAMPLE_RATE = self.ds.getSampleRate()

        #Wait until the first FFT packet becomes available
        self.ds.getNext()
    
        

