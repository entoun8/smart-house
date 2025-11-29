from TestingSuite import PicoTestBase
from components.sensors.water import WaterSensor

class WaterSensorTest(PicoTestBase):
    def test_water_sensor_initialization(self):
        water = WaterSensor()
        assert water is not None
        assert water.adc is not None

    def test_water_sensor_read_method_exists(self):
        water = WaterSensor()
        assert hasattr(water, 'read')
        assert callable(water.read)

    def test_water_sensor_read_returns_integer(self):
        water = WaterSensor()
        value = water.read()
        assert isinstance(value, int)

    def test_water_sensor_value_range(self):
        water = WaterSensor()
        value = water.read()
        assert 0 <= value <= 4095

    def test_water_sensor_is_wet_method_exists(self):
        water = WaterSensor()
        assert hasattr(water, 'is_wet')
        assert callable(water.is_wet)

    def test_water_sensor_is_wet_returns_boolean(self):
        water = WaterSensor()
        result = water.is_wet(threshold=2000)
        assert isinstance(result, bool)

    def test_water_sensor_threshold_detection(self):
        water = WaterSensor()
        value = water.read()
        if value > 0:
            assert water.is_wet(threshold=0) == True
        assert water.is_wet(threshold=4096) == False
