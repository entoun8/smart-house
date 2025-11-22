"""Task 6: Asthma Alert (humidity >50% + temp >27C) -> MQTT + LCD"""

from config import TOPICS


class AsthmaTask:
    def __init__(self, mqtt, lcd, temp_task):
        self.mqtt = mqtt
        self.lcd = lcd
        self.temp_task = temp_task  # Reference to temperature task for data
        self.previous = False

    def _check_conditions(self, temp, humidity):
        """Asthma alert: humidity >50% AND temp >27C"""
        return humidity > 50 and temp > 27

    def update(self):
        """Check asthma conditions - call this in main loop"""
        data = self.temp_task.get_last_data()
        if not data:
            return

        temp = data['temp']
        humidity = data['humidity']
        alert = self._check_conditions(temp, humidity)

        if alert and not self.previous:
            print("[Asthma] ALERT! (H>50% & T>27C)")
            if self.lcd and self.lcd.is_connected():
                self.lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")
            self.mqtt.publish(TOPICS.event("asthma_alert"), "1")

        elif not alert and self.previous:
            print("[Asthma] Cleared")
            if self.lcd and self.lcd.is_connected():
                self.lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")
            self.mqtt.publish(TOPICS.event("asthma_alert"), "0")

        self.previous = alert

    def cleanup(self):
        pass
