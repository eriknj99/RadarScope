import AsyncSerialInput
import SignalProcessor
import ModularScope
import numpy as np
import FrequencyCounter
import time


sp = SignalProcessor.SignalProcessor()

ms1 = ModularScope.ModularScope(sp)
#ms1.showFFT("fft")
#ms1.splitV()
#ms1.showVelWaterfall("fft")
ms1.showRangeWaterfall("fft")
ms1.show()



