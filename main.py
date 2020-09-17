import logging
import logging_config
import threading
from oocam import OpenOceanCamera
from appserver import start_server, server
from cam_scheduler import Scheduler


def command_executor():
    pass


def main():
    appserver_thread = threading.Thread(target=start_server)
    scheduler_thread = threading.Thread()
    appserver_thread.start()
    # Create a camera instance to manage the different operations of the camera
    camera = OpenOceanCamera()
    scheduler = Scheduler()
    while True:
        pass
    appserver_thread.join()


if __name__ == "__main__":
    main()
