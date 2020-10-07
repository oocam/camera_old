import pickle
import datetime

from constants import SCHEDULE_FILE_PATH
from cam_scheduler.scheduler import CameraConfig, ScheduleFrame
from .interface import UserInterface
from cam_scheduler import Scheduler
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app)


@app.route("/", methods=["GET", "POST"])
def ping():
    if request.method == "GET":
        return "OK"
    if request.method == "POST":
        # TODO: Set the camera time on this endpoint
        pass


@app.route("/setSchedule", methods=["POST"])
def set_schedule():
    if request.method == "POST":
        request_json = request.get_json()

        # Return back with an error if the JSON could not be parsed
        if request_json is None:
            return None

        # Validate that the config is acceptable
        if CameraConfig.validate_config(request_json):
            with open(SCHEDULE_FILE_PATH, "w") as schedule_file:
                scheduler_object = Scheduler(schedule_file=SCHEDULE_FILE_PATH)
                scheduler_object.set_scheduler_data(request_json)
                schedule_file.write(pickle.dumps(scheduler_object))


@app.route("/viewConfig", methods=["GET"])
def view_config():
    if request.method == "GET":
        response = {
            "local_time": datetime.now().strftime("%d-%B-%Y %H:%M:%S"),
            "local_timezone": "",
            "config": "",
        }
        return response


@app.route("/testPhoto")
def test_photo():
    if request.method == "POST":
        pass
