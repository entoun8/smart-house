from umqtt.simple import MQTTClient
import time
import ssl
from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_CLIENT_ID

class MQTT:
    def __init__(self):
        """Initialize MQTT (auto-loads settings from config)"""
        try:
            params = {
                'client_id': MQTT_CLIENT_ID,
                'server': MQTT_BROKER,
                'port': MQTT_PORT,
                'keepalive': 60
            }

            if MQTT_USER and MQTT_PASSWORD:
                params['user'] = MQTT_USER
                params['password'] = MQTT_PASSWORD

            if MQTT_PORT == 8883:
                params['ssl'] = True
                params['ssl_params'] = {'server_hostname': MQTT_BROKER}

            self.client = MQTTClient(**params)
        except Exception as e:
            print(f"[MQTT] Init error: {e}")
            self.client = None
        self.connected = False

    def connect(self):
        """Connect to MQTT broker"""
        try:
            if self.client:
                self.client.connect()
                self.connected = True
                print("[MQTT] Connected!")
                return True
            return False
        except Exception as e:
            print(f"[MQTT] Failed: {e}")
            return False

    def is_connected(self):
        """Check if connected"""
        return self.connected

    def disconnect(self):
        """Disconnect from broker"""
        if self.connected:
            self.client.disconnect()
            self.connected = False
            print("[MQTT] Disconnected")

    def publish(self, topic, message):
        """Publish a message"""
        if not self.connected:
            return False
        try:
            self.client.publish(topic, str(message))
            return True
        except:
            return False

    def subscribe(self, topic, callback):
        """Subscribe to a topic"""
        if not self.connected:
            return False
        try:
            self.client.set_callback(callback)
            self.client.subscribe(topic)
            return True
        except:
            return False

    def check_messages(self):
        """Check for new messages (call in loop)"""
        if self.connected:
            try:
                self.client.check_msg()
            except:
                self.connected = False
