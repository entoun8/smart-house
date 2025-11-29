from TestingSuite import PicoTestBase
from components.actuators.fan import Fan

class FanTest(PicoTestBase):
    def test_fan_initialization(self):
        fan = Fan()
        assert fan is not None
        assert fan.state == False

    def test_fan_on(self):
        fan = Fan()
        fan.on()
        assert fan.state == True

    def test_fan_off(self):
        fan = Fan()
        fan.on()
        fan.off()
        assert fan.state == False

    def test_fan_reverse(self):
        fan = Fan()
        fan.reverse()
        assert fan.state == True
        fan.off()
