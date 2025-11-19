from machine import Pin
import neopixel
import config


class RGBStrip:
    """RGB LED strip"""
    def __init__(self):
        self.np = neopixel.NeoPixel(Pin(config.RGB_LED_PIN), config.RGB_LED_COUNT)
        self.num_leds = config.RGB_LED_COUNT
        self.strip = self.np  

    def set_color(self, r, g, b):
        for i in range(self.num_leds):
            self.np[i] = (r, g, b)  
        self.np.write()

    def set_led(self, index, r, g, b):
        """Set individual LED color"""
        self.np[index] = (r, g, b)  
        self.np.write()

    def off(self):
        for i in range(self.num_leds):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def red(self):
        self.set_color(255, 0, 0)

    def green(self):
        self.set_color(0, 255, 0)

    def blue(self):
        self.set_color(0, 0, 255)

    def orange(self):
        self.set_color(255, 165, 0)

    def purple(self):
        self.set_color(128, 0, 128)

    def white(self):
        self.set_color(255, 255, 255)
