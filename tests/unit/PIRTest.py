from TestingSuite import PicoTestBase
from components.sensors.pir import PIR

class PIRTest(PicoTestBase):
    """Unit tests for PIR Motion Sensor component"""

    def test_pir_initialization(self):
        """Test PIR can be created"""
        pir = PIR()
        assert pir is not None
        assert pir.pin is not None

    def test_pir_motion_detected_method_exists(self):
        """Test PIR has motion_detected"""
        pir = PIR()
        assert hasattr(pir, 'motion_detected')
        assert callable(pir.motion_detected)

    def test_pir_motion_detected_returns_boolean(self):
        """Test PIR returns boolean"""
        pir = PIR()
        result = pir.motion_detected()
        assert isinstance(result, bool)

    def test_pir_pin_value_reading(self):
        """Test PIR reads pin value"""
        pir = PIR()
        value = pir.pin.value()
        assert value in [0, 1]
