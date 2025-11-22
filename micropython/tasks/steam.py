"""Task 4: Steam Detection -> Local only (close window)"""

from components import WaterSensor, WindowServo


class SteamTask:
    def __init__(self, rgb_controller):
        self.water = WaterSensor()
        self.window = WindowServo()
        self.rgb = rgb_controller
        self.previous = False

    def update(self):
        """Check steam sensor - call this in main loop"""
        steam = self.water.is_wet()

        if steam and not self.previous:
            print("[Steam] Detected - closing window")
            self.window.close()
            self.rgb.set_rgb("steam", self.rgb.rgb.blue)

        elif not steam and self.previous:
            self.rgb.clear_rgb("steam")

        self.previous = steam

    def cleanup(self):
        self.rgb.clear_rgb("steam")
