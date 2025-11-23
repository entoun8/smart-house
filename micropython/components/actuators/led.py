from machine import Pin
import time
import config

class LED:
    def __init__(self):
        self.pin = Pin(config.LED_PIN, Pin.OUT)
        self.state = False

    def on(self):
        self.pin.on()
        self.state = True

    def off(self):
        self.pin.off()
        self.state = False

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()

    def blink(self, times=1, delay=0.5):
        for _ in range(times):
            self.on()
            time.sleep(delay)
            self.off()
            time.sleep(delay)
