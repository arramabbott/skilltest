'''
using python Implement a control algorithm (e.g., PID) to adjust the proportional pinch valve position
based on the calculated flow rate.
'''
import time
import serial
from pid import PID

serl = serial.Serial('serial address', 9600, timeout=1)

previous_flow_weight = None
previous_time = None

max_valve_postion = 100
min_valve_position = 0

valve_flow_rate = 5

Kd = .01
Ki = .1
Kp = 1

pid = PID(Kp, Ki, Kd, setpoint=valve_flow_rate, output_limits=(min_valve_position, max_valve_postion))


while True:
    Weight_information_data = serl.readline().decode().strip()
    print(f'Weight: {Weight_information_data} grams')
    
    #Time
    current_time = time.time()
    if previous_time is None:
        current_elapsed_time = 0
    else:
        elapsed_time = current_time - previous_time
    
    #weight
    current_flow_weight = float(Weight_information_data)
    if previous_flow_weight is None:
        weight_difference = 0
    else:
        weight_difference = current_flow_weight - previous_flow_weight

    #Flow
    current_flow_rate = weight_difference / current_elapsed_time
    pid_control_output = pid(current_flow_rate)


    #Print output
    print(f'FLow rate: {current_flow_rate} grams per second.')
    print(f'Pitch valve position: {pid_control_output}')

    previous_flow_weight = current_flow_rate
    previous_time = current_elapsed_time