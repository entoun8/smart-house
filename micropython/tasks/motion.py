"""Task 3: Motion Detection -> MQTT"""

from components import PIR
from config import TOPICS


class MotionTask:
    def __init__(self, mqtt, rgb_controller):
        self.pir = PIR()
        self.mqtt = mqtt
        self.rgb = rgb_controller
        self.previous = False

    def update(self):
        """Check motion sensor - call this in main loop"""
        motion = self.pir.motion_detected()

        if motion and not self.previous:
            print("[Motion] Detected")
            self.rgb.set_rgb("motion", self.rgb.rgb.orange)
            self.mqtt.publish(TOPICS.event("motion_detected"), "1")

        elif not motion and self.previous:
            self.rgb.clear_rgb("motion")

        self.previous = motion

    def cleanup(self):
        self.rgb.clear_rgb("motion")
