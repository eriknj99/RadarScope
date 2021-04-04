import PyQt5
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import time
import sys
import SignalProcessor
import FrequencyCounter

class ModularScope():

    def dataFetchLoop(self):
        self.FFT = self.sp.getFFT()
        self.PEAKS = self.sp.getPeaks()
        self.fq.tick()
    
    def splitV(self):
        self.win.nextRow()

    def splitH(self):
        self.win.nextCol()

    def showPeaks(self):
        pp = self.win.addPlot(title="Peaks", name="Peaks",colspan=5)
        pp.showGrid(x=True,y=True)
        curve = pp.plot(pen='r')
        curve.setData(self.PEAKS)
        pp.enableAutoRange('xy', True)

        def update():
            curve.setData(self.PEAKS)

        self.plots.append(pp)
        self.mainTmr.timeout.connect(update)

    def showConsole(self):
        view = self.win.addViewBox(enableMouse=False,border="w",colspan=5)
        view.autoRange()
        pp = pg.TextItem(text="hello world\nLine 2", color=(0,255,0))
        pp.setPos(.01, .99)
        pp.setFont(QtGui.QFont("",16))
        view.addItem(pp)

        def update():
            pp.setText(
                     "\nSync Rate : " + self.sp.getSyncRate() + 
                     "\nFrame Rate: " + self.fq.getFreq() +
                     "\nPeak      : " + str(self.PEAKS[np.size(self.PEAKS) - 1]) + 
                     "\n----------" +
                     "\nVelocity  : ??? m/s"+
                     "\nRange     : ??? m"
            )

        self.consoleTmr.timeout.connect(update)

    def showFFT(self, name):
        # Graph the FFT 
        pfft = self.win.addPlot(title="FFT", name=name,colspan=20)
        pfft.autoRange()
        #pfft.setMinimumSize(500,100)
        lpeak = pg.InfiniteLine(pos=100, angle=90,pen='r')
        pfft.addItem(lpeak)
        pfft.showGrid(x=True, y=True)
        curve = pfft.plot(pen='g')
        global ptr
        ptr = 0
        curve.setData(self.FFT[1], self.FFT[0])
        pfft.enableAutoRange('xy', True)

        def update():
            global ptr
            peak = self.FFT[1][np.argmax(self.FFT[0])]
            lpeak.setPos(peak)
            curve.setData(self.FFT[1], self.FFT[0])
            if(ptr > 5): 
                pfft.enableAutoRange('xy', False)
            ptr += 1

        self.plots.append(pfft)
        self.mainTmr.timeout.connect(update)
    
    def showWaterfall(self,name):
        
        view = pg.PlotItem(invertY=True)
        view.setLabel(axis='left', text='')
        view.setLabel(axis='bottom', text='Frequency')
        view.showGrid(x=True, y=True)

        self.win.addItem(view, colspan=20)
        
        img = pg.ImageItem(border='w')
        pos = np.array([0., 1., 0.5, 0.25, 0.75])
        color = np.array([[0,255,255,0], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
        cmap = pg.ColorMap(pos, color)
        lut = cmap.getLookupTable(0.0, 1.0, 10000)
        img.setLevels([0,10000])
        img.setLookupTable(lut)

        img.translate(0,-500)

        view.addItem(img)
        view.setAutoVisible(x=True, y=True)
        ## Set initial view bounds
        view.setRange(QtCore.QRectF(0, 0, 600, 600))
        view.setXLink(name)
        
        global data   
        data = np.zeros((1, np.shape(self.FFT)[1], 500))

        def update():
            global data
            view.setYRange(0,-500)
            data = np.insert(data, -1, np.sqrt(self.FFT[0]), axis=2)
            data = np.delete(data, 0,2)
            img.setImage(data[0],autoLevels=False)
        
        self.mainTmr.timeout.connect(update)


    def show(self):
        QtGui.QApplication.instance().exec_()

    def __init__(self, sigproc):
        self.sp = sigproc 
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsLayoutWidget(show=True, title="RadarScope")
        self.win.resize(1000,600)
        self.win.setWindowTitle('RadarScope v2')
        pg.setConfigOptions(antialias=True)
       
        self.fq = FrequencyCounter.FrequencyCounter()

        self.mainTmr = QtCore.QTimer()
        self.mainTmr.timeout.connect(self.dataFetchLoop)
        self.mainTmr.start(20)
       
        self.consoleTmr = QtCore.QTimer()
        self.consoleTmr.start(100) 

        self.rawFFT = self.sp.getRawFFT()
        self.FFT = self.sp.getFFT()
        self.PEAKS = self.sp.getPeaks()

        self.plots = []

        
 
        
        




## Start Qt event loop unless running in interactive mode or using pyside.
#if __name__ == '__main__':
#    import sys
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()




