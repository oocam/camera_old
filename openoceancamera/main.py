import sys
sys.path.append("/usr/lib/python3.5/")
sys.path.append("/usr/lib/python3/")
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
from os import path
import base64
cmdoff="sudo ifconfig wlan0 down"
cmdoff1="sudo service dnsmasq stop"
from time import sleep
from uuid import uuid1
import json
import logging
from datetime import datetime
from flask import Flask, request, send_file
import threading
from  flask_cors import CORS
from smbus import SMBus
import base64
import ms5837
import tsys01
from picamera import PiCamera

try:
    from Camera import Camera
except:
    print("Could not initialise the camera")
from Scheduler import Scheduler

threads = []

app = Flask("OpenOceanCam")
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

external_drive = "/media/pi/OPENOCEANCA" 
camera_config = []
thread_active = False

last_file_name = ""

def start_capture(camera, video):
    global external_drive, last_file_name
    if not video:
        filename = external_drive +"/"+ str(uuid1()) + ".jpg"
        last_file_name = filename
        camera.do_capture(filename=filename)
        print("Written")
    else:
        filename = external_drive +"/"+ str(uuid1()) + ".h264"
        camera.do_record(filename=filename)
        print("Started recording")
    logging.info("Write: " + filename + " at time " + str(datetime.now()))

def main():
        while True:
            sleep(2)
            if thread_active:
                data = camera_config
                switch_flag = 0
                isrecord=0
                isopen=0
                print(thread_active)
                my_schedule = Scheduler(data)
                #camera = Camera()
                logging.info("Loaded Scheduler")
                #sleep(3)
                
                # Stall the camera to let it initialise
                while thread_active:
                    #print(my_schedule.should_start())
                    my_schedule.update_current_time()
                    slot = my_schedule.should_start()
                    if slot==-1 and isrecord==0:
                        sleep(2)
                        
                    
                    if isrecord==1 and slot==-1:
                        camera.do_close()
                        print("CLOSED")
                        isrecord=0
                        GPIO.output(17,0)
                        isopen=0
                        
                    if slot >= 0:
                        if(isopen==0):
                            camera = Camera()
                            isopen=1
                        
                        camera.set_capture_frequency(data[slot]["frequency"])
                        camera.set_iso(data[slot]["iso"])
                        camera.set_shutter_speed(data[slot]["shutter_speed"])
                        GPIO.output(17,data[slot]["light"])
                        #print(data[slot]["frequency"])
                        if not data[slot]["video"]:
                            start_capture(camera, False)
                            print(my_schedule.should_start())
                            sleep(data[slot]["frequency"])
                            isrecord=1
                        else:
                            
                            if(isrecord==0):
                                camera.set_camera_resolution((1920,1080))
                                camera.set_camera_frame_rate(30)
                                print("RECORDING")
                                start_capture(camera, True)
                                isrecord=1
                            else:
                                pass
                            #while  my_schedule.should_start() == slot:
                                #print("Recording")
                                #print(my_schedule.should_start())
                                #pass
                        switch_flag = 0

                    else:
                        if switch_flag == 0:
                            logging.info("Stop: " + str(datetime.now()))
                            switch_flag = 1

	while camera.check_recording():
	    log_file = open(external_drive + "/log_file.txt", 'a')
	    log_file.write(sensor_log())
	    log_file.write("\n")
	    log_file.close()
				
def update_config():
    pass

def sensor_log():
    press_sensor = ms5837.MS5837_30BA()
    press_sensor.init()
    press_sensor.read(ms5837.OSR_256)

    temp_sensor = tsys01.TSYS01()
    temp_sensor.init()
    temp_sensor.read()

    time - "time:" + str(datetime.now) + "\n"
    lum = "lum:" + str(os.system("sudo ./TSL2561/Python/TSL2561.py")) + "\n"
    press = "press:" + str(press_sensor.pressure()) + "mbar \n"
    temp = "temp:" + str(temp_sensor.temperature()) + "C \n"
    data = time + lum + press + temp

    return data

@app.route("/setSchedule", methods=['POST', 'GET'])
def app_connect():
    global external_drive
    global camera_config
    global thread_active
    if request.method == 'POST':
        thread_active = False
        print(request.get_json())
        camera_config = request.get_json()
        with open('schedule.json','w') as outfile:
                json.dump(camera_config,outfile)
        os.system("sudo date --s '"+camera_config[0]['date']+"'")
#This above command sets the system time == to the user's phone time 
	os.system("sudo ./wittypi/wittycam.sh 1")
	os.system("sudo ./wittypi/wittycam.sh 2")
#These above commands save the system time to RTC - need to change for WittyPi
        #external_drive = "/media/pi/" + sys.argv[1]
        external_drive = "/media/pi/OPENOCEANCA"
        pathv=path.exists(external_drive)
        if pathv:
            thread_active = True,
            return {"success":"Success",}
        else:
            return {"success":"Not a Success. No Memory called OPENOCEANCA inserted.",}
    else:
        return {"success":"Not a Success",}

@app.route("/viewConfig", methods=['GET'])
def returnConfig():
    if request.method == 'GET':
        if(camera_config!=[]):
            return json.dumps(camera_config)
        else:
            return {"error":"No Configuration exists",}
        
@app.route("/turnOffWiFi", methods=["GET"])
def turnOffWiFi():
    if request.method == "GET":
        os.system(cmdoff)
        os.system(cmdoff1)
        sys.exit()
        print("Wi-FI Off")
        return {"success":"Success",}
    

@app.route("/testPhoto", methods=['POST', 'GET'])
def sendTestPic():
    if request.method == 'POST':
        camera = Camera()
        data=(request.get_json(force=True))
        camera.set_iso(data[0]["iso"])
        camera.set_shutter_speed(data[0]["shutter_speed"])
        camera.do_capture()
        with open("test.jpg","rb")as image:
        #return dat
            stra = base64.b64encode(image.read())
        image.close()
        camera.do_close()
        return stra


@app.route("/testPhotoMem", methods=['POST', 'GET'])
def sendTestPicMem():
    if request.method == 'POST':
        camera = Camera()
        data=(request.get_json(force=True))
        camera.set_iso(data[0]["iso"])
        camera.set_shutter_speed(data[0]["shutter_speed"])
        flag="SUCCESS"
        external_drive = "/media/pi/OPENOCEANCA"
        pathv=path.exists(external_drive)
        if pathv:
            try:
                filename1 = external_drive +"/"+ str(uuid1())+".jpg"
                camera.do_capture(filename=filename1)
                print("Written")
                camera.do_close()
                camera= Camera()
                camera.set_camera_resolution((1920,1080))
                camera.set_camera_frame_rate(30)
                                    
                filename2 = external_drive +"/"+ str(uuid1())+".h264"
                camera.do_record(filename=filename2)
                print("Started recording")
                sleep(3)
            except Exception as e:
                flag=str(e);
        else:
            flag="USB Storage with name OPENOCEANCA required"
        
        camera.do_close()
        return flag


def start_api_server():
    app.run("0.0.0.0", 8000)

if __name__ == "__main__":
    #if len(sys.argv) < 2:
    #    print("Usage: python main.py <external drive name>")
    #    exit(0)
    try:
        with open('schedule.json') as f:
            camera_config=json.load(f)    
            thread_active=True
    except IOError:
        print("No File")
    finally:
        f.close()
        api_thread = threading.Thread(target=start_api_server)
        main_thread = threading.Thread(target=main)
        api_thread.start()
        main_thread.start()
        main_thread.join()
        api_thread.join()
        logging.info("Program is shutting down")

