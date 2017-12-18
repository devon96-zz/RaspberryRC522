import RPi.GPIO as GPIO
import time
import SimpleMFRC522
import pigpio


class Lock:
    def __init__(self):
        self.status = 1
        self.pi = pigpio.pi()

    def change_lock_position(self):
        duty = 0
        if self.status == 1:
            duty = 1000
            self.status = 0
        else:
            duty = 2000
            self.status = 1

        self.pi.set_servo_pulsewidth(18, duty)
        time.sleep(0.5)
        self.pi.set_servo_pulsewidth(18, 0)
        self.pi.stop()


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
            print "CARD ACCEPTED!\n"
            lock.change_lock_position()
        else:
            print "WRONG CARD!\n"
    except KeyboardInterrupt:
        GPIO.cleanup()
