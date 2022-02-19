import serial
import os
import time
from datetime import datetime

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=0.5)

ok = "OK"
admin_num = ""
##RTO_num = ""
number = ""
rcv = None
admin_config = False
##RTO_config = False

def send_cmd(cmd,response=None,t=0.5):
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=t)
    cmd1 = cmd
    cmd = str.encode(cmd + "\r")
    port.write(cmd)
    print("cmd" + str(cmd))
    rcv = port.readall()
    rcv = rcv.decode()
    rcv = rcv.strip()
    print ("rcv = ", rcv)
##    print(type(rcv))
    if (cmd1 == "AT+CGPSINF=2"):
        return str(rcv)
    
    elif response:
        print (rcv.endswith(response))
        return rcv.endswith(response)


def send_sms(text,num):
    print ("sending sms to ",num)
    send_cmd("AT+CMGF=1",ok)
    if send_cmd("AT+CMGS=\""+num+'\"','>'):
        if send_cmd(text+"\x1a",ok,5):
            print ("sms send")
        else:
            print ("cant send sms....check your balance")
        
def get_data():
    print ("data available")
    rcv = port.readall().strip()
    rcv = rcv.decode()
    print ("rcv=" , rcv)   
    check_data(rcv)
    port.flushInput()

def check_data(data):
    global admin_num
    global admin_config
    if data.find("+CLIP") > 0:
        index1 = data.find('\"') + 1
        index2 = data.find(',') - 1
        number = data[index1:index2]
        print ("receiving call from ",number)
        if not admin_config:
            admin_num = number
            admin_config = True
            print ("admin number saved..",admin_num)
            time.sleep(1)
            send_cmd("ATH",ok)
            print ("call cut")
            send_sms("This number is configure as ADMIN..",admin_num)            
        elif admin_config :
            print ("configuration already done")
            time.sleep(1)
            send_cmd("ATH",ok)
            print ("call cut")

        else:
            print ("%s already configure.."%admin_num)
            time.sleep(1)
            send_cmd("ATH",ok)
            print ("call cut")

    if data.find("+CMT") > 0:
        index1 = data.find('\"') + 1
        index2 = data.find(',') - 1
        sms_number = data[index1:index2]
        index3 = data.rfind('"') + 1
        sms = data[index3:]
        print ("number: ",sms_number)
        print ("sms: ", sms)

def gps_track():
    _lat = 0
    _lon = 0
    print('Tracking')
    gps_data = str(send_cmd("AT+CGPSINF=2"))
    gps_data = gps_data.strip()
    print ("gps_data =", gps_data)
    if gps_data.find("+CGPSINF:") >= 0:
        index1 = gps_data.find(',N')
        _lat = gps_data[0:index1]
        print (_lat)
        index2 = _lat.rfind(',') +1
        _lat = str(_lat[index2 : ])

        index1 = gps_data.find(',E')
        _lon = gps_data[0:index1]
        print (_lat)
        index2 = _lon.rfind(',') +1
        _lon = str(_lon[index2 : ])

        print ("lat = " , float(_lat))
        print ("lon = " , float(_lon))
        return float(_lat),float(_lon)

sms_sent = True
main = True
if main:
    print ("connecting GSM")     
    while True:
        if send_cmd("AT",ok):
            send_cmd("ATE0",ok)
            send_cmd("AT+CNMI=2,2,0,0",ok)
            send_cmd("AT+CGPSPWR=1",ok)
            send_cmd("AT+CLIP=1",ok)
            print ("GSM connected")
            time.sleep(1)
            break
        else:
            print ("GSM not connected")
            main = False
            time.sleep(3)
            break
    port.flushInput()
    port.flushOutput()
    if main:
        print ("Waiting for admin")
        while not admin_config:
            time.sleep(0.5)
            if port.inWaiting() > 0:
                get_data()
        print('Admin number is configured')
        sms_sent = False


if sms_sent == False:
    port.flushInput()
    port.flushOutput()
    lat,lon = gps_track()
    
    if lat > 0 and lon > 0:
        print('Lat: ', lat)
        print('Lon: ', lon)
        map_site = "Alcohol Detected!!\n" + "http://maps.google.com/maps?f=q&q=" + str(lat) + "," + str(lon) + "&z=16"
        print (map_site)
        send_sms(map_site,admin_num)
        sms_sent = True        
    else:
        print ("gps not working")
        map_site = "Alcohol Detected!!\n" + "gps not working"
        send_sms(map_site,admin_num)
        sms_sent = True
