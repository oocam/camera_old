from datetime import date, datetime


class Scheduler(object):
    def __init__(self, data):
        self.time_now = datetime.now()
        self.schedule_data = []
        self.load_scheduler_data(data)

    def update_current_time(self):
        self.time_now = datetime.now()

    def should_start(self):
        for i in range(len(self.schedule_data)):
            if self.schedule_data[i]["start"] <= self.time_now <= self.schedule_data[i]["stop"]:
                return i
        return (-1)

    def load_scheduler_data(self, data):
        for i in range(len(data)):
            frame = {
                "start": None,
                "stop": None,
            }
            frame["start"] = datetime.strptime(data[i]["start"], '%Y-%m-%d-%H:%M:%S')
            frame["stop"] = datetime.strptime(data[i]["stop"], '%Y-%m-%d-%H:%M:%S')
            self.schedule_data.append(frame.copy())
