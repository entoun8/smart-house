from machine import Pin
import config


class DHT:
    """Temperature & humidity sensor"""
    def __init__(self):
        import dht
        self.sensor = dht.DHT11(Pin(config.DHT_PIN))

    def read(self):
        try:
            self.sensor.measure()
            return {
                'temp': self.sensor.temperature(),
                'humidity': self.sensor.humidity()
            }
        except:
            return None
