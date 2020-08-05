from flask import Flask, request, send_file, jsonify

app = Flask("appserver")
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app)

# TODO: Refactor all server code


@app.route("/setSchedule", methods=["POST", "GET"])
def app_connect():
    if request.method == "POST":
        thread_active = False
        print(request.get_json())
        camera_config = request.get_json()
        with open("/home/pi/openoceancamera/schedule.json", "w") as outfile:
            json.dump(camera_config, outfile)
        date_input = camera_config[0]["date"]
        timezone = camera_config[0]["timezone"]
        # Clear WittyPi schedule
        clear_cmd = "sudo sh /home/pi/openoceancamera/wittypi/wittycam.sh 10 6"
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
