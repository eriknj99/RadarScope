import DataManager
import AsyncSerialInput
import SignalProcessor
import ModularScope
import numpy as np
#import FrequencyCounter
import time

FFT_SIZE = 2048
SAMPLE_RATE = 50000

sp = SignalProcessor.SignalProcessor(FFT_SIZE, SAMPLE_RATE)
asy = AsyncSerialInput.AsyncSerialInput(sp, True)

while(not sp.new_data):
    time.sleep(0)

ms1 = ModularScope.ModularScope(sp)
ms1.showFFT("fft")
#ms1.splitV()
#ms1.showVelWaterfall("fft")
ms1.showRangeWaterfall("fft")
ms1.show()



