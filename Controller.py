import RPi.GPIO as GPIO
import time
import sys
import SimpleMFRC522
import pigpio


class Lock:
    def move_lock(self, degrees):
        pi = pigpio.pi()
        duty = int((degrees / 180.0) * 1850.0 + 500.0)
        pi.set_servo_pulsewidth(18, duty)
        time.sleep(0.5)
        pi.set_servo_pulsewidth(18, 0)
        pi.stop()
        GPIO.cleanup()


class NFCReader:
    def __init__(self):
        self.reader = SimpleMFRC522.SimpleMFRC522()

    def read_id(self):
        text = self.reader.read()[0]
        return text
