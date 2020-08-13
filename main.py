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
    def __init__(self, record_filename, dc=0):
        super().__init__()

        # Camera Modules
        self.camera = Camera()
        self.capture = self.camera.capture()
        self.start_recording = self.camera.start_record(record_filename)
        self.stop_recording = self.camera.stop_recording()
        self.shutdown = self.camera.close()
        self.retrive_camera_parameter = self.camera.retrieve_params()
        self.set_camera_fr = self.camera.set_camera_frame_rate()
        self.set_camera_resolution = self.camera.set_camera_resolution()
        self.set_shutter_speed = self.camera.set_shutter_speed()
        self.set_iso = self.camera.set_iso()
        self.set_capture_frequency = self.camera.set_capture_frequency()
        
        # Subsealight Modules
        self.subsealight = SubseaLight()
        self.turn_on_light = self.subsealight.switch_on(dc)
        self.turn_off_light = self.subsealight.switch_off()

        # Sensors Modules
        self.pressure_sensor = PressureSensor()
        self.temperature_sensor = TemperatureSensor()
        self.luminosity_sensor = LuminositySensor()


   

def main():
    appserver_thread = threading.Thread(target=start_server)
    scheduler_thread = threading.Thread()
    appserver_thread.start()

    appserver_thread.join()

    try:
        camera = OpenOceanCamera.camera
        logging.info("Camera is Connected")
    except Exception as e:
        logging.error(e)

    try:
        pressure_sensor = OpenOceanCamera.pressure_sensor
        logging.info("Pressure sensor is Connected")
    except Exception as e:
        logging.error(e)

    try:
        temperature_sensor = OpenOceanCamera.temperature_sensor
        logging.info("Temperature sensor is Connected")
    except Exception as e:
        logging.error(e)

    try:
        luminosity_sensor = OpenOceanCamera.luminosity_sensor
        logging.info("Luminosity sensor is Connected")
    except Exception as e:
        logging.error(e)

    try:
        subsealight= OpenOceanCamera.subsealight
        logging.info("subsealight is Connected")
    except Exception as e:
        logging.error(e)

    # Start recording
    


    
        


if __name__ == "__main__":
    main()
