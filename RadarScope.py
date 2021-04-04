import PyQt5
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import SignalProcessor



def dataFetchLoop():
    global last_data 
    last_data = sp.getRawFFT()

# Initialize the Serial Input
sp = SignalProcessor.SignalProcessor()
# Setup the window
app = QtGui.QApplication([])
win = pg.GraphicsLayoutWidget(show=True, title="floatme")
win.resize(1000,600)
win.setWindowTitle('RadarScope v2')
pg.setConfigOptions(antialias=True)

mainTmr = QtCore.QTimer()
mainTmr.timeout.connect(dataFetchLoop)
mainTmr.start(20)

def showFFT(win, mainTmr):
    # Graph the FFT 
    pfft = win.addPlot(title="Raw FFT", name="Plot1")
    lpeak = pg.InfiniteLine(pos=100, angle=90,pen='r')
    pfft.addItem(lpeak)
    pfft.showGrid(x=True, y=True)
    curve = pfft.plot(pen='g')
    ptr = 0
    pfft.enableAutoRange('xy', True)
    curve.setData(last_data)
        
    def update():
        peak = np.argmax(last_data)
        lpeak.setPos(peak)
        curve.setData(last_data)

        pfft.enableAutoRange('xy', False)

    mainTmr.timeout.connect(update)

#showFFT(win, mainTmr)
print(last_data)
## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

exit(0)

win.nextRow()

# Graph the waterfall diaplay

#view = pg.ViewBox()
view = pg.PlotItem(invertY=True)
view.setLabel(axis='left', text='')
view.setLabel(axis='bottom', text='Frequency')
view.setXRange(5, 20)
view.showGrid(x=True, y=True)


win.addItem(view)

img = pg.ImageItem(border='w')
pos = np.array([0., 1., 0.5, 0.25, 0.75])
color = np.array([[0,255,255,0], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
cmap = pg.ColorMap(pos, color)
lut = cmap.getLookupTable(0.0, 1.0, 10000)
img.setLevels([0,10000])
img.setLookupTable(lut)


view.addItem(img)
view.setAutoVisible(x=True, y=True)
## Set initial view bounds
view.setRange(QtCore.QRectF(0, 0, 600, 600))
view.setXLink('Plot1')
data = np.zeros((1, 1024, 500))
i = 0

updateTime = ptime.time()
fps = 0

img.translate(0,-500)

def updateWaterfall():
    global img, data, updateTime, fps 
    view.setYRange(0,-300) 
    data = np.insert(data, -1, np.sqrt(last_data), axis=2)
    data = np.delete(data, 0,2)
    img.setImage(data[0],autoLevels=False)
    #img.setRect(QtCore.QRect(0,0,4,4))
    QtCore.QTimer.singleShot(20, updateWaterfall)
    now = ptime.time()
    fps2 = 1.0 / (now-updateTime)
    updateTime = now
    fps = fps * 0.9 + fps2 * 0.1
    
    #print "%0.1f fps" % fps
    

updateWaterfall()




