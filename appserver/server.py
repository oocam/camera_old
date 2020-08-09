# WIP: Refactoring all server code

from flask import Flask, request, send_file, jsonify
from camera import Camera
from flask_cors import CORS
import os, uuid, logging, sensors, time

# IMPORTANT: Is directory restructuring needed? See https://flask.palletsprojects.com/en/1.1.x/patterns/packages/

# Move to "main" file responsible for insantiating the server?
app = Flask("appserver")
app.config["CORS_HEADERS"] = "Content-Type"
server_logger = logging.getLogger(__name__)
CORS(app)

# Notes for anyone refactoring this code in the future:
# 1. Directories and files (schedule.json, /media/pi/...) should be accessed from the app config
# 2. Use only the requests you need - don't expect a POST request when all you're doing is creating a pure function to return data
# 3. Name your functions the same way you name your routes
# 4. Use HTTP response codes - they make for cleaner conditions for the API user

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
    if camera_config != []:
        return json.dumps(camera_config), 200
    else:
        server_logger.info("[/viewConfig] No configuration exists!")
        return "No configuration exists.", 500

@app.route("/turnOffWifi", methods=["POST"])
def turnOffWifi():
    # Unsure where this code lives now
    os.system(cmdoff)
    os.system(cmdoff1)
    sys.exit()

    server_logger.info("[/turnOffWifi] Wifi switched off.")
    return "OK", 200

@app.route("/testPhoto", methods=["POST"])
def testPhoto():
    #Instantiate camera
    camera = Camera()
    camera_options = request.get_json(force=True)[0]
    PWM.switch_on(camera_options["light"])
    camera.set_iso(camera_options["iso"])
    camera.set_shutter_speed(camera_options["shutter_speed"])

    routeResponse = ""
    responseCode = 200

    try:
        camera.capture()

        # Maybe the server shouldn't be responsible for this.
        # Seems wrong for the server to be getting a test image when the
        # test image isn't changing
        with open(app.config["TEST_IMAGE"], "rb") as image:
            img_base64 = base64.b64encode(image.read())

        # Function doesn't exist yet
        sensor_data = sensors.readSensorData()

        server_logger.debug(f"[/testPhoto] Read sensor data: {sensor_data}")
        response = {
            "image": img_base64.decode("utf-8"),
            "sensorData": json.dumps(sensor_data),
        }

        # Leaving this here for now, but unsure why this sleep call is needed
        time.sleep(2)

        server_logger.info(f"[/testPhoto] Capture test successful.")
        
        routeResponse = jsonify(response)
        
    except Exception as e:
        server_logger.error(f"[/testPhoto] Encounterd: {str(e)}")
        routeResponse = str(e)
        responseCode = 500

    finally:
        # Wrap up
        camera.close()
        PWM.switch_off()

    return routeResponse, responseCode

@app.route("/testPhotoMem", methods=["POST"])
def testPhotoMem():
    #Instantiate camera
    camera = Camera()
    camera_options = request.get_json(force=True)[0]
    PWM.switch_on(camera_options["light"])
    camera.set_iso(camera_options["iso"])
    camera.set_shutter_speed(camera_options["shutter_speed"])

    result = "SUCCESS"
    responseCode = 200

    # Check if USB storage is connected
    external_drive = app.config["EXTERNAL_DRIVE"]
    if os.path.isdir(external_drive):
        try:
            image_name = f"{external_drive}/{uuid.uuid4()}.jpg"

            # Is recreating a Camera instance really the way to go here?
            # @whoever is working on the Camera module, maybe figure out a way
            # to make this cleaner? Maybe we don't need to close this Camera instance
            # at all?
            camera.capture(filename=image_name)
            camera.close()
            server_logger.info(f"[/testPhotoMem] Wrote {image_name}")

            camera = Camera()
            camera.set_camera_resolution((1920, 1080))
            camera.set_camera_frame_rate(30)

            # @whoever is working on Camera: maybe refactor into a record function that takes
            # a duration, and starts/stops recording on its own. The server shouldn't be responsible
            # for sleeping
            video_name = f"{external_drive}/{uuid.uuid4()}.h264"
            camera.start_record(filename=video_name)
            time.sleep(3)
            camera.stop_recording()
            server_logger.info(f"[/testPhotoMem] Wrote {video_name}")

            server_logger.info(f"[/testPhotoMem] Capture test successful.")

        except Exception as e:
            server_logger.error(f"[/testPhotoMem] Encounterd: {str(e)}")
            result = str(e)
            responseCode = 500
    else:
        server_logger.error(f"[/testPhotoMem] No USB drive found!")
        result = "USB Storage with name OPENOCEANCA required"
        responseCode = 507 #Insufficient Storage

    # Wrap up
    camera.close()
    PWM.switch_off()

    # Function doesn't exist yet
    sensor_data = sensors.readSensorData()
    server_logger.info(f"[/testPhotoMem] Read sensor data: {sensor_data}")

    response = {
        "result": result,
        "sensorData": json.dumps(sensor_data),
    }

    return response, responseCode