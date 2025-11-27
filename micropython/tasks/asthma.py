from config import TOPICS

class AsthmaTask:
    def __init__(self, mqtt, lcd, temp_task):
        self.mqtt = mqtt
        self.lcd = lcd
        self.temp_task = temp_task  
        self.previous = False

    def _check_conditions(self, temp, humidity):
        return humidity > 50 and temp > 27

    def update(self):
        data = self.temp_task.get_last_data()
        if not data:
            return

        temp = data['temp']
        humidity = data['humidity']
        alert = self._check_conditions(temp, humidity)

        if alert and not self.previous:
            if self.lcd and self.lcd.is_connected():
                self.lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")
            self.mqtt.publish(TOPICS.event("asthma_alert"), "1")

        elif not alert and self.previous:
            if self.lcd and self.lcd.is_connected():
                self.lcd.display_alert(f"Temp: {temp}C", f"Humidity: {humidity}%")
            self.mqtt.publish(TOPICS.event("asthma_alert"), "0")

        self.previous = alert

    def cleanup(self):
        pass
