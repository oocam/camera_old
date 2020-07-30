import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
# originally 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
pwm = GPIO.PWM(24, 900)  # PIN 12 = Board 32


def switch_off():
    pwm.ChangeDutyCycle(0)
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

    pwm.ChangeDutyCycle(freq)


if __name__ == "__main__":
    for i in range(1, 5):
        switch_on(i)
        time.sleep(5)
        switch_off()
