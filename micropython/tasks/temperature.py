"""Task 2: Temperature Logging (every 30 min) -> MQTT"""

import time
from components import DHT
from config import TOPICS

LOG_INTERVAL = 1800  # 30 minutes


class TemperatureTask:
    def __init__(self, mqtt, lcd=None):
        self.dht = DHT()
        self.mqtt = mqtt
        self.lcd = lcd
        self.last_log = 0
        self.last_data = None

    def update(self):
        """Read and publish temperature - call this in main loop"""
        now = time.time()
        if self.last_log != 0 and now - self.last_log < LOG_INTERVAL:
            return None

        data = self.dht.read()
        if not data:
            print("[Temp] Read failed")
            return None

        temp = data['temp']
        humidity = data['humidity']
        print(f"[Temp] {temp}C, {humidity}%")

        # Publish to MQTT
        self.mqtt.publish(TOPICS.sensor("temperature"), str(temp))
        self.mqtt.publish(TOPICS.sensor("humidity"), str(humidity))

        # Update LCD if available
        if self.lcd:
            print(f"[Temp] LCD connected: {self.lcd.is_connected()}")
            if self.lcd.is_connected():
                self.lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")
                print("[Temp] LCD updated")

        self.last_log = now
        self.last_data = data
        return data

    def get_last_data(self):
        """Get last temperature reading (for asthma task)"""
        return self.last_data

    def cleanup(self):
        pass
