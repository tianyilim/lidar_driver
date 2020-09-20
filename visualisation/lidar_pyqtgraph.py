from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSlot
import pyqtgraph as pg
import numpy as np
import time
import serial
import serial.tools.list_ports

np.random.seed(42)

class Worker(QRunnable):
    def __init__(self, main_class):
        super(Worker, self).__init__()
        self.ser = main_class.ser
        self.x_data = main_class.x_data
        self.y_data = main_class.y_data
        self.s1 = main_class.s1

    # @pyqtSlot()
    def run(self):
        while True:
            # num = int(self.ser.readline())
            num1 = np.random.random()
            num2 = np.random.random()

            self.x_data.append(num1)
            self.y_data.append(num2)

            self.s1.setData(x=self.x_data, y=self.y_data)
            time.sleep(0.01)

class mainApp():
    def __init__(self):
        # Setup windows
        app = QtGui.QApplication([])
        mw = QtGui.QMainWindow()
        mw.resize(800,800)
        view = pg.GraphicsLayoutWidget() 
        mw.setCentralWidget(view)
        w1 = view.addPlot()
        s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 200))
        w1.addItem(s1)

        # Setup serial
        s = [port.device for port in serial.tools.list_ports.comports()]
        self.ser = serial.Serial(s[1])

        self.s1 = s1
        self.mw = mw
        self.x_data=[]
        self.y_data=[]

        # Start worker thread to plot data
        self.threadpool = QThreadPool()
        worker = Worker(self)
        self.threadpool.start(worker) 

    def show(self):
        self.mw.show()
        QtGui.QApplication.instance().exec_()

bla = mainApp()
bla.show()