import time
from components import GasSensor, Fan
from config import TOPICS

WARMUP_TIME = 30  
DEBOUNCE_COUNT = 6  

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
        if not self.warmup_done:
            if time.time() - self.start_time > WARMUP_TIME:
                self.warmup_done = True
            return

        reading = self.gas.is_detected()

        if reading:
            self.detection_count += 1
        else:
            self.detection_count = 0

        confirmed = self.detection_count >= DEBOUNCE_COUNT

        if confirmed and not self.previous:
            self.fan.on()
            self.rgb.set_rgb("gas", self.rgb.rgb.red)
            self.mqtt.publish(TOPICS.event("gas_detected"), "1")
            self.mqtt.publish(TOPICS.device_state("fan"), "on")

        elif not confirmed and self.previous:
            self.fan.off()
            self.rgb.clear_rgb("gas")
            self.mqtt.publish(TOPICS.event("gas_detected"), "0")
            self.mqtt.publish(TOPICS.device_state("fan"), "off")

        self.previous = confirmed

    def cleanup(self):
        self.fan.off()
        self.rgb.clear_rgb("gas")
