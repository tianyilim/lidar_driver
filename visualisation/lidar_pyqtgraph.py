from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

import pyqtgraph as pg
import numpy as np
import time
import serial
import serial.tools.list_ports

np.random.seed(42)

class Worker(QThread):
    signal = pyqtSignal(object)

    def __init__(self, main_class):
        super(Worker, self).__init__()

    def run(self):
        i = 0
        while True:
            num1 = np.random.random()
            num2 = np.random.random()
            self.signal.emit((num1, num2)) # Sends signal to mainApp
            time.sleep(0.001)
            i = i + 1

class mainApp():
    def __init__(self):
        # Setup windows
        app = QApplication([])
        mw = QMainWindow()
        mw.resize(500, 500)
        view = pg.GraphicsLayoutWidget() 
        mw.setCentralWidget(view)
        w1 = view.addPlot()
        s1 = pg.ScatterPlotItem(size=5, 
                                pen=pg.mkPen(None), 
                                brush=pg.mkBrush(255, 255, 255, 200))
        w1.addItem(s1)
        w1.enableAutoRange(enable=False)
        self.mw = mw
        self.s1 = s1
        self.data = [[],[]] # Stores x & y coordinates

        # Setup serial
        # s = [port.device for port in serial.tools.list_ports.comports()]
        # self.ser = serial.Serial(s[1])

        # Start worker thread to plot data
        worker = Worker(self)
        worker.signal.connect(self.grab_data)
        worker.start()

        # Show graph
        self.mw.show()
        QApplication.instance().exec_()

    def grab_data(self, data):
        num1, num2 = data
        # Do some truncation to limit the number of dots in our graph
        num1 = round(num1, 3)
        num2 = round(num2, 3)
        if not (num1 in self.data[0] and num2 in self.data[1]):
            self.data[0].append(num1)
            self.data[1].append(num2)
            self.s1.setData(x=self.data[0], y=self.data[1])
        print("length:" + str(len(self.data[0])) + 
              " x=" + str(num1) + " y=" + str(num2))

widget = mainApp()