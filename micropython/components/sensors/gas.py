from machine import Pin
import config


class GasSensor:
    """Gas sensor (digital output)"""
    def __init__(self):
        self.pin = Pin(config.GAS_SENSOR_PIN, Pin.IN, Pin.PULL_UP)

    def read(self):
        return self.pin.value()

    def is_detected(self, threshold=0):
        # Try inverted logic: 1 = gas detected
        return self.read() == 1  
