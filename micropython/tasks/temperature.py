import time
from components import DHT
from config import TOPICS
import json

LOG_INTERVAL = 900  

class TemperatureTask:
    def __init__(self, mqtt, lcd=None):
        self.dht = DHT()
        self.mqtt = mqtt
        self.lcd = lcd
        self.last_log = None
        self.last_data = None

    def update(self):
        now = time.time()
        if self.last_log is not None and now - self.last_log < LOG_INTERVAL:
            return None

        data = self.dht.read()
        if not data:
            return None

        temp = data['temp']
        humidity = data['humidity']

        climate_data = json.dumps({"temp": temp, "humidity": humidity})
        self.mqtt.publish(TOPICS.sensor("climate"), climate_data)

        self.last_log = now
        self.last_data = data
        return data

    def get_last_data(self):
        return self.last_data

    def cleanup(self):
        pass
