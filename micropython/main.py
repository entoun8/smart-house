import time
import ntptime
from components import RGBStrip, LCD, WiFi, MQTT

from tasks.led_control import LEDControlTask
from tasks.temperature import TemperatureTask
from tasks.motion import MotionTask
from tasks.steam import SteamTask
from tasks.gas import GasTask
from tasks.asthma import AsthmaTask
from tasks.access_control import AccessControlTask
from tasks.device_control import DeviceControlTask

class RGBController:
    PRIORITY = {"off": 0, "motion": 1, "steam": 2, "gas": 3}

    def __init__(self):
        self.rgb = RGBStrip()
        self.current_state = "off"

    def set_rgb(self, state, color_func):
        if self.PRIORITY.get(state, 0) >= self.PRIORITY.get(self.current_state, 0):
            color_func()
            self.current_state = state

    def clear_rgb(self, state):
        if self.current_state == state:
            self.rgb.off()
            self.current_state = "off"

    def off(self):
        self.rgb.off()
        self.current_state = "off"

class MQTTWrapper:
    def __init__(self):
        self.mqtt = MQTT()
        self.connected = False
        self.command_callback = None

    def set_command_callback(self, callback):
        self.command_callback = callback

    def connect(self):
        try:
            if self.mqtt.connect():
                self.connected = True
                print("[MQTT] Connected")
                self._subscribe_commands()
                return True
        except Exception as e:
            print(f"[MQTT] Failed: {e}")
        self.connected = False
        return False

    def _subscribe_commands(self):
        try:
            def on_message(topic, msg):
                topic = topic.decode() if isinstance(topic, bytes) else topic
                msg = msg.decode() if isinstance(msg, bytes) else msg
                print(f"[MQTT] Cmd: {topic} -> {msg}")
                if self.command_callback:
                    self.command_callback(topic, msg)

            self.mqtt.client.set_callback(on_message)
            self.mqtt.client.subscribe(b"ks5009/house/devices/+/command")
            print("[MQTT] Subscribed to commands")
        except Exception as e:
            print(f"[MQTT] Subscribe error: {e}")

    def publish(self, topic, message):
        if self.connected:
            try:
                self.mqtt.publish(topic, message)
                return True
            except:
                self.connected = False
        return False

    def check_messages(self):
        if self.connected:
            try:
                self.mqtt.check_messages()
            except:
                self.connected = False

    def disconnect(self):
        if self.connected:
            self.mqtt.disconnect()
            self.connected = False

def sync_time():
    """Sync time with NTP server"""
    for i in range(5):
        try:
            print(f"NTP sync {i+1}/5...")
            ntptime.settime()
            print("Time synced!")
            return True
        except:
            time.sleep(2)
    print("NTP sync failed")
    return False


print("=" * 40)
print("SMART HOUSE")
print("=" * 40)

print("\n[WiFi] Connecting...")
wifi = WiFi()
wifi.connect()

print("\n[Time] Syncing...")
sync_time()

print("\n[MQTT] Connecting...")
mqtt = MQTTWrapper()
mqtt.connect()

print("\n[DeviceControl] Initializing...")
device_control = DeviceControlTask(mqtt)

rgb = RGBController()
print("\n[LCD] Initializing...")
time.sleep(1)  
lcd = LCD()
print(f"[LCD] Connected: {lcd.is_connected()}")

print("\n[Tasks] Initializing...")
tasks = {
    "led": LEDControlTask(),
    "temp": TemperatureTask(mqtt, lcd),
    "motion": MotionTask(mqtt, rgb),
    "steam": SteamTask(rgb),
    "gas": GasTask(mqtt, rgb),
    "rfid": AccessControlTask(mqtt, rgb),
    "device_control": device_control,
}
tasks["asthma"] = AsthmaTask(mqtt, lcd, tasks["temp"])

tasks["led"].update()

if lcd.is_connected():
    print("[LCD] Testing direct write...")
    lcd.display_alert("Smart House", "Starting...")
    time.sleep(2)

tasks["temp"].update()

print("\nRunning...")
print("=" * 40)

while True:
    try:
        for task in tasks.values():
            task.update()

        if mqtt.connected:
            mqtt.check_messages()
        else:
            mqtt.connect()

        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping...")
        for task in tasks.values():
            task.cleanup()
        rgb.off()
        lcd.clear()
        mqtt.disconnect()
        break

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)
