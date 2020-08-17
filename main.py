import logging
import logging_config

from camera import Camera

from subsealight import SubseaLight

from sensors import PressureSensor
from sensors import TemperatureSensor
from sensors import LuminositySensor
from sensors import ReadSensorData

from appserver import start_server, server

from cam_scheduler import Scheduler

import threading


class OpenOceanCamera:
    def __init__(self):
        super().__init__()
        # Camera Modules
        self.camera = Camera()
        # Subsealight Modules
        self.subsealight = SubseaLight()
        # Sensors Modules
        self.pressure_sensor = PressureSensor()
        self.temperature_sensor = TemperatureSensor()
        self.luminosity_sensor = LuminositySensor()

    def capture_image(self, filename, light_intensity, iso, shutter_speed, resolution):
        self.subsealight.switch_on(light_intensity)
        self.camera.capture(filename)
        luminosity = self.luminosity_sensor.luminosity()
        temperature = self.temperature_sensor.temperature()
        pressure = self.pressure_sensor.pressure()

        logging.info(
            f"Readings while capturing image: Luminosity: {luminosity} lux, Temperature: {temperature}, Pressure: {pressure}"
        )

    def start_video_capture(self):
        pass

    def stop_video_capture(self):
        pass


def main():
    appserver_thread = threading.Thread(target=start_server)
    scheduler_thread = threading.Thread()
    appserver_thread.start()

    # Create a camera instance to manage the different operations of the camera
    try:
        camera = OpenOceanCamera()
        logging.info("Camera is Connected")
    except Exception as e:
        logging.error(e)

    appserver_thread.join()


if __name__ == "__main__":
    main()
