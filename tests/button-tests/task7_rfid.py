import time
import sys
sys.path.append('/lib')
from machine import Pin, PWM
from components import Buzzer, RGBStrip, WiFi, MQTT
from mfrc522_i2c import MFRC522_I2C
from config import TOPICS
import config

buzzer = Buzzer()
rgb = RGBStrip()
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

door_pwm = PWM(Pin(config.DOOR_SERVO_PIN), freq=50)

def door_open():
    door_pwm.duty(128)

def door_close():
    door_pwm.duty(26)

rfid = MFRC522_I2C(scl=22, sda=21, addr=0x28)

wifi = WiFi()
wifi.connect()

mqtt = MQTT()
mqtt_connected = False
try:
    mqtt_connected = mqtt.connect()
except:
    pass

door_close()
buzzer.off()
rgb.off()

AUTHORIZED_CARD = "0x7cdab502"
DENIED_CARD = "0x5a6e25b6"

last_card = None
last_scan_time = 0

while True:
    if btn_left.value() == 0 and btn_right.value() == 0:
        door_close()
        buzzer.off()
        rgb.off()
        door_pwm.deinit()
        if mqtt_connected:
            mqtt.disconnect()
        break

    card_id = rfid.scan()

    if card_id:
        current_time = time.time()
        if card_id != last_card or (current_time - last_scan_time) > 3:
            last_card = card_id
            last_scan_time = current_time

            if card_id == AUTHORIZED_CARD:
                if mqtt_connected:
                    mqtt.publish(TOPICS.event("rfid_scan"),
                        f'{{"card":"{card_id}","status":"authorized"}}')

                rgb.green()
                door_open()
                if mqtt_connected:
                    mqtt.publish(TOPICS.device_state("door"), "open")

                time.sleep(3)

                door_close()
                if mqtt_connected:
                    mqtt.publish(TOPICS.device_state("door"), "close")
                rgb.off()

            else:
                if mqtt_connected:
                    mqtt.publish(TOPICS.event("rfid_scan"),
                        f'{{"card":"{card_id}","status":"unauthorized"}}')

                for _ in range(3):
                    rgb.red()
                    buzzer.on()
                    time.sleep(0.2)
                    rgb.off()
                    buzzer.off()
                    time.sleep(0.2)

    time.sleep(0.1)
