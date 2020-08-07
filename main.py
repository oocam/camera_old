import logging
import logging_config
from camera import Camera
from subsealight import SubseaLight
from sensors import PressureSensor
from sensors import TemperatureSensor
from sensors import LuminositySensor
from appserver import start_server
import threading


class OpenOceanCamera:
    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self.pressure_sensor = PressureSensor()
        self.temperature_sensor = TemperatureSensor()
        self.luminosity_sensor = LuminositySensor()
        self.subsealight = SubseaLight()


def main():
    appserver_thread = threading.Thread(target=start_server)
    scheduler_thread = threading.Thread()
    appserver_thread.start()

    appserver_thread.join()


if __name__ == "__main__":
    main()
