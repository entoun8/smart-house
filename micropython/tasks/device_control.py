from components import DoorServo, WindowServo, Fan
from config import TOPICS

class DeviceControlTask:
    def __init__(self, mqtt_wrapper):
        self.door = DoorServo()
        self.window = WindowServo()
        self.fan = Fan()
        self.mqtt = mqtt_wrapper

        self.mqtt.set_command_callback(self.handle_command)

    def handle_command(self, topic, message):
        msg = message.lower()

        if "door" in topic:
            if msg == "open":
                self.door.open()
                self.mqtt.publish(TOPICS.device_state("door"), "open")
            elif msg == "close":
                self.door.close()
                self.mqtt.publish(TOPICS.device_state("door"), "close")

        elif "window" in topic:
            if msg == "open":
                self.window.open()
                self.mqtt.publish(TOPICS.device_state("window"), "open")
            elif msg == "close":
                self.window.close()
                self.mqtt.publish(TOPICS.device_state("window"), "close")

        elif "fan" in topic:
            if msg == "on":
                self.fan.on()
                self.mqtt.publish(TOPICS.device_state("fan"), "on")
            elif msg == "off":
                self.fan.off()
                self.mqtt.publish(TOPICS.device_state("fan"), "off")

    def update(self):
        pass

    def cleanup(self):
        self.fan.off()
        self.door.close()
        self.window.close()
