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
        self.camera = Camera()
        self.pressure_sensor = PressureSensor().pressure()
        self.temperature_sensor = TemperatureSensor().temperature()
        self.luminosity_sensor = LuminositySensor().luminosity()
        self.subsealight = SubseaLight()


def main():
    appserver_thread = threading.Thread(target=start_server)
    scheduler_thread = threading.Thread()
    appserver_thread.start()

    appserver_thread.join()

    print("Main started")

    while True:
        sleep(2)
        camera = Camera()
        if appserver_thread.isAlive():
            camera_configuration = server.app_connect()
            my_schedule = Scheduler(camera_configuration)
            print("Loaded Scheduler. Main thread acive")
            switch_flag = 0
            isrecord = 0
            isopen = 0

            # Stall the camera to let it initialise
            while appserver_thread.isAlive():
                '''
                make functions listed below (scheduler.py, class Scheduler)
                my_schedule.update_current_time()
                slot = my_schedule.should_start()
                '''
                if slot == -1 and isrecord == 0:
                    sleep(2)

                if isrecord == 1 and slot == -1:
                    PWM.switch_off()
                    camera.close()
                    print("CLOSED")
                    isrecord = 0
                    isopen = 0
                
                if slot >= 0:  # if slot open
                    if isopen == 0:
                        try:
                            camera = Camera()
                        except Exception as e:
                            print(e)
                        isopen = 1

                    # Write Sensors data to log.txt
                    log_filename = f"{external_drive}/log.txt"
                    sensor_data = ReadSensorData(log_filename, OpenOceanCamera.pressure_sensor, 
                                    OpenOceanCamera.temperature_sensor, OpenOceanCamera.luminosity_sensor)
                    sensor_data.write_data()

                    
                    camera.set_capture_frequency()
                    camera.set_iso()
                    camera.set_shutter_speed()
                    
        


if __name__ == "__main__":
    main()
