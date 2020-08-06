from Scheduler import Scheduler
from picamera import PiCamera

# import ms5837
import smbus
from flask_cors import CORS
import threading
from flask import Flask, request, send_file, jsonify
from datetime import datetime, timedelta
import logging
import json
from uuid import uuid1
from time import sleep, time
import base64
from os import path
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

import os
import sys
import subprocess
from subsealight import PWM

sys.path.append("/usr/lib/python3.5/")
sys.path.append("/usr/lib/python3/")
cmdoff = "sudo ifconfig wlan0 down"
cmdoff1 = "sudo service dnsmasq stop"

try:
    from Camera import Camera
except:
    print("Could not initialise the camera")

threads = []

app = Flask("OpenOceanCam")
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app)

external_drive = "/media/pi/OPENOCEANCA"
camera_config = []
thread_active = False

last_file_name = ""


def readSensorData():

    try:
        lightSensor = float(
            str(
                subprocess.check_output(
                    "python /home/pi/openoceancamera/TSL2561/Python/TSL2561.py", shell=True, text=True
                )
            )
        )
    except Exception as e:
        lightSensor = -1.0

    try:
        temperatureSensor = float(
            str(
                subprocess.check_output(
                    "python /home/pi/openoceancamera/tsys01-python/example.py", shell=True, text=True
                )
            )
        )
    except Exception as e:
        temperatureSensor = -1.0

    try:
        pressureSensorReadings = subprocess.check_output(
            "python /home/pi/openoceancamera/ms5837-python/example.py", shell=True, text=True
        )

        pressureSensorReadings = pressureSensorReadings.split()

        pressureSensor, mstemperatureSensor, depthSensor = (
            float(pressureSensorReadings[0]),
            float(pressureSensorReadings[1]),
            float(pressureSensorReadings[2]),
        )
    except Exception as e:
        pressureSensor = -1.0
        mstemperatureSensor = -1.0
        depthSensor = -1.0

    return {
        "luminosity": lightSensor,
        "temp": temperatureSensor,
        "pressure": pressureSensor,
        "mstemp": mstemperatureSensor,
        "depth": depthSensor,
    }


def start_capture(camera, video):
    global external_drive, last_file_name
    if not video:
        filename = external_drive + "/" + str(uuid1()) + ".jpg"
        last_file_name = filename
        camera.do_capture(filename=filename)
        print("Written")
    else:
        filename = external_drive + "/" + str(uuid1()) + ".h264"
        camera.do_record(filename=filename)
        print("Started recording")
    logging.info("Write: " + filename + " at time " + str(datetime.now()))


def main():
    camera = None
    print("Main started")
    global thread_active
    while True:
        sleep(2)
        if thread_active:
            data = camera_config
            switch_flag = 0
            isrecord = 0
            isopen = 0
            print(thread_active)
            my_schedule = Scheduler(data)
            print("Loaded Scheduler. Main thread active")

            # Stall the camera to let it initialise
            while thread_active:
                # print(my_schedule.should_start())
                my_schedule.update_current_time()
                slot = my_schedule.should_start()
                if slot == -1 and isrecord == 0:
                    sleep(2)

                if isrecord == 1 and slot == -1:
                    PWM.switch_off()
                    camera.do_close()
                    print("CLOSED")
                    isrecord = 0
                    isopen = 0

                if slot >= 0:  # if slot open
                    if isopen == 0:
                        try:
                            camera = Camera()
                        except Exception as e:
                            print(e)
                        isopen = 1
                    sensor_data = readSensorData()
                    log_filename = f"{external_drive}/log.txt"
                    file_mode = None
                    if os.path.exists(log_filename):
                        file_mode = "a"
                    else:
                        file_mode = "w"
                    try:
                        with open(log_filename, file_mode) as f:
                            f.write(
                                json.dumps(
                                    {
                                        "timestamp": datetime.now().strftime(
                                            "%m/%d/%Y, %H:%M:%S"
                                        ),
                                        "luminosity": sensor_data["luminosity"],
                                        "temp": sensor_data["temp"],
                                        "pressure": sensor_data["pressure"],
                                        "mstemp": sensor_data["mstemp"],
                                        "depth": sensor_data["depth"],
                                    }
                                )
                            )
                    except:
                        with open(log_filename, "w"):
                            pass
                    camera.set_capture_frequency(data[slot]["frequency"])
                    camera.set_iso(data[slot]["iso"])
                    camera.set_shutter_speed(data[slot]["shutter_speed"])
                    # GPIO.output(17, data[slot]["light"])
                    light_mode = data[slot]["light"]
                    PWM.switch_on(light_mode)
                    # print(data[slot]["frequency"])
                    if not data[slot]["video"]:  # slot for photo
                        start_capture(camera, False)
                        print(my_schedule.should_start())
                        sleep(data[slot]["frequency"])
                        isrecord = 1
                    else:

                        if isrecord == 0:  # slot for video, has not recorded yet
                            camera.set_camera_resolution((1920, 1080))
                            camera.set_camera_frame_rate(30)
                            print("RECORDING")
                            start_capture(camera, True)
                            isrecord = 1
                        else:  # slot for video, already recording
                            sleep(1)
                            pass
                        # while  my_schedule.should_start() == slot:
                        # print("Recording")
                        # print(my_schedule.should_start())
                        # pass
                    switch_flag = 0

                else:
                    if switch_flag == 0:
                        logging.info("Stop: " + str(datetime.now()))
                        switch_flag = 1

                next_slot = my_schedule.next_future_timeslot()
                slot = my_schedule.should_start()
                if next_slot is not None:
                    print("Next slot is: ")
                    print(next_slot)
                    mins_to_next_slot = int(my_schedule.time_to_nearest_schedule() / 60)
                    print(f"We have {mins_to_next_slot} mins to next slot")
                    if (mins_to_next_slot > 10) and slot == -1:
                        five_mins = timedelta(minutes=2)
                        one_mins = timedelta(minutes=5)
                        #thread_active = False
                        sleeptime = datetime.now() + one_mins
                        sleeptime = sleeptime.strftime("%d %H:%M")
                        next_reboot = next_slot["start"] - five_mins
                        print(f"I will wake up at {next_reboot}")
                        next_reboot = next_reboot.strftime("%d %H:%M:%S")
                        print(next_reboot)
                        startup_cmd = (
                            'sudo sh /home/pi/openoceancamera/wittypi/wittycam.sh 5 "' + next_reboot + '"'
                        )
                        print(startup_cmd)
                        os.system(startup_cmd)
                        print(
                            "raspberry pi is going to sleep now in 5 min, do not disturb"
                        )
                        shutdown_cmd = (
                            'sudo sh /home/pi/openoceancamera/wittypi/wittycam.sh 4 "' + sleeptime + '"'
                        )
                        os.system(shutdown_cmd)
                        thread_active = False
                        break


def update_config():
    pass


@app.route("/setSchedule", methods=["POST", "GET"])
def app_connect():
    global external_drive
    global camera_config
    global thread_active
    if request.method == "POST":
        thread_active = False
        print(request.get_json())
        camera_config = request.get_json()
        with open("/home/pi/openoceancamera/schedule.json", "w") as outfile:
            json.dump(camera_config, outfile)
        date_input = camera_config[0]["date"]
        timezone = camera_config[0]["timezone"]
        clear_cmd = ('sudo sh /home/pi/openoceancamera/wittypi/wittycam.sh 10 6')
        os.system(clear_cmd)
        os.system(f"sudo timedatectl set-timezone {timezone}")
        print(timezone)
        print(date_input)
        # Sets the system time to the user's phone time
        os.system(f"sudo date -s '{date_input}'")
        # Save the system time to RTC -
        os.system("sudo sh /home/pi/openoceancamera/wittypi/wittycam.sh 1")
        os.system("sudo sh /home/pi/openoceancamera/wittypi/wittycam.sh 2")
        # external_drive = "/media/pi/" + sys.argv[1]
        external_drive = "/media/pi/OPENOCEANCA"
        pathv = path.exists(external_drive)
        if pathv:
            thread_active = True
            return {
                "success": "Success",
            }
        else:
            return {
                "success": "Not a Success. No Memory called OPENOCEANCA inserted.",
            }
    else:
        return {
            "success": "Not a Success",
        }


@app.route("/viewConfig", methods=["GET"])
def returnConfig():
    if request.method == "GET":
        if camera_config != []:
            camera_config[0].localdate = str(datetime.now())
            return json.dumps(camera_config)
        else:
            return {
                "error": "No Configuration exists",
            }


@app.route("/turnOffWiFi", methods=["GET"])
def turnOffWiFi():
    if request.method == "GET":
        os.system(cmdoff)
        os.system(cmdoff1)
        sys.exit()
        print("Wi-FI Off")
        return {
            "success": "Success",
        }


@app.route("/testPhoto", methods=["POST", "GET"])
def sendTestPic():
    camera = Camera()
    if request.method == "POST":
        try:
            data = request.get_json(force=True)
            PWM.switch_on(data[0]["light"])
            camera.set_iso(data[0]["iso"])
            camera.set_shutter_speed(data[0]["shutter_speed"])
            camera.do_capture()
            with open("/home/pi/openoceancamera/test.jpg", "rb") as image:
                img_base64 = base64.b64encode(image.read())
            camera.do_close()
            sensor_data = readSensorData()
            print(f"Read sensor data: {sensor_data}")
            response = {
                "image": img_base64.decode("utf-8"),
                "sensors": json.dumps(sensor_data),
            }
            sleep(2)
            PWM.switch_off()
            return jsonify(response)
        except Exception as e:
            camera.do_close()
            PWM.switch_off()
            print(e)
            return "ERROR"


@app.route("/testPhotoMem", methods=["POST", "GET"])
def sendTestPicMem():
    if request.method == "POST":
        camera = Camera()
        data = request.get_json(force=True)
        PWM.switch_on(data[0]["light"])
        camera.set_iso(data[0]["iso"])
        camera.set_shutter_speed(data[0]["shutter_speed"])
        flag = "SUCCESS"
        external_drive = "/media/pi/OPENOCEANCA"
        pathv = path.exists(external_drive)
        if pathv:
            try:
                filename1 = external_drive + "/" + str(uuid1()) + ".jpg"
                camera.do_capture(filename=filename1)
                print("Written")
                camera.do_close()
                camera = Camera()
                camera.set_camera_resolution((1920, 1080))
                camera.set_camera_frame_rate(30)

                filename2 = external_drive + "/" + str(uuid1()) + ".h264"
                camera.do_record(filename=filename2)
                print("Started recording")
                sleep(3)
            except Exception as e:
                flag = str(e)
        else:
            flag = "USB Storage with name OPENOCEANCA required"

        camera.do_close()
        PWM.switch_off()
        sensor_data = readSensorData()
        response = {
            "flag": flag,
            "sensors": json.dumps(sensor_data),
        }
        return response


def start_api_server():
    app.run("0.0.0.0", 8000)


if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #    print("Usage: python main.py <external drive name>")
    #    exit(0)
    print("start")
    try:
        with open("/home/pi/openoceancamera/schedule.json") as f:
            camera_config = json.load(f)
            thread_active = True
            print("schedule opened, should start new thread")
    except IOError:
        print("No File")
    finally:
        api_thread = threading.Thread(target=start_api_server)
        main_thread = threading.Thread(target=main)
        api_thread.start()
        main_thread.start()
        main_thread.join()
        api_thread.join()
        logging.info("Program is shutting down")
