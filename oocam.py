from cam_scheduler.scheduler import CameraConfig
import logging
import logging_config
from camera import Camera
from subsealight import SubseaLight
from sensors import PressureSensor
from sensors import TemperatureSensor
from sensors import LuminositySensor
from cam_scheduler import ScheduleFrame


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

    def capture_image(self, camera_config: CameraConfig):
        self.subsealight.switch_on(camera_config.light)
        self.camera.set_camera_params(camera_config)
        self.camera.capture()
        luminosity = self.luminosity_sensor.luminosity()
        temperature = self.temperature_sensor.temperature()
        pressure = self.pressure_sensor.pressure()
        logging.info(
            f"Sensor readings: Lum: {luminosity}, Temp: {temperature}, Pressure: {pressure}"
        )

    def start_video_capture(self, frame: ScheduleFrame):
        self.subsealight.switch_on(frame.camera_config.light)
        luminosity = self.luminosity_sensor.luminosity()
        temperature = self.temperature_sensor.temperature()
        pressure = self.pressure_sensor.pressure()
        logging.info(
            f"Sensor readings: Lum: {luminosity}, Temp: {temperature}, Pressure: {pressure}"
        )
        self.camera.start_recording()

    def stop_video_capture(self):
        self.camera.stop_recording()
