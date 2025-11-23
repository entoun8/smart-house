from machine import Pin
import config

class Fan:
    def __init__(self):
        self.pin1 = Pin(config.FAN_PIN1, Pin.OUT)
        self.pin2 = Pin(config.FAN_PIN2, Pin.OUT)
        self.state = False

    def on(self):
        self.pin1.on()
        self.pin2.off()
        self.state = True

    def off(self):
        self.pin1.off()
        self.pin2.off()
        self.state = False

    def reverse(self):
        self.pin1.off()
        self.pin2.on()
        self.state = True
