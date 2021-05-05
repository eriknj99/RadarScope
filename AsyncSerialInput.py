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
    # TODO: Make these optional instance variables
    serialPort = "/dev/ttyACM0"
    baudrate = 115200
    SOT = [0x02,0x03,0x04,0x05]

    def getFFTSize(self):
        return self.FFT_SIZE 
  
    def getSampleRate(self):
        return self.SAMPLE_RATE

    
    # Parse the input data for MODE1 + calculate and return the magnitude
    def parse(self, input):
        # Split the input array into real and imag components
        for i in range(self.FFT_SIZE):
            self.real[i] = input[i]
        for i in range(self.FFT_SIZE):
            self.imag[i] = input[self.FFT_SIZE + i]
    
    def calculateReplaySleepTime(self):
        return self.FFT_SIZE / self.SAMPLE_RATE

    def replayDataset(self):
        Logger.info("Loading replay dataset...")
        # Read in the data 
        data = self.dataManager.readData()
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
                # Check is the thread was stopped
                if(self.stop_thread):
                   return
                    
                self.real = dreal[i]
                self.imag = dimag[i]

                self.sp.FFTSync(self.real, self.imag)
                time.sleep(sleepTime)

    def recieveSerial(self):
        try:
            ser = serial.Serial(self.serialPort, self.baudrate)
        except:
            Logger.error("Unable to connect to serial port:" + self.serialPort + "@" + str(self.baudrate))
            return  

        while True:
            # Check is the thread was stopped
            if(self.stop_thread):
                return 

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
                Logger.error("MODE 0 is no longer supported. Please switch to MODE 1...")
            if(self.MODE == 1):
                self.parse(f)

            # Save the data if enabled 
            if(self.save):
               self.dataManager.writeData(self.real, self.imag)

            self.sp.FFTSync(self.real, self.imag)

    def cleanup(self):
       self.stop_thread = True
       self.dataThread.join() 

    def __init__(self, sp, FFT_SIZE, SAMPLE_RATE, replay=False, replayFilePrefix="", save=False, saveFilePrefix=""):

        self.sp = sp
        self.mag = []
        self.prevMag = []

        self.replay = replay
        self.replayFilePrefix = replayFilePrefix
        self.save = save
        self.saveFilePrefix = saveFilePrefix

        self.stop_thread = False
        

        if(save):
            self.dataManager = DataManager.DataManager(self.saveFilePrefix)   
            self.dataManager.initFiles()
        if(replay):
            self.dataManager = DataManager.DataManager(self.replayFilePrefix)   

        self.MODE = 1 # DEPRICATED: The signal processor no longer handles MODE 0
        
        self.SAMPLE_RATE = SAMPLE_RATE
        self.FFT_SIZE  = FFT_SIZE 
        self.PACKET_SIZE = self.FFT_SIZE * 2 


        self.real = np.zeros(self.FFT_SIZE)
        self.imag = np.zeros(self.FFT_SIZE)

        if(replay):
            self.dataThread = threading.Thread(target=self.replayDataset)
        else:
            self.dataThread = threading.Thread(target=self.recieveSerial)
        
        self.dataThread.start()



