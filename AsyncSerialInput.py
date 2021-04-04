import serial
import struct
import time
import threading
import time
import numpy as np

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


    # This is where you should access the recieved data. You can querry this function whenever you want. It will always be in sync.
    def getLast(self):
        return np.asarray(self.data)[:int(self.FFT_SIZE/2)]

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
            raw = ser.read(4 * self.FFT_SIZE) 
            f = struct.unpack('%sf' % self.FFT_SIZE, raw)

            # Set the data variable to the recieved data.
            self.data = f
            self.sp.FFTSync(f)

    def __init__(self, sp):

        self.sp = sp

        self.data = []
        self.prevData = []
        
        self.SAMPLE_RATE = 1000
        self.FFT_SIZE  = 1024
        
        self.x = threading.Thread(target=self.recieve)
        self.x.start()



