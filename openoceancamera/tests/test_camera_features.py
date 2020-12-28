import pytest 
import os 
from ..Camera import Camera

class TestCamera: 
    def test_single_image_capture(self): 
        camera = Camera() 
        camera.do_capture("/home/pi/test1.jpg")
        camera.do_close()
        os.remove("/home/pi/test1.jpg")

    def test_write_image_to_usb(self): 
        camera = Camera() 
        camera.do_capture("/media/pi/OPENOCEANCA/test.jpg")
        camera.do_close()
        if os.path.isfile("/media/pi/OPENOCEANCA/test.jpg"):
            os.remove("/media/pi/OPENOCEANCA/test.jpg")
            pass 
        else: 
            raise Exception("Image was not written to the USB") 

    def test_capture_continuous_image(self): 
        

