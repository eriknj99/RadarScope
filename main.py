import AsyncSerialInput
import SignalProcessor
import ModularScope
import numpy as np
import FrequencyCounter
import time
#ffts = np.array([np.zeros(1024)]) 
#ffts = np.append(ffts, [[1,2,3]], axis=0)
#ffts = np.append(ffts, [[9,8,7]], axis=0)
#print(ffts)
#print(np.shape(ffts))


#t = np.zeros(1024)
#print(np.shape(t))

#ffts = np.append(ffts, [t],axis=0)
#print(np.shape(ffts))

sp = SignalProcessor.SignalProcessor()

#fq = FrequencyCounter.FrequencyCounter()

#while(True):
#    fq.tick() 
#    time.sleep(.01)
#    print("Frequency: " + fq.getFreq() + "     ", end="\r")


#print(np.shape(sp.getRawFFT()))
graphics = True 

if(graphics):
    ms1 = ModularScope.ModularScope(sp)
    ms1.showFFT("fft1")
    ms1.showPeaks()
    ms1.splitV()
    ms1.showWaterfall("fft1")
    ms1.showConsole()
    ms1.show()



