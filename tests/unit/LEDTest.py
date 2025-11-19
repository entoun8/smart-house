from TestingSuite import PicoTestBase
from components.actuators.led import LED

class LEDTest(PicoTestBase):
    """Unit tests for LED component"""

    def test_led_initialization(self):
        """Test LED can be created"""
        led = LED()
        assert led is not None
        assert led.state == False

    def test_led_on(self):
        """Test LED turns on"""
        led = LED()
        led.on()
        assert led.state == True

    def test_led_off(self):
        """Test LED turns off"""
        led = LED()
        led.on()
        led.off()
        assert led.state == False

    def test_led_toggle(self):
        """Test LED toggles"""
        led = LED()
        led.toggle()
        assert led.state == True
        led.toggle()
        assert led.state == False

    def test_led_blink(self):
        """Test LED blinks"""
        led = LED()
        led.blink(times=2, delay=0.1)
        assert led.state == False
