from .mqtt import MQTT

class MQTTWrapper:
    def __init__(self):
        self.mqtt = MQTT()
        self.connected = False
        self.command_callback = None

    def set_command_callback(self, callback):
        self.command_callback = callback

    def connect(self):
        if self.mqtt.connect():
            self.connected = True
            self.mqtt.client.set_callback(self._on_message)
            self.mqtt.client.subscribe(b"ks5009/house/devices/+/command")
            return True
        self.connected = False
        return False

    def _on_message(self, topic, msg):
        topic = topic.decode() if isinstance(topic, bytes) else topic
        msg = msg.decode() if isinstance(msg, bytes) else msg
        if self.command_callback:
            self.command_callback(topic, msg)

    def publish(self, topic, message):
        if self.connected:
            self.mqtt.publish(topic, message)
            return True
        return False

    def check_messages(self):
        if self.connected:
            self.mqtt.check_messages()

    def disconnect(self):
        if self.connected:
            self.mqtt.disconnect()
            self.connected = False
