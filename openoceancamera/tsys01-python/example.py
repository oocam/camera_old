#!/usr/bin/python
import tsys01
from time import sleep

sensor = tsys01.TSYS01()
try:
    if not sensor.init():
        print("Error initializing sensor")
        exit(1)

    #while True:
    if sensor.read():
        print("{:.2f}".format(sensor.temperature()))       
    else:
        print("Error reading sensor")
        exit(1)
    #        sleep(0.2)
except: 
    print("TSYS01 not connected")
