from TestingSuite import PicoTestBase
from components.sensors.pir import PIR

class PIRTest(PicoTestBase):
    def test_pir_initialization(self):
        pir = PIR()
        assert pir is not None
        assert pir.pin is not None

    def test_pir_motion_detected_method_exists(self):
        pir = PIR()
        assert hasattr(pir, 'motion_detected')
        assert callable(pir.motion_detected)

    def test_pir_motion_detected_returns_boolean(self):
        pir = PIR()
        result = pir.motion_detected()
        assert isinstance(result, bool)

    def test_pir_pin_value_reading(self):
        pir = PIR()
        value = pir.pin.value()
        assert value in [0, 1]
