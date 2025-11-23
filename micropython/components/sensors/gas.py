from machine import Pin
import config


class GasSensor:
    def __init__(self):
        self.pin = Pin(config.GAS_SENSOR_PIN, Pin.IN)

    def read(self):
        return self.pin.value()

    def is_detected(self):
        return self.read() == 0  
