import RPi.GPIO as GPIO
import time

class Lock:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.OUT)
        self.p = GPIO.PWM(18,50)
        self.p.start(5)

    def change_lock_position(self, angle):
        duty = float(angle) / 10.0 + 2.5
        self.p.ChangeDutyCycle(duty)
        time.sleep(2)

lock = Lock()
for i in range(0,180,15):
    lock.change_lock_position(i)