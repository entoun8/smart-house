"""Task 7: RFID Access Control -> MQTT"""

import time
from components import RFID, Buzzer, DoorServo
from config import TOPICS

SCAN_COOLDOWN = 3  # Seconds between same card scans


class AccessControlTask:
    def __init__(self, mqtt, rgb_controller):
        self.rfid = RFID()
        self.buzzer = Buzzer()
        self.door = DoorServo()
        self.mqtt = mqtt
        self.rgb = rgb_controller
        self.last_card = None
        self.last_scan = 0

    def update(self):
        """Check for RFID scans - call this in main loop"""
        card_id = self.rfid.scan()
        now = time.time()

        if card_id and (card_id != self.last_card or now - self.last_scan > SCAN_COOLDOWN):
            print(f"[RFID] Scanned: {card_id}")
            self.mqtt.publish(TOPICS.event("rfid_scan"), f'{{"card":"{card_id}","action":"check"}}')

            # Flash green as acknowledgment
            self.rgb.rgb.green()
            time.sleep(1)
            self.rgb.rgb.off()

            self.last_card = card_id
            self.last_scan = now

    def handle_authorized(self, card_id):
        """Called when card is authorized (from MQTT callback)"""
        print(f"[RFID] Authorized: {card_id}")
        self.door.open()
        self.rgb.rgb.green()
        time.sleep(2)
        self.rgb.rgb.off()
        time.sleep(3)
        self.door.close()

    def handle_unauthorized(self, card_id):
        """Called when card is unauthorized (from MQTT callback)"""
        print(f"[RFID] Unauthorized: {card_id}")
        for _ in range(3):
            self.rgb.rgb.red()
            self.buzzer.on()
            time.sleep(0.3)
            self.rgb.rgb.off()
            self.buzzer.off()
            time.sleep(0.3)

    def cleanup(self):
        self.buzzer.off()
        self.door.close()
