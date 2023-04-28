import sys
import serial as serl
import time
from pid import PID
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout

serl = serl.Serial('serial address', baudrate=9600, timeout=1)

class PIDControler(QWidget):
    def __init__(self):
        super().__init__()

        #Init the user interface
        self.initUI()

        #previous weight and time
        self.previous_time = None
        self.previous_weight = None

        Kd = .01
        Ki = .1
        Kp = 1

        max_valve_postion = 100
        min_valve_position = 0

        # Init the PID and timer
        self.pid = PID(Kp, Ki, Kd, setpoint=0, output_limits=(min_valve_position, max_valve_postion))
        self.valve_flow_rate = 0
        self.control_timer = None
        self.is_running = False

    def initUI(self):
        self.setGeometry(400, 400, 400, 50)
        self.setWindowTitle('Flow Control')

        #Create the buttons
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop)
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start)

        #Create the layout for the GUI
        virtical_box = QVBoxLayout()
        horizontal_box_1 = QHBoxLayout()
        horizontal_box_1.addWidget(QLabel('valve flow rate grams per second:'))
        horizontal_box_1.addWidget(QLineEdit())
        virtical_box.addLayout(horizontal_box_1)
        virtical_box.addWidget(QLabel('Current flow rate grams per second:'))
        virtical_box.addWidget(QLabel('0'))
        virtical_box.addWidget(QLabel('Valve position percentage:'))
        virtical_box.addWidget(QLabel('0'))
        horizontal_box_2 = QHBoxLayout()
        horizontal_box_2.addWidget(self.start_button)
        horizontal_box_2.addWidget(self.stop_button)
        virtical_box.addLayout(horizontal_box_2)
        self.setLayout(virtical_box)

    def start(self):
        #desired rate from the field
        self.desired_flow_rate = float(self.desired_flow_rate_edit.text())

        #Start
        self.control_timer = self.startTimer(100)
        self.is_running = True

    def stop(self):
        #Stop
        self.killTimer(self.control_timer)
        self.is_running = False

    def timerEvent(self, event):
        #Read
        weight_data = serl.readline().decode().strip()

        #time
        curr_time = time.time()
        if self.prev_time is None:
            elapsed_time = 0
        else:
            elapsed_time = curr_time - self

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PIDControler()
    window.show()
    sys.exit(app.exec_())