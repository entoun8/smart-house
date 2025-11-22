"""Task 5: Gas Detection -> MQTT + Fan"""

import time
from components import GasSensor, Fan
from config import TOPICS

WARMUP_TIME = 30  # Seconds for sensor to stabilize
DEBOUNCE_COUNT = 6  # Consecutive readings needed to confirm


class GasTask:
    def __init__(self, mqtt, rgb_controller):
        self.gas = GasSensor()
        self.fan = Fan()
        self.mqtt = mqtt
        self.rgb = rgb_controller
        self.previous = False
        self.warmup_done = False
        self.start_time = time.time()
        self.detection_count = 0

    def update(self):
        """Check gas sensor with debouncing - call this in main loop"""
        # Skip during warmup
        if not self.warmup_done:
            if time.time() - self.start_time > WARMUP_TIME:
                self.warmup_done = True
                print("[Gas] Warmup complete")
            return

        # Read sensor
        reading = self.gas.is_detected()

        # Debouncing
        if reading:
            self.detection_count += 1
        else:
            self.detection_count = 0

        # Confirm only after enough consecutive readings
        confirmed = self.detection_count >= DEBOUNCE_COUNT

        if confirmed and not self.previous:
            print("[Gas] DETECTED!")
            self.fan.on()
            self.rgb.set_rgb("gas", self.rgb.rgb.red)
            self.mqtt.publish(TOPICS.event("gas_detected"), "1")

        elif not confirmed and self.previous:
            print("[Gas] Cleared")
            self.fan.off()
            self.rgb.clear_rgb("gas")
            self.mqtt.publish(TOPICS.event("gas_detected"), "0")

        self.previous = confirmed

    def cleanup(self):
        self.fan.off()
        self.rgb.clear_rgb("gas")
