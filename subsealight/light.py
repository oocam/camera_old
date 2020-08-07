import datetime
import logging
import sys

try: 
    import RPi.GPIO as GPIO
except: 
    print("Try pip intsall RPi.GPIO")

light_logger = logging.getLogger(__name__)

class SubseaLight:
    def __init__(self, pinout=24):
        self.pinout = pinout
        self.mode = GPIO.setmode(GPIO.BCM)
        self.pwm = GPIO.PWM(self.pinout, 500)
        self.setup = GPIO.setup(self.pintout, GPIO.OUT)

    def switch_off(self):
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()

    def switch_on(self, dc):
        light_logger.info(f"Light has been switched to a duty cycle of {dc}.")
        self.pwm.start(dc)

if __name__ == "__main__":
    current_time = datetime.datetime.now()
    un_until = current_time + datetime.timedelta(0, 5)
    switch_on(40)

    while datetime.datetime.now() < run_until:
        pass
    self.switch_off()
