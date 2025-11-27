from components import RGBStrip

class RGBController:
    PRIORITY = {"off": 0, "motion": 1, "steam": 2, "gas": 3}

    def __init__(self):
        self.rgb = RGBStrip()
        self.current_state = "off"

    def set_rgb(self, state, color_func):
        if self.PRIORITY.get(state, 0) >= self.PRIORITY.get(self.current_state, 0):
            color_func()
            self.current_state = state

    def clear_rgb(self, state):
        if self.current_state == state:
            self.rgb.off()
            self.current_state = "off"

    def off(self):
        self.rgb.off()
        self.current_state = "off"
