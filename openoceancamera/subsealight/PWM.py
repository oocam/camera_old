import RPi.GPIO as GPIO
import datetime
import sys

GPIO.setwarnings(False)
# originally 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
pwm = GPIO.PWM(24, 67)  # PIN 12 = Board 32


def switch_off():
    pwm.ChangeDutyCycle(0)
    pwm.stop()


def switch_on(dc):
    print(dc)
    pwm.start(dc)


if __name__ == "__main__":
    x = datetime.datetime.now()
    y = x + datetime.timedelta(0, 5)
    while datetime.datetime.now() < y:
        switch_on(100)
    switch_off()
