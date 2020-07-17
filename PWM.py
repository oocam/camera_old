
import RPi.GPIO as GPIO 
import time 
import sys

#Input: mode (int range 1-5), minutes (int)
#Duty cycle: percentage of time the signal is on 

if len(sys.argv) > 3:
  sys.exit("Error: More than two inputs received.")
if int(sys.argv[1]) < 1 or int(sys.argv[1]) > 5:
  sys.exit("Modes range from 1-5.")

mode = str(sys.argv[1])
run_time = int(sys.argv[2])

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm = GPIO.PWM(11, 67)

end_time = time.time() + 60 * run_time

if mode == '1':
  freq = 67
elif mode == '2':
  freq = 60
elif mode == '3':
  freq = 55
elif mode == '4':
  freq = 53
elif mode == '5':
  freq = 40

pwm.ChangeFrequency(freq)

while time.time() < end_time: 
  pwm.start(7.5) 
  
pwm.stop()
GPIO.cleanup(11)
