import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import time

pir = 19
GPIO.setup(pir, GPIO.IN)

while True:
    if GPIO.input(pir) == True:
        print(True)
        time.sleep(1)
    elif GPIO.input(pir) == False:
        print(False)
        time.sleep(1)
