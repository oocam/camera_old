import io
import time
import picamera
from base_camera import BaseCamera 


class Camera_Pi(BaseCamera):
    def __init__(self, time_duration=0):
        super().__init__(time_duration)
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:

            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):

                stream.seek(0)
                yield stream.read()
                
                stream.seek(0)
                stream.truncate()
