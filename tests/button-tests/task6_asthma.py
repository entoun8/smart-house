import time
from machine import Pin
from components import LCD, WiFi
from components.connectivity.mqtt_wrapper import MQTTWrapper
from config import TOPICS

btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

time.sleep(0.5)
lcd = LCD()

wifi = WiFi()
wifi.connect()

mqtt = MQTTWrapper()
mqtt_connected = mqtt.connect()

if lcd.is_connected():
    lcd.display_alert("Temp: 25C", "Humidity: 45%")

alert_active = False
last_press = 0

while True:
    if btn_right.value() == 0:
        if lcd.is_connected():
            lcd.clear()
        if mqtt_connected:
            mqtt.publish(TOPICS.event("asthma_alert"), "0")
            mqtt.disconnect()
        break

    if time.time() - last_press < 2:
        time.sleep(0.1)
        continue

    if btn_left.value() == 0:
        last_press = time.time()

        if not alert_active:
            if lcd.is_connected():
                lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")

            if mqtt_connected:
                mqtt.publish(TOPICS.event("asthma_alert"), "1")

            alert_active = True
        else:
            if lcd.is_connected():
                lcd.display_alert("Temp: 25C", "Humidity: 45%")

            if mqtt_connected:
                mqtt.publish(TOPICS.event("asthma_alert"), "0")

            alert_active = False

    time.sleep(0.1)

