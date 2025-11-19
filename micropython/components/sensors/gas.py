from machine import Pin
import config


class GasSensor:
    """Gas sensor (digital output)"""
    def __init__(self):
        self.pin = Pin(config.GAS_SENSOR_PIN, Pin.IN)

    def read(self):
        return self.pin.value()

    def is_detected(self, threshold=0):
        return self.read() == 0  
