import logging
import logging_config
import threading
from oocam import OpenOceanCamera
from constants import SCHEDULE_FILE_PATH
from appserver import start_server, server
from cam_scheduler import Scheduler, ScheduleFrame, ShootingMode

scheduleSetterSignal = threading.Event()


def run(frame: ScheduleFrame, camera: OpenOceanCamera):
    if frame.camera_config.shooting_mode == ShootingMode.VIDEO:
        camera.start_video_capture()
    elif frame.camera_config.shooting_mode == ShootingMode.PHOTO:
        camera.capture_image(frame)


def unrun(frame: ScheduleFrame, camera: OpenOceanCamera):
    if frame.camera_config.shooting_mode == ShootingMode.VIDEO:
        camera.stop_video_capture()


def main():
    # appserver_thread = threading.Thread(target=start_server)
    # appserver_thread.start()
    # Create a camera instance to manage the different operations of the camera
    camera = OpenOceanCamera()
    scheduler = Scheduler(schedule_file=SCHEDULE_FILE_PATH)
    while True:
        frame: ScheduleFrame = scheduler.get_event_to_execute()
        if frame is not None:
            run(frame, camera)
            frame.set_executed()
            while frame.should_frame_run():
                pass
            unrun(frame, camera)
    # appserver_thread.join()


if __name__ == "__main__":
    main()
