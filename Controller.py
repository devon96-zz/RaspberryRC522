import RPi.GPIO as GPIO
import time
import SimpleMFRC522

OPEN = 7
CLOSED = 0

class Lock:
    status = 0
    def init_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18,GPIO.OUT)
        self.p = GPIO.PWM(18,50)
        self.p.start(0)

    def change_lock_position(self):
        self.init_gpio()
        time.sleep(1)

        duty = 0
        if self.status:
            duty = CLOSED
            self.status = 0
        else:
            duty = OPEN
            self.status = 1

        self.p.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.cleanup()

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
            return text

lock = Lock()
reader = NFCReader()

while True:
    card_content = reader.read().strip()
    if card_content=="Open!":
        lock.change_lock_position()
    else:
        print "WRONG CARD!"
