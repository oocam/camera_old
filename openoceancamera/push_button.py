import RPi.GPIO as GPIO
import os
import time
cmdon="sudo ifconfig wlan0 up"
cmdon1="sudo service dnsmasq start"
cmdon2="sudo service hostapd start"
cmdoff="sudo ifconfig wlan0 down"
cmdoff1="sudo service dnsmasq stop"
cmdoff2="sudo service hostapd start"
#os.system(cmdoff)
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
wlon=0;
prevwlan=0;

while True:
    if (GPIO.input(18)==GPIO.HIGH):
        wlan=1
    else:
        wlan=0
    if(wlan==0 and prevwlan!=0):
        os.system(cmdoff)
        os.system(cmdoff1)
        os.system(cmdoff2)
        print("wlan off")
    elif(wlan==1 and  prevwlan!=1):
        os.system(cmdon)
        os.system(cmdon1)
        os.system(cmdon2)
        #TURN OFF OLD ONE AND TURN ON
        print("wlanon")
    prevwlan=wlan
    time.sleep(5)
        

