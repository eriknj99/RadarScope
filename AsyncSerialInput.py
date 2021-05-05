import serial
import struct
import time
import threading
import time
import numpy as np
import math
import Logger
import DataManager

class AsyncSerialInput:
    #Serial Params
    serialPort = "/dev/ttyACM0"
    baudrate = 115200
    SOT = [0x02,0x03,0x04,0x05]

    def getFFTSize(self):
        return self.FFT_SIZE 
  
    def getSampleRate(self):
        return self.SAMPLE_RATE

    # This will wait until new data is recieved and return it when it is ready. Synchronous!
    def getNext(self):
        while(self.prevData == self.data):
            time.sleep(0)
        self.prevData = self.data
        return np.asarray(self.data)[:int(self.FFT_SIZE/2)]

    def getReal(self):
        return self.real

    def getImag(self):
        return self.imag

    # This is where you should access the recieved data. You can querry this function whenever you want. It will always be in sync.
    def getLast(self):
        return np.asarray(self.data)[:int(self.FFT_SIZE/2)]
  
    # Calculate the magnitude of the FFT given its real and imaginary components
    def getMagnitude(self,real, imag):
        mag = np.zeros(self.FFT_SIZE)
        for i in range(self.FFT_SIZE):
            mag[i] = math.sqrt((real[i]**2) + (imag[i]**2)) 
        return mag

    # Parse the input data for MODE1 + calculate and return the magnitude
    def parse(self, input):
        # Split the input array into real and imag components
        for i in range(self.FFT_SIZE):
            self.real[i] = input[i]
        for i in range(self.FFT_SIZE):
            self.imag[i] = input[self.FFT_SIZE + i]
        
        # Calculate the magnitude for compatability
        mag = getMagnitude(self.real, self.imag) 
        
        return mag    
    
    def calculateReplaySleepTime(self):
        return self.FFT_SIZE / self.SAMPLE_RATE

    def replay(self):
        Logger.info("Loading Replay Data...")
        # Read in the data 
        data = DataManager.readData("runaway")
        dreal = data[0,:]
        dimag = data[1,:]
       
        # Make sure the data is the correct length.
        # Removes the first column of zeros from old runs if present
        dreal = dreal[:,len(dreal[0])-self.FFT_SIZE:]
        dimag = dimag[:,len(dimag[0])-self.FFT_SIZE:]

        sleepTime = self.calculateReplaySleepTime()

        while(True):
            Logger.info("Replaying data...")
            for i in range(min(len(dreal),len(dimag))):
                self.real = dreal[i]
                self.imag = dimag[i]
                mag = self.getMagnitude(self.real, self.imag)
                self.data = mag
                self.sp.FFTSync(mag, self.real, self.imag)
                time.sleep(sleepTime)
                


    def recieve(self):
        try:
            ser = serial.Serial(self.serialPort, self.baudrate)
        except:
            print("Unable to connect to serial port:" + self.serialPort + "@" + str(self.baudrate))

        while True:
            # Wait until the SOT sequence is recieved
            ready = False
            buf = [0x00,0x00,0x00,0x00]
            while not ready:
                for i in range(len(self.SOT) - 1):
                    buf[i] = buf[i+1]
                
                buf[len(self.SOT) - 1] = struct.unpack('b',ser.read())[0]
                if(buf == self.SOT):
                        ready = True


            # Recieve the data. SAMPLES * 4 bytes : SAMPLES floats
            raw = ser.read(4 * self.PACKET_SIZE) 
            f = struct.unpack('%sf' % self.PACKET_SIZE, raw)

            # Set the data variable to the recieved data.
            if(self.MODE == 0):    
                self.data = f
            if(self.MODE == 1):
                self.data = self.parse(f)

            #self.sp.FFTSync(self.data)

    def __init__(self, sp, replay=False):

        self.sp = sp

        self.data = []
        
        self.prevData = []
        
        self.MODE = 1
        self.SAMPLE_RATE = 50000
        self.FFT_SIZE  = 2048
        if(self.MODE == 0):
            self.PACKET_SIZE = self.FFT_SIZE 
        if(self.MODE == 1):
            self.PACKET_SIZE = self.FFT_SIZE * 2 


        self.real = np.zeros(self.FFT_SIZE)
        self.imag = np.zeros(self.FFT_SIZE)

        if(replay):
            self.x = threading.Thread(target=self.replay)
        else:
            self.x = threading.Thread(target=self.recieve)
        
        self.x.start()



