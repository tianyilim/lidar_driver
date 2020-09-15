from PyQt5.QtWidgets import (QApplication, QLabel, QGridLayout, QPushButton)
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QComboBox, QHBoxLayout
from PyQt5 import QtCore

import serial.tools.list_ports
import serial
import pyqtgraph as pg
import numpy as np

class MainWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.baudrate = -1
        self.serialport = "invalid_port"
        self._buildUI()

    def _handlerSerialport(self, idx):
        self.serialport = self.combobox_serialport.itemText(idx)
        self.text_debug.setText(self.serialport)

    def _handlerBaudrate(self, idx):
        self.baudrate = int(self.combobox_baudrate.itemText(idx))
        print(self.baudrate)

    def _handlerConnect(self):
        self.ser = serial.Serial(self.serialport)

    def _buildBottomTextBar(self):
        text_debug = QLabel(text="Debug here")
        text_debug.setFixedHeight(50)
        text_debug.setStyleSheet("background-color:cyan")

        self.text_debug = text_debug

    def _buildRightSettingsBar(self):
        # Connect status setup
        text_connect_status = QLabel(text="Disconnected")
        drawing_connect_status = QLabel() # Some creative use of stylesheets to draw our circle
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
        grid_serialport.addWidget(text_serialport, alignment=QtCore.Qt.AlignCenter)
        grid_serialport.addWidget(combobox_serialport, alignment=QtCore.Qt.AlignCenter)

        # Baud rate setup
        text_serialport = QLabel(text="Baud rate")
        combobox_baudrate = QComboBox()
        combobox_baudrate.addItems(["300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "28800", "31250", "38400", "57600", "115200"])
        combobox_baudrate.setFixedWidth(180)
        combobox_baudrate.currentIndexChanged.connect(self._handlerBaudrate)
        grid_baudrate = QVBoxLayout()
        grid_baudrate.addStretch(1)
        grid_baudrate.addWidget(text_serialport, alignment=QtCore.Qt.AlignCenter)
        grid_baudrate.addWidget(combobox_baudrate, alignment=QtCore.Qt.AlignCenter)

        # Connect button setup
        button_connect = QPushButton()
        button_connect.setText("Connect")
        button_connect.clicked.connect(self._handlerConnect)

        # Overall grid
        grid_settings = QVBoxLayout()
        grid_settings.addLayout(grid_connect_status)
        grid_settings.addLayout(grid_serialport)
        grid_settings.addLayout(grid_baudrate)
        grid_settings.addWidget(button_connect)

        frame_settings = QFrame()
        frame_settings.setLayout(grid_settings)
        frame_settings.setFixedWidth(200)
        self.frame_settings = frame_settings

        # Exposing combobox for callback functions
        self.combobox_baudrate = combobox_baudrate
        self.combobox_serialport = combobox_serialport

    def _buildMainMapUI(self):
        text_header = QLabel(text="LIDAR visualisation v1.0")
        text_header.setFixedHeight(30)
        frame_placeholder = QFrame()
        frame_placeholder.setStyleSheet("background-color:pink")

        # view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default

        # w1 = view.addPlot()
        w1 = pg.PlotWidget()
        w1.setFixedSize(800, 600)

        np.random.seed(42)
        n = 10
        s1 = pg.ScatterPlotItem(size=10, brush=pg.mkBrush(255, 255, 255, 200))
        pos = np.random.normal(size=(2,n))
        spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
        s1.addPoints(spots)
        w1.addItem(s1)
        
        s1.addPoints(x=[0], y=[1])

        grid_map = QGridLayout()
        grid_map.addWidget(text_header, 0, 0)
        grid_map.addWidget(w1, 1, 0)

        frame_map = QFrame()
        frame_map.setLayout(grid_map)

        self.frame_map = frame_map

    def _buildUI(self):
        # text2 = QLabel(text="World")
        # text2.setStyleSheet("background-color:cyan")
        self._buildBottomTextBar()
        self._buildRightSettingsBar()
        self._buildMainMapUI()

        grid_main = QGridLayout()
        grid_main.addWidget(self.frame_map, 0, 0)
        grid_main.addWidget(self.frame_settings, 0, 1)
        grid_main.addWidget(self.text_debug, 1, 0, 1, 2) # row1, column2, occupies 1 row and 2 columns
        # grid_main.setRowStretch(1,0)
        
        # grid.addWidget(Button1, 0, 1, alignment=QtCore.Qt.AlignRight)
        # grid.addWidget(Button2, 1, 0)
        # grid.addWidget(Button3, 1, 2)
        # grid.addWidget(Button4, 1, 1)
 
        self.setLayout(grid_main)
        self.setGeometry(300, 300, 200, 200) # x, y, width, height
        self.setWindowTitle('PyQt5 Layout')
        self.show()

app = QApplication([])
bla = MainWindow()
app.exec_()

# while True:
#     print(str(bla.ser.readline()))
    # self.text_debug.setText(ser.readline())
