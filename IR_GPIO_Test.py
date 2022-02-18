import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

ir1 = 27
ir2 = 17

GPIO.setup(ir1,GPIO.IN)
GPIO.setup(ir2,GPIO.IN)

def ir1_detect(channel1):##left sensor
    print('ir1: True')
    time.sleep(1)
    
def ir2_detect(channel2):##right sensor
    print('ir2: True')
    time.sleep(1)
    
GPIO.add_event_detect(ir1, GPIO.RISING, callback = ir1_detect, bouncetime=1)
GPIO.add_event_detect(ir2, GPIO.RISING, callback = ir2_detect, bouncetime=1)

while True:
    print("Working")
    time.sleep(1)
