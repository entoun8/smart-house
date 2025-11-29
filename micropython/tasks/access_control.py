import time
from machine import Pin, PWM
from components import RFID, Buzzer
from config import TOPICS
import config

SCAN_COOLDOWN = 3  

AUTHORIZED_CARD = "0x7cdab502"  

class AccessControlTask:
    def __init__(self, mqtt, rgb_controller):
        self.rfid = RFID()
        self.buzzer = Buzzer()
        self.door_pwm = PWM(Pin(config.DOOR_SERVO_PIN), freq=50)
        self.door_close()  
        self.mqtt = mqtt
        self.rgb = rgb_controller
        self.last_card = None
        self.last_scan = 0

    def door_open(self):
        self.door_pwm.duty(128)  

    def door_close(self):
        self.door_pwm.duty(26)   

    def update(self):
        card_id = self.rfid.scan()
        now = time.time()

        if card_id and (card_id != self.last_card or now - self.last_scan > SCAN_COOLDOWN):
            self.last_card = card_id
            self.last_scan = now

            if card_id == AUTHORIZED_CARD:
                mqtt_msg = f'{{"card":"{card_id}","status":"authorized"}}'
                mqtt_topic = TOPICS.event("rfid_scan")
                result = self.mqtt.publish(mqtt_topic, mqtt_msg)

                self.rgb.rgb.green()
                self.door_open()
                self.mqtt.publish(TOPICS.device_state("door"), "open")
                time.sleep(3)
                self.door_close()
                self.mqtt.publish(TOPICS.device_state("door"), "close")
                self.rgb.rgb.off()

            else:
                mqtt_msg = f'{{"card":"{card_id}","status":"unauthorized"}}'
                mqtt_topic = TOPICS.event("rfid_scan")
                result = self.mqtt.publish(mqtt_topic, mqtt_msg)

                for _ in range(3):
                    self.rgb.rgb.red()
                    self.buzzer.on()
                    time.sleep(0.2)
                    self.rgb.rgb.off()
                    self.buzzer.off()
                    time.sleep(0.2)

    def cleanup(self):
        self.buzzer.off()
        self.door_close()
        self.door_pwm.deinit()
