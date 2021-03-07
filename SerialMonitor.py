import serial
import struct
import time


#Serial Params
serialPort = "/dev/ttyACM0"
baudRate = 115200

#FFT Params
SOT = [0x02,0x03,0x04,0x05]
SAMPLES = 1024 
try:
    ser = serial.Serial(serialPort, 115200)
except:
    print("Unable to connect to serial port:" + serialPort + "@" + str(baudrate))


def printFloats():
    raw = ser.read(4)

    f = struct.unpack('f', raw)
    print(f[0])

def printStrings():
    raw = ser.readline()
    print(str(raw))

avgFreq = 0
while True:

   start = time.time()
   ready = False
   buf = [0x00,0x00,0x00,0x00]
   while not ready:
       for i in range(len(SOT) - 1):
           buf[i] = buf[i+1]
       buf[len(SOT) - 1] = struct.unpack('b',ser.read())[0]
       if(buf == SOT):
            ready = True

   raw = ser.read(4 * SAMPLES) 
 
   f = struct.unpack('%sf' % SAMPLES, raw)

   elapsed = (time.time() - start)
   avgFreq = (avgFreq + (1/1000*elapsed)) / 2

   if(len(f)!=SAMPLES):
         print("X", end="\n", flush=True)
   else:
         print("Packet Revieve Rate:" + str(1.0/elapsed) + "Hz            ", end="\r", flush=True)
   
