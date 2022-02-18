import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
import serial

state = 13
GPIO.setup(state, GPIO.IN)

def get_data(channel):
    while True:
        port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
        rcv = port.readall().strip()
        rcv = rcv.decode()
        patient_data = rcv
        if patient_data:
            health_data =  patient_data.split(",")
            print(type(patient_data))
            sys = str(health_data[0]).strip()
            dia = str(health_data[1]).strip()
            beats = str(health_data[2]).strip()
            print("sys: %s" % sys)
            print("dia: %s" % dia)
            print("beats: %s" % beats)
            break
GPIO.add_event_detect(state, GPIO.RISING, callback= get_data)

while True:    
    time.sleep(2)
