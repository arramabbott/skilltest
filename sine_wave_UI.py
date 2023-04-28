'''
1. Design and implement a GUI using PyQt5 that consists of:
a. The main application window showing in the upper figure.
b. A button that controls the initiation of the sinewave plotting.
2. Upon clicking the button, the plot window should start displaying a randomly generated,
real-time sinewave, as shown in the lower figure.
a. The button should start an independent script that will run the sinewave function
and generate data.
3. Save the sinewave data as follows:
a. Save the real-time data from the sinewave to a numpy file every 1 second.
b. Save all data from the sinewave to a separate numpy file every 5 minutes.
'''

import sys
import matplotlib.pyplot as pylt
import numpy as nmp
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QGridLayout,QFrame, QScrollArea
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas
import time
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #Create the title window and set the size
        self.setWindowTitle("Arrams Skilltest")
        self.setGeometry(100, 100, 600, 400)
        self.graphContainer = QWidget()
        self.gridlayout = QGridLayout(self.graphContainer)
        self.scrollArea.setWidget(self.graphContainer)
        self.layout.addWidget(self.scrollArea)


        #Create the button to plot data
        self.plot_data_button = QPushButton("Plot Data", self)
        self.plot_data_button.move(50,50)
        self.plot_data_button.clicked.connect(self.plot_sine_wave_data)

        #save Timer
        self.realtime_timer = QTimer()
        self.realtime_timer.timeout.connect(self.save_data_realtime)
        self.realtime_timer.start(1000)
        self.all_data_timer = QTimer()
        self.all_data_timer.timeout.connect(self.save_all)
        self.all_data_timer.start(300000) 

        # Initialize the data array
        self.data = nmp.zeros((1000, 2))

    def plot_sine_wave_data(self):
        #create the data that will be used for the sinewave
        x = nmp.linspace(0,2*nmp.pi, 1000)
        y = nmp.sin(x)

        #create the plt itself
        fig,axis = pylt.subplots()
        axis.plot(x, y)
        axis.set_xlabel('x')
        axis.set_ylabel('sin(x)')
        axis.set_title('Sinewave Plot Data')
        pylt.show()

    def save_all(self):
        #save
        nmp.save("save_all.npy", self.data)
    
    def save_data_realtime(self):
        nmp.save("save_data_realtime.npy",self.data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())