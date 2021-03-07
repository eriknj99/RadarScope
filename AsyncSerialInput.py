import serial
import struct
import time
import threading
import numpy as np

class AsyncSerialInput:
    #Serial Params
    serialPort = "/dev/ttyACM0"
    baudRate = 115200
    SOT = [0x02,0x03,0x04,0x05]

    #FFT Params
    SAMPLES = 1024

    # This is where you should access the recieved data. You can querry this function whenever you want. It will always be in sync.
    def getLast(self):
        return np.asarray(self.data)[:int(self.SAMPLES)]

    def recieve(self):
        try:
            ser = serial.Serial(self.serialPort, self.baudRate)
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
            raw = ser.read(4 * self.SAMPLES) 
            f = struct.unpack('%sf' % self.SAMPLES, raw)

            # Set the data variable to the recieved data.
            self.data = f

    def __init__(self):
        self.data = []
        x = threading.Thread(target=self.recieve)
        x.start()



