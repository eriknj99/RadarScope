import PyQt5
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import time
import sys
import SignalProcessor
import FrequencyCounter
import Logger

class ModularScope():

    def frameRateUpdate(self):
        self.fq.tick()
    
    def splitV(self):
        self.win.nextRow()

    def splitH(self):
        self.win.nextCol()

    
    def showConsole(self):
        view = self.win.addViewBox(enableMouse=False,border="w",colspan=5)
        view.autoRange()
        pp = pg.TextItem(text="hello world\nLine 2", color=(0,255,0))
        pp.setPos(.01, .99)
        pp.setFont(QtGui.QFont("",16))
        view.addItem(pp)

        def update():
            pp.setText("Homebrew Radar\n" + 
                     "\nSync Rate : " + self.sp.getSyncRate() + 
                     "\nFrame Rate: " + self.fq.getFreq() +
                     "\nPeak      : " + str(self.PEAKS[0])) 

        self.consoleTmr.timeout.connect(update)
    def showPeaks(self):
        pp = self.win.addPlot(title="Peaks", name="Peaks",colspan=5)
        pp.showGrid(x=True,y=True)
        curve = pp.plot(pen='r')
        curve.setData(self.sp.getPeaks())
        pp.enableAutoRange('xy', True)

        def update():
            curve.setData(self.sp.getPeaks())

        self.plots.append(pp)
        self.mainTmr.timeout.connect(update)

    def showFFT(self, name):
        # Graph the FFT 
        pfft = self.win.addPlot(title="FFT", name=name,colspan=20)
        pfft.autoRange()
        lpeak = pg.InfiniteLine(pos=100, angle=90,pen='r')
        pfft.addItem(lpeak)
        pfft.showGrid(x=True, y=True)
        curve = pfft.plot(pen='g')
        global ptr
        ptr = 0
        curve.setData(self.sp.getFFT()[1], self.sp.getFFT()[0])
        pfft.enableAutoRange('xy', True)

        def update():
            global ptr
            FFT = self.sp.getFFT()
            peak = FFT[1][5+np.argmax(FFT[0][5:int(self.sp.FFT_SIZE/2)])]
            lpeak.setPos(peak)
            curve.setData(FFT[1], FFT[0])
            if(ptr > 5): 
                pfft.enableAutoRange('xy', False)
            
            ptr += 1

        self.plots.append(pfft)
        self.mainTmr.timeout.connect(update)
  
  
    def showRangeWaterfall(self, name):

        C = 3e8
        B = 100e6
        T = 8.7177e-3

        view = pg.PlotItem(invertY=True)
        view.showGrid(x=True,y=True)
        self.win.addItem(view, colspan=20)
        img = pg.ImageItem(border='w')
        #pos = np.flip(np.array([0.,  5, 0.75, 0.9, 1]))
        #color =(np.array([[255,0,0,255], [255, 165, 0, 255], [255,255,0,0], [0, 255, 0, 0],[0,0,255,0]], dtype=np.ubyte))
        #pos = np.array([0., .6, 0.8, 0.9, 1])
        #color = np.array([[0,0,128,128], [0, 0, 255, 255], [0,255,0,255], [0, 255, 0, 255],[255,255,0,255]], dtype=np.ubyte)

        histogram = pg.HistogramLUTItem()
        histogram.setImageItem(img)
        histogram.setHistogramRange(0,100)
        histogram.gradient.restoreState({'ticks': [(0.3333, (0, 255, 255, 255)), (0.6666, (255, 255, 0, 255)), (1, (0, 255, 0, 255)), (0, (64, 64, 255, 64))], 'mode': 'rgb'})
        histogram.setFixedWidth(128)
        self.win.addItem(histogram)
        
        img.translate(0,-self.sp.MAX_RANGES)
        view.addItem(img)
        img.setImage(np.rot90(np.rot90(np.rot90(self.sp.getRanges()))),autoLevels=False)
        #view.setXLink(name)
        img.scale(((self.sp.SAMPLE_RATE/self.sp.FFT_SIZE) * C * T) / (4*B),1)
        
        def update():
            #img.setImage(np.flip(np.rot90(self.sp.ffts))[:int(self.sp.FFT_SIZE/2)], autoLevels=False)
            img.setImage(np.rot90(np.rot90(np.rot90(self.sp.getRanges()))),autoLevels=False)
        self.mainTmr.timeout.connect(update)
    
    def showVelWaterfall(self, name):
        C = 3e8
        B = 100e6
        T = 8.7177e-3

        view = pg.PlotItem(invertY=True)
        view.showGrid(x=True,y=True)
        self.win.addItem(view, colspan=20)
        img = pg.ImageItem(border='w')
        #pos = np.flip(np.array([0.,  5, 0.75, 0.9, 1]))
        #color =(np.array([[255,0,0,255], [255, 165, 0, 255], [255,255,0,0], [0, 255, 0, 0],[0,0,255,0]], dtype=np.ubyte))
        
        histogram = pg.HistogramLUTItem()
        histogram.setImageItem(img)
        #histogram.setHistogramRange(0,100)
        histogram.gradient.restoreState({'ticks': [(0.3333, (0, 255, 255, 255)), (0.6666, (255, 255, 0, 255)), (1, (0, 255, 0, 255)), (0, (64, 64, 255, 64))], 'mode': 'rgb'})
        histogram.setFixedWidth(128)
        self.win.addItem(histogram)

        img.translate(0,-self.sp.MAX_VELS)
        view.addItem(img)
        img.setImage(np.rot90(np.rot90(np.rot90(self.sp.getVels()))),autoLevels=False)
        #view.setXLink(name)
        img.scale((10/108),1)
        
        def update():
            #img.setImage(np.flip(np.rot90(self.sp.ffts))[:int(self.sp.FFT_SIZE/2)], autoLevels=False)
            img.setImage(np.rot90(np.rot90(np.rot90(self.sp.getVels()))),autoLevels=False)
        self.mainTmr.timeout.connect(update)


    def showFFTWaterfall(self, name):
        view = pg.PlotItem(invertY=True)
        view.showGrid(x=True,y=True)
        self.win.addItem(view, colspan=20)
        img = pg.ImageItem(border='w')

        histogram = pg.HistogramLUTItem()
        histogram.setImageItem(img)
        #histogram.setHistogramRange(0,100)
        histogram.gradient.restoreState({'ticks': [(0.3333, (0, 255, 255, 255)), (0.6666, (255, 255, 0, 255)), (1, (0, 255, 0, 255)), (0, (64, 64, 255, 64))], 'mode': 'rgb'})
        histogram.setFixedWidth(128)
        self.win.addItem(histogram)

        
        img.translate(0,-self.sp.MAX_FFTS)
        view.addItem(img)
        img.setImage(np.rot90(self.sp.ffts[:int(self.sp.FFT_SIZE/2)]))
        view.setXLink(name)
        img.scale(self.sp.SAMPLE_RATE/self.sp.FFT_SIZE,1)
        
        def update():
            img.setImage(np.flip(np.rot90(self.sp.ffts))[:int(self.sp.FFT_SIZE/2)], autoLevels=False)
            
        self.mainTmr.timeout.connect(update)


    def show(self):
        QtGui.QApplication.instance().exec_()

    def cleanup(self):
        self.app.quit()

    def __init__(self, sigproc):
        self.sp = sigproc 
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True, title="RadarScope")
        self.win.resize(1000,600)
        self.win.setWindowTitle('RadarScope v2')
        pg.setConfigOptions(antialias=True)
       
        self.fq = FrequencyCounter.FrequencyCounter()

        self.mainTmr = QtCore.QTimer()
        self.mainTmr.timeout.connect(self.frameRateUpdate)
        self.mainTmr.start(20)
       
        self.consoleTmr = QtCore.QTimer()
        self.consoleTmr.start(100) 

        self.rawFFT = self.sp.getHalfBinVals()
        self.FFT = self.sp.getFFT()
        self.PEAKS = self.sp.getPeaks()

        self.plots = []

## Start Qt event loop unless running in interactive mode or using pyside.
#if __name__ == '__main__':
#    import sys
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()




