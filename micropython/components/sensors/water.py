from machine import Pin, ADC
import config

class WaterSensor:
    """Water/steam sensor"""
    def __init__(self):
        self.adc = ADC(Pin(config.WATER_SENSOR_PIN))
        self.adc.atten(ADC.ATTN_11DB)

    def read(self):
        return self.adc.read()

    def is_wet(self, threshold=2000):
        return self.read() > threshold
