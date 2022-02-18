#Libraries
import RPi.GPIO as GPIO
import time
from threading import Timer
 
GPIO.setmode(GPIO.BCM)

front_trigg= 7
front_echo = 8

GPIO.setup(front_trigg, GPIO.OUT)
GPIO.setup(front_echo, GPIO.IN)
 
def distance_isr(Trigger, Echo):
    global distance
    GPIO.output(Trigger, False)
    time.sleep(0.60)
    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)
 
    StopTime = time.time()
    while GPIO.input(Echo) == 0:
        None
  
    StartTime = time.time()
    while GPIO.input(Echo) == 1:
        None

    TimeElapsed = time.time() - StartTime
    distance = (TimeElapsed * 34300) / 2

    if distance >= 200:
        distance = 200
    return distance

distance = 0

while True:
    distance = distance_isr(front_trigg, front_echo)
    print ("Measured Front Distance = %.1f cm" % distance)
    time.sleep(1)
