import RPi.GPIO as GPIO
import datetime
import sys

GPIO.setwarnings(False)
# originally 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
pwm = GPIO.PWM(24, 900)  # PIN 12 = Board 32


def switch_off():
    pwm.ChangeDutyCycle(0)
    pwm.stop()


def switch_on(mode):
    if mode == 1:
        dc = 67
    elif mode == 2:
        dc = 60
    elif mode == 3:
        dc = 55
    elif mode == 4:
        dc = 53
    elif mode == 5:
        dc = 40

    print(dc)
    pwm.start(dc)


if __name__ == "__main__":
    x = datetime.datetime.now()
    y = x + datetime.timedelta(0, 5)
    while datetime.datetime.now() < y:
        switch_on(1)
    switch_off()
