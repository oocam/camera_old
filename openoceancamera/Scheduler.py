from datetime import date, datetime, timezone
import pytz


class Scheduler(object):
    def __init__(self, data):
        self.time_now = datetime.now()
        self.schedule_data = []
        self.load_scheduler_data(data)

    def update_current_time(self):
        tz = pytz.timezone(timezone_str)
        self.time_now = datetime.now(tz=tz)

    def should_start(self):
        for i in range(len(self.schedule_data)):
            if (
                self.schedule_data[i]["start"]
                <= self.time_now
                <= self.schedule_data[i]["stop"]
            ):
                return i
        return -1

    def load_scheduler_data(self, data, timezone_str):
        for i in range(len(data)):
            frame = {
                "start": None,
                "stop": None,
            }
            frame["start"] = datetime.strptime(data[i]["start"], "%Y-%m-%d-%H:%M:%S")
            frame["stop"] = datetime.strptime(data[i]["stop"], "%Y-%m-%d-%H:%M:%S")
            self.schedule_data.append(frame.copy())

    def time_to_nearest_schedule(self):
        self.update_current_time()
        possible_slots = []

        # Get the future slots
        for slot in self.schedule_data:
            if slot["start"] >= self.time_now:
                possible_slots.append(slot)

        # Sorts the slots in case they may not be
        possible_slots = sorted(possible_slots, key=lambda x: x["start"])

        print(f"The time now is: {self.time_now}")
        print(f"The future slots are: {possible_slots}")

        # Take the difference between the most recent slot's start time and time now
        delta = possible_slots[0]["start"] - self.time_now
        print(f"The time difference is: {delta}")
        # Returns an integer value for the time difference in seconds
        return int(delta.total_seconds())

    def next_future_timeslot(self):
        self.update_current_time()

        future_slots = []
        # Get the future slots
        for slot in self.schedule_data:
            if slot["start"] >= self.time_now:
                future_slots.append(slot)
        # Sorts the slots in case they may not be
        future_slots = sorted(future_slots, key=lambda x: x["start"])
        return future_slots[0]
