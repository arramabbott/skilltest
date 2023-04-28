'''
using python Calculate the flow rate based on the change in weight and time, ensuring that the flow
rate is within the specified limits.
'''
import time
import serial

serl = serial.Serial('serial address', 9600, timeout=1)

previous_flow_weight = None
previous_time = None

min_valve_flow_rate = 1
max_valve_flow_rate = 10


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
    if current_flow_rate < min_valve_flow_rate:
        current_flow_rate = min_valve_flow_rate
    elif current_flow_rate > max_valve_flow_rate:
        current_flow_rate = max_valve_flow_rate

    #Print output
    print(f'FLow rate: {current_flow_rate} grams per second.')

    previous_flow_weight = current_flow_rate
    previous_time = current_elapsed_time