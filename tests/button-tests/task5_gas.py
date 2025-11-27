import time
from machine import Pin
from components import Fan, WiFi
from components.connectivity.mqtt_wrapper import MQTTWrapper
from tasks.rgb_controller import RGBController
from config import TOPICS

fan = Fan()
rgb = RGBController()
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

wifi = WiFi()
wifi.connect()

mqtt = MQTTWrapper()
mqtt_connected = mqtt.connect()

fan.off()
rgb.off()

gas_active = False
last_press = 0

while True:
    if btn_right.value() == 0:
        fan.off()
        rgb.off()
        if mqtt_connected:
            mqtt.publish(TOPICS.event("gas_detected"), "0")
            mqtt.publish(TOPICS.device_state("fan"), "off")
            mqtt.disconnect()
        break

    if time.time() - last_press < 2:
        time.sleep(0.1)
        continue

    if btn_left.value() == 0:
        last_press = time.time()

        if not gas_active:
            fan.on()
            rgb.set_rgb("gas", rgb.rgb.red)

            if mqtt_connected:
                mqtt.publish(TOPICS.event("gas_detected"), "1")
                mqtt.publish(TOPICS.device_state("fan"), "on")

            gas_active = True
        else:
            fan.off()
            rgb.clear_rgb("gas")

            if mqtt_connected:
                mqtt.publish(TOPICS.event("gas_detected"), "0")
                mqtt.publish(TOPICS.device_state("fan"), "off")

            gas_active = False

    time.sleep(0.1)
