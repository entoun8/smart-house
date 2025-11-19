from TestingSuite import PicoTestBase
from components.sensors.gas import GasSensor

class GasSensorTest(PicoTestBase):
    """Unit tests for Gas Sensor component"""

    def test_gas_sensor_initialization(self):
        """Test GasSensor can be created"""
        gas = GasSensor()
        assert gas is not None
        assert gas.pin is not None

    def test_gas_sensor_read_method_exists(self):
        """Test GasSensor has read method"""
        gas = GasSensor()
        assert hasattr(gas, 'read')
        assert callable(gas.read)

    def test_gas_sensor_read_returns_integer(self):
        """Test GasSensor returns integer"""
        gas = GasSensor()
        value = gas.read()
        assert isinstance(value, int)

    def test_gas_sensor_value_range(self):
        """Test GasSensor value range"""
        gas = GasSensor()
        value = gas.read()
        assert value in [0, 1]

    def test_gas_sensor_is_detected_method_exists(self):
        """Test GasSensor has is_detected"""
        gas = GasSensor()
        assert hasattr(gas, 'is_detected')
        assert callable(gas.is_detected)

    def test_gas_sensor_is_detected_returns_boolean(self):
        """Test GasSensor returns boolean"""
        gas = GasSensor()
        result = gas.is_detected()
        assert isinstance(result, bool)

    def test_gas_sensor_detection_logic(self):
        """Test GasSensor detection logic"""
        gas = GasSensor()
        value = gas.read()
        detected = gas.is_detected()
        if value == 1:
            assert detected == True
        else:
            assert detected == False
