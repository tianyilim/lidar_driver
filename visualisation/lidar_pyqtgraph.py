from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import time

np.random.seed(42)

class mainApp():
    def __init__(self):
        app = QtGui.QApplication([])
        mw = QtGui.QMainWindow()
        mw.resize(800,800)
        view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
        mw.setCentralWidget(view)

        w1 = view.addPlot()

        np.random.seed(42)
        n = 10
        s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 200))
        w1.addItem(s1)

        self.s1 = s1
        self.mw = mw
        self.x_data=[]
        self.y_data=[]

    def addPoint(self):
        self.x_data.append(np.random.random())
        self.y_data.append(np.random.random())
        self.s1.setData(x=self.x_data, y=self.y_data)

    def show(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.addPoint)
        timer.start(10) # Timeout in milliseconds
        self.mw.show()
        QtGui.QApplication.instance().exec_()

bla = mainApp()
bla.show()