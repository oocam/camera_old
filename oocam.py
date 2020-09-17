import logging
import logging_config
from camera import Camera
from subsealight import SubseaLight
from sensors import PressureSensor
from sensors import TemperatureSensor
from sensors import LuminositySensor
from sensors import ReadSensorData


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

    def start_video_capture(self):
        pass

    def stop_video_capture(self):
        pass
