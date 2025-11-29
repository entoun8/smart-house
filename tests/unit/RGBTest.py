from TestingSuite import PicoTestBase
from components.actuators.rgb import RGBStrip

class RGBTest(PicoTestBase):
    def test_rgb_initialization(self):
        rgb = RGBStrip()
        assert rgb is not None
        assert rgb.num_leds == 4

    def test_rgb_set_color(self):
        rgb = RGBStrip()
        rgb.set_color(255, 0, 0)
        assert rgb.strip[0] == (0, 255, 0)

    def test_rgb_off(self):
        rgb = RGBStrip()
        rgb.set_color(255, 255, 255)
        rgb.off()
        assert rgb.strip[0] == (0, 0, 0)

    def test_rgb_individual_led(self):
        rgb = RGBStrip()
        rgb.set_led(0, 255, 0, 0)
        assert rgb.strip[0] == (0, 255, 0)
        assert rgb.strip[1] == (0, 0, 0)
