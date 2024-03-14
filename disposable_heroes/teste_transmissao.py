import serial
import time

arduino = serial.Serial (port='/dev/ttyUSB0', baudrate=9600, bytesize=8, parity='N', stopbits=1)

time.sleep(2)

byte_R1 = "004002000000"
arduino.write(byte_R1.encode())
time.sleep(0.5)
arduino.close