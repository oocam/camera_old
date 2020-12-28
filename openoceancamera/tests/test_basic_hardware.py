import pytest 
import os 
from picamera import PiCamera 

class TestBasicHardware: 
    external_drive = "/media/pi/OPENOCEANCA"

    def test_mounting(self): 
       assert os.path.ismount(self.external_drive)==True

    def test_write_to_mount_point(self): 
        assert os.access(self.external_drive, os.W_OK)==True 

    def test_open_camera(self): 
        camera = PiCamera()
        camera.close()

