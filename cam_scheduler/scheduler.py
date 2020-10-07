import os
import json
import logging
from datetime import datetime
from typing import List
from enum import Enum

scheduler_logger = logging.getLogger(__name__)


class ShootingMode(Enum):
    PHOTO: 0
    VIDEO: 1


class CameraConfig:
    def __init__(self, config: dict):
        self.shooting_mode = (
            ShootingMode.VIDEO
            if config.get("video") is not None
            else ShootingMode.PHOTO
        )
        self.frequency = config.get("frequency", None)
        self.light = config.get("light", 0)
        self.iso = config.get("iso", 0)
        self.shutter_speed = config.get("shutter_speed", 0)
        self.camera_resolution = (
            config.get("resolution").get("x", 1920),
            config.get("resolution").get("y", 1080),
        )
        self.camera_framerate = config.get("framerate", 0)

    @staticmethod
    def validate_config(config):
        pass


class ScheduleFrame:
    def __init__(self, start: datetime, stop: datetime, camera_config=None):
        super().__init__()
        self.start: datetime = start
        self.stop: datetime = stop
        self.executed: bool = False
        if camera_config is not None:
            self.camera_config: CameraConfig = CameraConfig(camera_config)
        else:
            logging.error(f"No configuration was provided to the schedule: {self}")

    def __str__(self):
        return {
            "start": self.start.isoformat(),
            "stop": self.stop.isoformat(),
            "camera_config": self.camera_config,
        }

    def __lt__(self, b):
        # a.__lt__(b) means self < object
        return self.start < b.start

    def set_executed(self):
        self.executed = True

    def should_frame_start(self):
        return (
            self.start <= datetime.now()
            and self.stop > datetime.now()
            and self.executed == False
        )

    def should_frame_run(self):
        return (
            self.start <= datetime.now()
            and self.stop > datetime.now()
            and self.executed
        )


class EventList:
    def __init__(self):
        super().__init__()
        self.queue: List(ScheduleFrame) = []

    def append(self, event):
        self.queue.append(event)
        self.queue.sort()

    def clear(self):
        self.queue = []

    def get_current_event_to_execute(self):
        for frame in self.queue:
            if frame.should_frame_start():
                return frame
        return None

    def get_current_active_frame(self):
        for frame in self.queue:
            if frame.should_frame_run():
                return frame
        return None


class Scheduler:
    def __init__(self, schedule_file):
        super().__init__()
        self.schedule_file = schedule_file
        self.events = EventList()

    def clear_all_events(self):
        self.events.clear()

    def get_event_list(self):
        return self.events

    def get_event_to_execute(self):
        return self.events.get_current_event_to_execute()

    def read_schedule_config(self):
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, "r") as f:
                data = f.read()
                data = json.dumps(data)
                return data
        else:
            return None

    def set_scheduler_data(self, data):
        if data is None:
            logging.warn(
                "There was no data while trying to load events from the schedule data."
            )
            return None

        logging.debug("Adding frames to events list")
        for i in range(len(data)):
            start = datetime.strptime(data[i]["start"], "%Y-%m-%d-%H:%M:%S")
            stop = datetime.strptime(data[i]["stop"], "%Y-%m-%d-%H:%M:%S")
            schedule_frame = ScheduleFrame(start, stop, data[i])
            logging.debug(schedule_frame)
            self.events.append(schedule_frame)
        logging.debug("Finished loading the slots for schedule")

    def get_active_slot(self):
        return self.events.get_current_active_frame()
