"""
Task: Device Control (Web App Commands)
Handles door, window, fan commands from web app via MQTT
"""

from components import DoorServo, WindowServo, Fan


class DeviceControlTask:
    """Handles web app commands for door, window, fan"""

    def __init__(self, mqtt_wrapper):
        self.door = DoorServo()
        self.window = WindowServo()
        self.fan = Fan()
        self.mqtt = mqtt_wrapper

        # Register callback
        self.mqtt.set_command_callback(self.handle_command)
        print("[DeviceControl] Initialized")

    def handle_command(self, topic, message):
        """Process incoming MQTT commands"""
        msg = message.lower()

        if "door" in topic:
            if msg == "open":
                self.door.open()
                print("[Door] Opened")
            elif msg == "close":
                self.door.close()
                print("[Door] Closed")

        elif "window" in topic:
            if msg == "open":
                self.window.open()
                print("[Window] Opened")
            elif msg == "close":
                self.window.close()
                print("[Window] Closed")

        elif "fan" in topic:
            if msg == "on":
                self.fan.on()
                print("[Fan] ON")
            elif msg == "off":
                self.fan.off()
                print("[Fan] OFF")

    def update(self):
        """No periodic update needed - command-driven"""
        pass

    def cleanup(self):
        """Cleanup on shutdown"""
        self.fan.off()
        self.door.close()
        self.window.close()
