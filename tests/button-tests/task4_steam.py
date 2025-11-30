import time
from machine import Pin
from components import WindowServo, WiFi
from components.connectivity.mqtt_wrapper import MQTTWrapper
from tasks.rgb_controller import RGBController
from config import TOPICS

wifi = WiFi()
wifi.connect()

mqtt = MQTTWrapper()
mqtt_connected = mqtt.connect()

window = WindowServo()
rgb = RGBController()
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

window.open()
rgb.off()

steam_active = False
last_press = 0

while True:
    if btn_right.value() == 0:
        rgb.off()
        window.open()
        if mqtt_connected:
            mqtt.publish(TOPICS.device_state("window"), "open")
            time.sleep(0.5)  # Wait for message to be sent
            mqtt.disconnect()
        break

    if time.time() - last_press < 2:
        time.sleep(0.1)
        continue

    if btn_left.value() == 0:
        last_press = time.time()

        if not steam_active:
            window.close()
            rgb.set_rgb("steam", rgb.rgb.blue)
            if mqtt_connected:
                mqtt.publish(TOPICS.device_state("window"), "close")
            steam_active = True
        else:
            window.open()
            rgb.clear_rgb("steam")
            if mqtt_connected:
                mqtt.publish(TOPICS.device_state("window"), "open")
            steam_active = False

    time.sleep(0.1)
