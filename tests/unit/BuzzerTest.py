from TestingSuite import PicoTestBase
from components.actuators.buzzer import Buzzer

class BuzzerTest(PicoTestBase):
    """Unit tests for Buzzer component"""

    def test_buzzer_initialization(self):
        """Test Buzzer can be created"""
        buzzer = Buzzer()
        assert buzzer is not None
        assert buzzer.state == False

    def test_buzzer_on(self):
        """Test Buzzer turns on"""
        buzzer = Buzzer()
        buzzer.on()
        assert buzzer.state == True
        buzzer.off()

    def test_buzzer_off(self):
        """Test Buzzer turns off"""
        buzzer = Buzzer()
        buzzer.on()
        buzzer.off()
        assert buzzer.state == False

    def test_buzzer_beep(self):
        """Test Buzzer beeps"""
        buzzer = Buzzer()
        buzzer.beep(duration=0.1)
        assert buzzer.state == False
