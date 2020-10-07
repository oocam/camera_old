from oocam import OpenOceanCamera


class UserInterface:
    oocam: OpenOceanCamera

    def __init__(self, oocam) -> None:
        self.oocam = oocam

    def send_photo(self) -> None:
        if self.oocam.camera.thread_lock.locked():
            return None
        else:
            self.oocam.camera.capture()

    def send_video_stream(self):
        pass

