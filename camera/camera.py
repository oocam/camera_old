from cam_scheduler.scheduler import CameraConfig
import logging
from threading import Lock
from uuid import uuid1

camera_logger = logging.getLogger(__name__)


class CameraLibraryNotFoundError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


try:
    from picamera import PiCamera
except:
    camera_logger.error(
        "picamera package was not found. will not use Raspberry Pi camera"
    )
    raise CameraLibraryNotFoundError(
        "Library for picamera does not exist. Are you running this code on the Raspberry Pi?"
    )


class Camera(PiCamera):
    def __init__(self, resolution=(3200, 2400), shutter_speed=5000, iso=0, frequency=3):
        super().__init__()
        self.set_camera_resolution(resolution)
        self.set_shutter_speed(shutter_speed)
        self.set_iso(iso)
        self.set_capture_frequency(frequency)
        self.thread_lock = Lock()

    def set_camera_params(self, config: CameraConfig):
        self.set_camera_resolution(config.camera_resolution)
        self.set_shutter_speed(config.shutter_speed)
        self.set_iso(config.iso)
        self.set_capture_frequency(config.frequency)

    def capture(self, filename=str(uuid1()) + ".jpg"):
        self.thread_lock.acquire()
        super().capture(filename)
        self.close()

    def start_recording(self, filename=str(uuid1()) + ".h264"):
        self.thread_lock.acquire()
        super().start_recording(filename, format="h264")

    def stop_recording(self):
        if self.recording():
            super().stop_recording()

    def close(self):
        self.stop_recording()
        super().close()
        self.thread_lock.release()

    def retrieve_params(self):
        print("Resolution:", super().resolution)
        print("Shutter speed:", super().shutter_speed)
        print("ISO:", super().iso)

    def set_camera_frame_rate(self, fr):
        super().framerate = fr

    def set_camera_resolution(self, resolution):
        super().resolution = resolution

    def set_shutter_speed(self, speed=0):
        super().shutter_speed = speed

    def set_iso(self, iso):
        super().iso = iso

    def set_capture_frequency(self, frequency):
        self.frequency = frequency

    def recording(self):
        return super().recording
