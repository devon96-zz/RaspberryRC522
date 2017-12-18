import RPi.GPIO as GPIO
import time
import SimpleMFRC522

OPEN = 5
CLOSED = 10


class Lock:
    def __init__(self):
        self.status = 1
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(18, GPIO.OUT)
        self.p = GPIO.PWM(18, 50)
        self.p.start(5)
        time.sleep(1)

    def change_lock_position(self):
        duty = 0
        if self.status == 1:
            duty = 10
            self.status = 0
        else:
            duty = 5
            self.status = 1

        self.p.ChangeDutyCycle(duty)
        time.sleep(1)


class NFCReader:
    def __init__(self):
        self.reader = SimpleMFRC522.SimpleMFRC522()

    def read(self):
        text = self.reader.read()[1]
        return text


lock = Lock()
reader = NFCReader()

while True:
    try:
        card_content = reader.read().strip()
        if card_content == "Open!":
            lock.change_lock_position()
            print "Card accepted!\n"
        else:
            print "WRONG CARD!\n"
    except KeyboardInterrupt:
        GPIO.cleanup()
