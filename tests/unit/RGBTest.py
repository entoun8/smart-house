from TestingSuite import PicoTestBase
from components.actuators.rgb import RGBStrip

class RGBTest(PicoTestBase):
    """Unit tests for RGB LED Strip component"""

    def test_rgb_initialization(self):
        """Test RGBStrip can be created"""
        rgb = RGBStrip()
        assert rgb is not None
        assert rgb.num_leds == 4

    def test_rgb_set_color(self):
        """Test RGB sets color"""
        rgb = RGBStrip()
        rgb.set_color(255, 0, 0)
        assert rgb.strip[0] == (0, 255, 0)

    def test_rgb_off(self):
        """Test RGB turns off"""
        rgb = RGBStrip()
        rgb.set_color(255, 255, 255)
        rgb.off()
        assert rgb.strip[0] == (0, 0, 0)

    def test_rgb_individual_led(self):
        """Test RGB individual LED"""
        rgb = RGBStrip()
        rgb.set_led(0, 255, 0, 0)
        assert rgb.strip[0] == (0, 255, 0)
        assert rgb.strip[1] == (0, 0, 0)
