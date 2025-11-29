from TestingSuite import PicoTestBase
from components.sensors.dht_sensor import DHT

class DHTTest(PicoTestBase):
    def test_dht_initialization(self):
        dht = DHT()
        assert dht is not None
        assert dht.sensor is not None

    def test_dht_read_method_exists(self):
        dht = DHT()
        assert hasattr(dht, 'read')
        assert callable(dht.read)

    def test_dht_read_returns_dict_or_none(self):
        dht = DHT()
        result = dht.read()
        assert result is None or isinstance(result, dict)

    def test_dht_read_dict_structure(self):
        dht = DHT()
        result = dht.read()
        if result:
            assert 'temp' in result
            assert 'humidity' in result

    def test_dht_temperature_range(self):
        dht = DHT()
        result = dht.read()
        if result:
            assert 0 <= result['temp'] <= 50

    def test_dht_humidity_range(self):
        dht = DHT()
        result = dht.read()
        if result:
            assert 20 <= result['humidity'] <= 90
