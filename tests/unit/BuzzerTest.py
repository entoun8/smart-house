from TestingSuite import PicoTestBase
from components.actuators.buzzer import Buzzer

class BuzzerTest(PicoTestBase):
    def test_buzzer_initialization(self):
        buzzer = Buzzer()
        assert buzzer is not None
        assert buzzer.state == False

    def test_buzzer_on(self):
        buzzer = Buzzer()
        buzzer.on()
        assert buzzer.state == True
        buzzer.off()

    def test_buzzer_off(self):
        buzzer = Buzzer()
        buzzer.on()
        buzzer.off()
        assert buzzer.state == False

    def test_buzzer_beep(self):
        buzzer = Buzzer()
        buzzer.beep(duration=0.1)
        assert buzzer.state == False
