'''
Develop a Python script to control the proportional pinch valve connected to the outlet of
a pressurized reservoir.
'''
import serial

#Connect to Serial port
serl = serial.Serial('Address of serial port', 9600, timeout=1)

#init proportional pinch valve
serl.write(b'MINP 0\r\n')
serl.write(b'MAXP 100\r\n')
serl.write(b'RESP 10\r\n')

#Valve information
valve_pressure = 50
command = (f'PRES {valve_pressure}\r\n')
serl.write(command.encode())

#close connection to serial port
serl.close()