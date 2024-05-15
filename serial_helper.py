import serial as ser
import time 

def initialize_serial(COM_PORT, BAUD):
    ser = ser.Serial(COM_PORT, BAUD)

def angle_to_PWM(angle): 
    PWM = (angle/360)*255
    PWM = int(PWM)
    return PWM
def write_to_port(angle,serial_connection): 

    PWM = angle_to_PWM(angle)
    
    if 0 <= PWM <= 255: 
        serial_connection.write(bytes([PWM]))
        print("Sent Duty Cycle: ", PWM)
    else: 
        print("Invalid Input Duty Cycle")