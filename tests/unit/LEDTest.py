from TestingSuite import PicoTestBase
from components.actuators.led import LED

class LEDTest(PicoTestBase):
    def test_led_initialization(self):
        led = LED()
        assert led is not None
        assert led.state == False

    def test_led_on(self):
        led = LED()
        led.on()
        assert led.state == True

    def test_led_off(self):
        led = LED()
        led.on()
        led.off()
        assert led.state == False

    def test_led_toggle(self):
        led = LED()
        led.toggle()
        assert led.state == True
        led.toggle()
        assert led.state == False

    def test_led_blink(self):
        led = LED()
        led.blink(times=2, delay=0.1)
        assert led.state == False
