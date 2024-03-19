# Follow the instructions here: https://medium.com/@kekreaditya/interfacing-u-blox-neo-6m-gps-module-with-raspberry-pi-1df39f9f2eba

import serial
import time
import string 
import pynmea2

while True: 
    port="/dev/ttyAMAO"

    ser=serial.Serial(port,baudrate=9600,timeout=0.5)

    dataout =pynmea2.NMEAStreamReader()

    newdata=ser.readline()

    if newdata[0:6]=="$GPRMC":

        newmsg=pynmea2.parse(newdata)

        lat=newmsg.latitude

        lng=newmsg.longitude

        gps="Latitude=" +str(lat) + "and Longitude=" +str(lng)

        print(gps)