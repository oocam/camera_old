import datetime
import logging
import sys

light_logger = logging.getLogger(__name__)


class SubSeaLightLibraryNotFoundError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


try:
    import RPi.GPIO as GPIO
except:
    light_logger.error("Try pip intsall RPi.GPIO")
    raise SubSeaLightLibraryNotFoundError("Try pip intsall RPi.GPIO")


class SubseaLight:
    def __init__(self, pinout=24):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinout, GPIO.OUT)
        self.pwm = GPIO.PWM(pinout, 500)

    def switch_off(self):
        light_logger.info("Light has been switched to a duty cycle of 0.")
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()
        light_logger.info("Light has been switched off.")

    def switch_on(self, dc):
        light_logger.info(f"Light has been switched to a duty cycle of {dc}.")
        self.pwm.start(dc)


if __name__ == "__main__":
    current_time = datetime.datetime.now()
    run_until = current_time + datetime.timedelta(0, 5)  # Turn light on for 5 minutes
    sslight = SubseaLight()
    # Turn light on
    sslight.switch_on(100)
    while datetime.datetime.now() < run_until:
        pass
    sslight.switch_off()
