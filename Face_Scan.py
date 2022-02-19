import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
from smbus import SMBus
import math
import cv2
import time
from servosix import ServoSix

ss = ServoSix()

servo1 = 2
servo2 = 1

angle1 = 0
angle2 = 0

not_finish = True
camera=cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

ret = camera.set(3,320)
ret = camera.set(4,240)

while not camera.isOpened():
    None
    
t1 = datetime.now()
low = True

angle1_high = 70
angle1_low = 35

angle1 = angle1_low
angle2 = 0

Video_file = "1.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter(Video_file,fourcc,12.0,(320,240))
                
while not_finish:
    
    ret, frame = camera.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        print ("face detected")
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
    t2 = datetime.now()
    delta = t2 - t1
    time_elapse = delta.total_seconds()
    if time_elapse > 0.1:
        if low:
            if angle1 < angle1_high:
                angle1 = angle1 + 1
            if angle1 == angle1_high:
                low = False
        else:
            if angle1 > angle1_low:
                angle1 = angle1 - 1
            if angle1 == angle1_low:
                low = True
                
        if angle1 <= angle1_low: 
            angle2 = angle2 + 45

        if angle2 > 90:
            angle2 = 0
        t1 = datetime.now()

        ss.set_servo(servo1, angle1)
        ss.set_servo(servo2, angle2)

    out.write(frame)
    cv2.imshow('gray',gray)
    cv2.imshow('img',frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

out.release()
print ('video saved')
