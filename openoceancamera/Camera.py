try:
    from picamera import PiCamera
    from time import sleep,time
    from datetime import datetime
except:
    print(
        "Program is not running on a Raspberry Pi. The camera module cannot be loaded"
    )
    exit(0)


class Camera(object):
    def __init__(self, resolution=(1920, 1080), shutter_speed=5000, iso=0, frequency=3):
        self.camera = PiCamera()
        self.set_camera_resolution(resolution)
        self.set_shutter_speed(shutter_speed)
        self.set_iso(iso)
        self.set_capture_frequency(frequency)

    def do_capture(self, filename="test.jpg", continuous=False, slot=None):
        if continuous:
            #try:
            #    for f in self.camera.capture_continuous('/media/pi/OPENOCEANCA/img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
            #        sleep((self.frequency-1))
            #        print (f)
            #        currenttime=datetime.now()
            #        if currenttime<datetime.strptime(slot["stop"],"%Y-%m-%d-%H:%M:%S"):
            #            pass
            #        else:
            #            break
            #except Exception as err:
            #    print(err)
            pass
        else:
            try:
                print("Going to capture in Camera")
                self.camera.capture(filename)
                print("Done capturing", filename)
            except Exception as err:
                print(err)

    def do_record(self, filename):
        self.camera.start_recording(filename, format="h264")
        self.recording = True

    def stop_recording(self):
        if self.check_recording():
            self.camera.stop_recording()

    def do_close(self):
        self.stop_recording()
        self.camera.close()

    def retrieve_params(self):
        print("Resolution:", self.camera.resolution)
        print("Shutter speed:", self.camera.shutter_speed)
        print("ISO:", self.camera.iso)

    def set_camera_frame_rate(self, fr):
        self.camera.framerate = fr

    def set_camera_resolution(self, resolution):
        self.camera.resolution = resolution

    def set_shutter_speed(self, speed=0):
        self.camera.shutter_speed = speed

    def set_iso(self, iso):
        self.camera.iso = iso

    def set_capture_frequency(self, frequency):
        self.frequency = frequency

    def check_recording(self):
        return self.camera.recording

    def set_camera_exposure_mode(self, mode):
        self.camera.exposure_mode = mode

    def set_camera_exposure_compensation(self, compensation):
        self.camera.exposure_compensation = compensation
