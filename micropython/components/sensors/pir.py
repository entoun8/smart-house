from machine import Pin
import config

class PIR:
    """Motion sensor"""
    def __init__(self):
        self.pin = Pin(config.PIR_SENSOR_PIN, Pin.IN)

    def motion_detected(self):
        return self.pin.value() == 1
