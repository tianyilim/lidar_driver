from math import sin, cos, radians
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import (QApplication, QLabel, QGridLayout, QPushButton, 
    QWidget, QVBoxLayout, QFrame, QComboBox, QHBoxLayout)

import serial
import serial.tools.list_ports
import pyqtgraph as pg
import numpy as np

# Data streamed in the format: (TOF1)-(TOF2)-(LIGHT1)-(LIGHT2)
np.random.seed(42)

class Worker(QThread):
    signal = pyqtSignal(object)

    def __init__(self, serial_object):
        super(Worker, self).__init__()
        self.serial_object = serial_object

    def run(self):
        while True:
            if self.isInterruptionRequested():
                print("stop worker!")
                return
            self.signal.emit(self.serial_object.readline().decode())

class MainWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.baudrate = -1
        self.serialport = "invalid_port"
        self.xy_data = [[], []]
        self.buffer = []
        self._buildUI()

    def _buildBottomTextBar(self):
        text_debug = QLabel(text="Debug here")
        text_debug.setFixedHeight(50)
        text_debug.setStyleSheet("background-color:cyan")

        self.text_debug = text_debug

    def _buildRightSettingsBar(self):
        # Connect status setup
        text_connect_status = QLabel(text="Disconnected")
        drawing_connect_status = QLabel() # Some creative use of stylesheets to 
                                          # draw our circle
        drawing_connect_status.setFixedSize(20, 20)
        drawing_connect_status.setStyleSheet("""border: 0px solid black; 
                                                border-radius: 10px;
                                                background-color: red""")
        grid_connect_status = QHBoxLayout()
        grid_connect_status.addWidget(text_connect_status)
        grid_connect_status.addWidget(drawing_connect_status)

        # Serial Port setup
        text_serialport = QLabel(text="Serial Port")
        list_ports = [port.device for port in serial.tools.list_ports.comports()]
        combobox_serialport = QComboBox()
        combobox_serialport.addItems(list_ports)
        combobox_serialport.setFixedWidth(180)
        combobox_serialport.currentIndexChanged.connect(self._handlerSerialport)
        grid_serialport = QVBoxLayout()
        grid_serialport.addStretch(1)
        grid_serialport.addWidget(text_serialport)
        grid_serialport.addWidget(combobox_serialport)

        # Baud rate setup
        text_serialport = QLabel(text="Baud rate")
        list_baudrate = ["300", "600", "1200", "2400", "4800", "9600", "14400", 
                         "19200", "28800", "31250", "38400", "57600", "115200"]
        combobox_baudrate = QComboBox()
        combobox_baudrate.addItems(list_baudrate)
        combobox_baudrate.setFixedWidth(180)
        combobox_baudrate.currentIndexChanged.connect(self._handlerBaudrate)
        grid_baudrate = QVBoxLayout()
        grid_baudrate.addStretch(1)
        grid_baudrate.addWidget(text_serialport)
        grid_baudrate.addWidget(combobox_baudrate)

        # Connect button setup
        button_connect = QPushButton()
        button_connect.setText("Connect")
        button_connect.setFixedWidth(100)
        button_connect.clicked.connect(self._handlerConnect)

        button_disconnect = QPushButton()
        button_disconnect.setText("Disconnect")
        button_disconnect.setFixedWidth(100)
        button_disconnect.clicked.connect(self._handlerDisconnect) 

        # Reset button setup
        button_reset = QPushButton()
        button_reset.setText("Reset graph")
        button_reset.setFixedWidth(200)
        button_reset.clicked.connect(self._handlerReset)

        grid_buttons = QGridLayout()
        grid_buttons.addWidget(button_connect, 1, 1)
        grid_buttons.addWidget(button_disconnect, 1, 2)
        grid_buttons.addWidget(button_reset, 2, 1)

        # Overall grid
        grid_settings = QVBoxLayout()
        grid_settings.addLayout(grid_connect_status)
        grid_settings.addLayout(grid_serialport)
        grid_settings.addLayout(grid_baudrate)
        grid_settings.addLayout(grid_buttons)

        frame_settings = QFrame()
        frame_settings.setLayout(grid_settings)
        frame_settings.setFixedWidth(230)
        self.frame_settings = frame_settings

        # Exposing combobox for callback functions
        self.combobox_baudrate = combobox_baudrate
        self.combobox_serialport = combobox_serialport
        self.drawing_connect_status = drawing_connect_status
        self.text_connect_status = text_connect_status

        # Set dropdown box default values
        self.combobox_baudrate.setCurrentIndex(list_baudrate.index('115200'))

    def _buildMainMapUI(self):
        text_header = QLabel(text="LIDAR visualisation v1.0")
        text_header.setFixedHeight(30)
        frame_placeholder = QFrame()
        frame_placeholder.setStyleSheet("background-color:pink")

        plot_widget = pg.PlotWidget()
        plot_widget.setFixedSize(800, 600)
        graph_item = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(255, 255, 255, 200))
        
        # pos = np.random.normal(size=(2,10))
        # self.xy_data = pos.tolist()
        graph_item.setData(x=self.xy_data[0], y=self.xy_data[1])
        plot_widget.addItem(graph_item)
        plot_widget.setRange(xRange=[-1000,1000], yRange=[-1000, 1000])

        grid_map = QGridLayout()
        grid_map.addWidget(text_header, 0, 0)
        grid_map.addWidget(plot_widget, 1, 0)

        frame_map = QFrame()
        frame_map.setLayout(grid_map)

        self.frame_map = frame_map
        self.graph_item = graph_item

    def _buildUI(self):
        self._buildBottomTextBar()
        self._buildRightSettingsBar()
        self._buildMainMapUI()

        grid_main = QGridLayout()
        grid_main.addWidget(self.frame_map, 0, 0)
        grid_main.addWidget(self.frame_settings, 0, 1)
        grid_main.addWidget(self.text_debug, 1, 0, 1, 2) # row1, column2, occupies 1 row and 2 columns
 
        self.setLayout(grid_main)
        self.setGeometry(300, 300, 200, 200) # x, y, width, height
        self.setWindowTitle('PyQt5 Layout')
        self.show()

    # Handler functions
    def _handlerSerialport(self, idx):
        self.serialport = self.combobox_serialport.itemText(idx)
        self.text_debug.setText(self.serialport)

    def _handlerBaudrate(self, idx):
        self.baudrate = int(self.combobox_baudrate.itemText(idx))

    def _handlerConnect(self):
        try:
            self.ser = serial.Serial(self.serialport, int(self.baudrate))
            self.worker = Worker(self.ser)
            self.worker.signal.connect(self.handlerWorker)
            self.worker.start()

            self.drawing_connect_status.setStyleSheet("""border: 0px solid black; 
                                                border-radius: 10px;
                                                background-color: green""")
            self.text_connect_status.setText("Connected")
            self.text_debug.setText("Reading values...")
        except:
            self.text_debug.setText("Failed to connect!")

    def _handlerDisconnect(self):
        try:
            self.worker.requestInterruption()
            self.ser.close()
            self.text_debug.setText("Disconnected; worker stopped")
            self.drawing_connect_status.setStyleSheet("""border: 0px solid black; 
                                                border-radius: 10px;
                                                background-color: red""")
            self.text_connect_status.setText("Disconnected")
            self._handlerReset()
            self.text_debug.setText("Disconnected")
        except:
            self.text_debug.setText("Nothing to disconnect")

    def _handlerReset(self):
        self.xy_data = [[], []]
        self.graph_item.setData(x=self.xy_data[0], y=self.xy_data[1])
        self.text_debug.setText("Graph reset!")

    def handlerWorker(self, input):
        input = str(input)
        try:
            tof1, tof2, light1, light2 = input.split("-")
            if (light1 == '1' and len(self.buffer) > 10):
                self.plotBuffer()
                self.buffer = []
            else:
                self.buffer.append(float(tof1))
        except ValueError:
            print("init stuff")
        print(self.buffer)

    # Plotting functions
    def plot(self, x, y):
        self.xy_data[0].append(x)
        self.xy_data[1].append(y)
        self.graph_item.setData(x=self.xy_data[0], y=self.xy_data[1])

    def plotPolar(self, angle, dist):
        self.plot(dist * cos(radians(90-angle)), 
                  dist * sin(radians(90-angle)))

    def plotBuffer(self):
        self.xy_data = [[], []]
        self.graph_item.setData(x=self.xy_data[0], y=self.xy_data[1])

        noOfPoints = len(self.buffer)
        for idx, point in enumerate(self.buffer):
            self.plotPolar(360 / noOfPoints * idx, point)
        
app = QApplication([])
bla = MainWindow()
app.exec_()