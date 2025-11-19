from TestingSuite import PicoTestBase
from components.connectivity.wifi import WiFi

class WiFiTest(PicoTestBase):
    """Unit tests for WiFi component"""

    def test_wifi_initialization(self):
        """Test WiFi can be created"""
        wifi = WiFi()
        assert wifi is not None
        assert wifi.wlan is not None

    def test_wifi_connect_method_exists(self):
        """Test WiFi has connect"""
        wifi = WiFi()
        assert hasattr(wifi, 'connect')
        assert callable(wifi.connect)

    def test_wifi_disconnect_method_exists(self):
        """Test WiFi has disconnect"""
        wifi = WiFi()
        assert hasattr(wifi, 'disconnect')
        assert callable(wifi.disconnect)

    def test_wifi_is_connected_method_exists(self):
        """Test WiFi has is_connected"""
        wifi = WiFi()
        assert hasattr(wifi, 'is_connected')
        assert callable(wifi.is_connected)

    def test_wifi_is_connected_returns_boolean(self):
        """Test WiFi returns boolean"""
        wifi = WiFi()
        result = wifi.is_connected()
        assert isinstance(result, bool)

    def test_wifi_get_ip_method_exists(self):
        """Test WiFi has get_ip"""
        wifi = WiFi()
        assert hasattr(wifi, 'get_ip')
        assert callable(wifi.get_ip)

    def test_wifi_connection(self):
        """Test WiFi connects"""
        wifi = WiFi()
        result = wifi.connect(timeout=10)
        assert isinstance(result, bool)
        if result:
            assert wifi.is_connected() == True
            ip = wifi.get_ip()
            assert ip is not None
            assert isinstance(ip, str)
