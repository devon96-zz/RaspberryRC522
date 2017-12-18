import RPi.GPIO as GPIO
import time
from random import randint
import SimpleMFRC522

class Lock:
    def init_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.OUT)
        self.p = GPIO.PWM(18,50)
        self.p.start(5)

    def change_lock_position(self, angle):
        self.init_gpio()
        time.sleep(1)
        duty = float(angle) / 10.0 + 2.5
        self.p.ChangeDutyCycle(duty)
        time.sleep(1)

class NFCReader:
    def __init__(self):
        self.reader = SimpleMFRC522.SimpleMFRC522()

    def read(self):
        try:
            id, text = self.reader.read()
            print(id)
            print(text)
        finally:
            GPIO.cleanup()

lock = Lock()
reader = NFCReader()

while True:
    reader.read()
    lock.change_lock_position(randint(0,90))
