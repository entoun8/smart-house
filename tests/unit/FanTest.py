from TestingSuite import PicoTestBase
from components.actuators.fan import Fan

class FanTest(PicoTestBase):
    """Unit tests for Fan component"""

    def test_fan_initialization(self):
        """Test Fan can be created"""
        fan = Fan()
        assert fan is not None
        assert fan.state == False

    def test_fan_on(self):
        """Test Fan turns on"""
        fan = Fan()
        fan.on()
        assert fan.state == True

    def test_fan_off(self):
        """Test Fan turns off"""
        fan = Fan()
        fan.on()
        fan.off()
        assert fan.state == False

    def test_fan_reverse(self):
        """Test Fan reverses"""
        fan = Fan()
        fan.reverse()
        assert fan.state == True
        fan.off()
