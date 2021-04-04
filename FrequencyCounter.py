import time
from sigfig import round

class FrequencyCounter():

    def tick(self):
        self.duration = time.time() - self.timestamp 
        self.timestamp = time.time()

    def getFreq(self, dec=3):
        freq = round(1.0 / self.duration,decimals=dec)
        return str(freq) + "Hz"

    
    def __init__(self):
        self.timestamp = time.time() 
        self.duration = 0
