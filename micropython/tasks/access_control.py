import time
from components import RFID, Buzzer, DoorServo
from config import TOPICS

SCAN_COOLDOWN = 3

AUTHORIZED_CARD = "0x7cdab502"

class AccessControlTask:
    def __init__(self, mqtt, rgb_controller):
        self.rfid = RFID()
        self.buzzer = Buzzer()
        self.door = DoorServo()
        self.door.close()
        self.mqtt = mqtt
        self.rgb = rgb_controller
        self.last_card = None
        self.last_scan = 0   

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
                self.door.open()
                self.mqtt.publish(TOPICS.device_state("door"), "open")
                time.sleep(3)
                self.door.close()
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
        self.door.close()
