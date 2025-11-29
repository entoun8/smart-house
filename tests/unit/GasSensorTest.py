from TestingSuite import PicoTestBase
from components.sensors.gas import GasSensor

class GasSensorTest(PicoTestBase):
    def test_gas_sensor_initialization(self):
        gas = GasSensor()
        assert gas is not None
        assert gas.pin is not None

    def test_gas_sensor_read_method_exists(self):
        gas = GasSensor()
        assert hasattr(gas, 'read')
        assert callable(gas.read)

    def test_gas_sensor_read_returns_integer(self):
        gas = GasSensor()
        value = gas.read()
        assert isinstance(value, int)

    def test_gas_sensor_value_range(self):
        gas = GasSensor()
        value = gas.read()
        assert value in [0, 1]

    def test_gas_sensor_is_detected_method_exists(self):
        gas = GasSensor()
        assert hasattr(gas, 'is_detected')
        assert callable(gas.is_detected)

    def test_gas_sensor_is_detected_returns_boolean(self):
        gas = GasSensor()
        result = gas.is_detected()
        assert isinstance(result, bool)

    def test_gas_sensor_detection_logic(self):
        gas = GasSensor()
        value = gas.read()
        detected = gas.is_detected()
        if value == 1:
            assert detected == True
        else:
            assert detected == False
