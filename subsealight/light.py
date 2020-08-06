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
        self.pwm.setup = GPIO.setup(self.pintout, GPIO.OUT)

    def switch_off():
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()

    def switch_on(dc):
        logger.info(f"Light has been switched to a duty cycle of {dc}.")
        self.pwm.start(dc)

    def main():
        current_time = datetime.datetime.now()
        run_until = current_time + datetime.timedelta(0, 5)
        switch_on(40)

        while datetime.datetime.now() < run_until:
            pass
        switch_off()

if __name__ == "__main__":
    main()
