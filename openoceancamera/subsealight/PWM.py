import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm = GPIO.PWM(11, 67)


def switch_off():
    pwm.ChangeFrequency(0)
    pwm.stop()
    GPIO.cleanup(11)


def switch_on(mode):
    if mode == 1:
        freq = 67
    elif mode == 2:
        freq = 60
    elif mode == 3:
        freq = 55
    elif mode == 4:
        freq = 53
    elif mode == 5:
        freq = 40

    pwm.ChangeFrequency(freq)
