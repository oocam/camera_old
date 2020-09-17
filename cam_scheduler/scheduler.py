import os
import json
import logging
from datetime import datetime
from typing import List

scheduler_logger = logging.getLogger(__name__)


class ScheduleFrame:
    def __init__(self, start: datetime, stop: datetime, camera_config=None):
        super().__init__()
        self.start = start
        self.stop = stop
        self.camera_config = camera_config

    def __str__(self):
        return {
            "start": self.start.isoformat(),
            "stop": self.stop.isoformat(),
            "camera_config": self.camera_config,
        }

    def __lt__(self, b: ScheduleFrame):
        # a.__lt__(b) means self < object
        return self.start < b.start

    def should_frame_start(self):
        return self.start <= datetime.now() and self.stop > datetime.now()


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

    def load_scheduler_data(self, data):
        if data is None:
            logging.warn(
                "There was no data while trying to load events from the schedule."
            )
            return

        logging.debug("Adding frames to events list")
        for i in range(len(data)):
            start = datetime.strptime(data[i]["start"], "%Y-%m-%d-%H:%M:%S")
            stop = datetime.strptime(data[i]["stop"], "%Y-%m-%d-%H:%M:%S")
            schedule_frame = ScheduleFrame(start, stop)
            logging.debug(schedule_frame)
            self.events.append(schedule_frame)
        logging.debug("Finished loading the slots for schedule")

    def get_active_slot(self):
        pass

    def prepare_camera_for_scheduled_slot(self):
        pass
