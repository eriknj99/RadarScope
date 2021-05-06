import DataManager
import AsyncSerialInput
import SignalProcessor
import ModularScope
import Logger
import numpy as np
#import FrequencyCounter
import time
import sys
import signal
import subprocess
import os

FFT_SIZE = 2048
SAMPLE_RATE = 50000

save = False
saveFilePrefix = ""

replay = False
replayFilePrefix = ""

video = False

#Arg parse
if(len(sys.argv) > 1):
    for i in range(1,len(sys.argv)):
        if(sys.argv[i] == "--replay"):
            if(len(sys.argv) > i+1):
                replay = True
                replayFilePrefix = sys.argv[i+1]
                i+=1
                Logger.info("Replaying dataset: \'" + replayFilePrefix + "\'")
            else:
                Logger.error("You must specify a replay file prefix")
        if(sys.argv[i] == "--video"):
            video = True
        if(sys.argv[i] == "--save"):
            if(len(sys.argv) > i+1):
                save = True
                saveFilePrefix = sys.argv[i+1]
                i+=1
                Logger.info("Saving dataset: \'" + saveFilePrefix+ "\'")
            else:
                Logger.error("You must specify a save file prefix")



signalProcessor = SignalProcessor.SignalProcessor(FFT_SIZE, SAMPLE_RATE)
dataInput = AsyncSerialInput.AsyncSerialInput(signalProcessor, FFT_SIZE, SAMPLE_RATE, replay=replay, replayFilePrefix=replayFilePrefix, save=save, saveFilePrefix=saveFilePrefix)

# Wait until the signal processor recieves it's first packet before starting the GUI
while(not signalProcessor.data_stream_started):
    time.sleep(0)

if(video and replay):
   vfile = replayFilePrefix+".mp4"
   Logger.info("Playing video file: " + vfile)
   subprocess.Popen(["./vids/play.sh", "./vids/" + vfile])
#   os.spawnl(os.NOWAIT, "./vids/play.sh ./vids/"+vfile) i

signal.signal(signal.SIGINT, signal.SIG_DFL)
ms1 = ModularScope.ModularScope(signalProcessor)
#ms1.showFFT("fft")
#ms1.showPeaks()
#ms1.splitV()
#ms1.showFFTWaterfall("fft")
#ms1.showConsole()
ms1.showRangeWaterfall("fft")
ms1.show()


def signal_handler(sig, frame):
    print("")
    Logger.info("Cleaning up...")
    signalProcessor.cleanup()
    dataInput.cleanup()
    Logger.info("Goodbye.")
    # This will cause a thread exception. I don't care so dont print anything.
    try:
        sys.exit(0)
    except:
        pass

signal.signal(signal.SIGINT, signal_handler)

