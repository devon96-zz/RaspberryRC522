import RPi.GPIO as GPIO
import time

def change_lock_position(angle):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    p = GPIO.PWM(18,50)
    p.start(7.5)
    duty = float(angle) / 10.0 + 2.5
    p.ChangeDutyCycle(duty)

change_lock_position(90)
time.sleep(1)
change_lock_position(0)
time.sleep(0)