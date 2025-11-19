from TestingSuite import PicoTestBase
from components.connectivity.mqtt import MQTT

class MQTTTest(PicoTestBase):
    """Unit tests for MQTT component"""

    def test_mqtt_initialization(self):
        """Test MQTT can be created"""
        mqtt = MQTT()
        assert mqtt is not None
        assert mqtt.client is not None

    def test_mqtt_connect_method_exists(self):
        """Test MQTT has connect"""
        mqtt = MQTT()
        assert hasattr(mqtt, 'connect')
        assert callable(mqtt.connect)

    def test_mqtt_disconnect_method_exists(self):
        """Test MQTT has disconnect"""
        mqtt = MQTT()
        assert hasattr(mqtt, 'disconnect')
        assert callable(mqtt.disconnect)

    def test_mqtt_publish_method_exists(self):
        """Test MQTT has publish"""
        mqtt = MQTT()
        assert hasattr(mqtt, 'publish')
        assert callable(mqtt.publish)

    def test_mqtt_subscribe_method_exists(self):
        """Test MQTT has subscribe"""
        mqtt = MQTT()
        assert hasattr(mqtt, 'subscribe')
        assert callable(mqtt.subscribe)

    def test_mqtt_is_connected_method_exists(self):
        """Test MQTT has is_connected"""
        mqtt = MQTT()
        assert hasattr(mqtt, 'is_connected')
        assert callable(mqtt.is_connected)

    def test_mqtt_is_connected_returns_boolean(self):
        """Test MQTT returns boolean"""
        mqtt = MQTT()
        result = mqtt.is_connected()
        assert isinstance(result, bool)
