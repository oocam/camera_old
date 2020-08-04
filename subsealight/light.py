import datetime
import logging
import RPi.GPIO as GPIO
import sys

logger = logging.getLogger(__name__)


def switch_off():
    pwm.ChangeDutyCycle(0)
    pwm.stop()


def switch_on(dc):
    logger.info(f"Light has been switched to a duty cycle of {dc}.")
    pwm.start(dc)


def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)
    pwm = GPIO.PWM(24, 500)

    current_time = datetime.datetime.now()
    run_until = current_time + datetime.timedelta(0, 5)
    switch_on(40)

    while datetime.datetime.now() < run_until:
        pass
    switch_off()


if __name__ == "__main__":
    main()
