import network
import time
import config


class WiFi:
    """WiFi connection"""
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self, timeout=10):
        """Connect to WiFi from config"""
        if self.wlan.isconnected():
            print(f"[WiFi] Already connected! IP: {self.get_ip()}")
            return True

        try:
            self.wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        except OSError as e:
            print(f"[WiFi] Connection error: {e}")
            try:
                self.wlan.disconnect()
                time.sleep(1)
                self.wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
            except:
                return False

        max_wait = timeout
        while max_wait > 0:
            if self.wlan.isconnected():
                print(f"[WiFi] Connected! IP: {self.get_ip()}")
                return True
            max_wait -= 1
            time.sleep(1)
        return False

    def disconnect(self):
        """Disconnect from WiFi"""
        self.wlan.disconnect()

    def is_connected(self):
        return self.wlan.isconnected()

    def get_ip(self):
        """Get IP address"""
        if self.is_connected():
            return self.wlan.ifconfig()[0]
        return None
