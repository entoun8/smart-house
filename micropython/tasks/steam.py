from components import WaterSensor, WindowServo
from config import TOPICS

class SteamTask:
    def __init__(self, rgb_controller, mqtt=None):
        self.water = WaterSensor()
        self.window = WindowServo()
        self.rgb = rgb_controller
        self.mqtt = mqtt
        self.previous = False

    def update(self):
        steam = self.water.is_wet()

        if steam and not self.previous:
            self.window.close()
            self.rgb.set_rgb("steam", self.rgb.rgb.blue)
            if self.mqtt:
                self.mqtt.publish(TOPICS.device_state("window"), "close")

        elif not steam and self.previous:
            self.rgb.clear_rgb("steam")

        self.previous = steam

    def cleanup(self):
        self.rgb.clear_rgb("steam")
