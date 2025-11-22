"""
Smart House - Main Program
ESP32 -> MQTT -> Web App

Tasks:
1. LED auto-control (8pm-7am)
2. Temperature -> MQTT
3. Motion -> MQTT
4. Steam -> local only
5. Gas -> MQTT
6. Asthma -> MQTT
7. RFID -> MQTT
"""

import time
import ntptime
from components import RGBStrip, LCD, WiFi, MQTT

# Import tasks
from tasks.led_control import LEDControlTask
from tasks.temperature import TemperatureTask
from tasks.motion import MotionTask
from tasks.steam import SteamTask
from tasks.gas import GasTask
from tasks.asthma import AsthmaTask
from tasks.access_control import AccessControlTask


# ============================================
# RGB PRIORITY CONTROLLER
# ============================================

class RGBController:
    """Manages RGB LED with priority system (gas > steam > motion)"""
    PRIORITY = {"off": 0, "motion": 1, "steam": 2, "gas": 3}

    def __init__(self):
        self.rgb = RGBStrip()
        self.current_state = "off"

    def set_rgb(self, state, color_func):
        """Set RGB if new state has higher/equal priority"""
        if self.PRIORITY.get(state, 0) >= self.PRIORITY.get(self.current_state, 0):
            color_func()
            self.current_state = state

    def clear_rgb(self, state):
        """Clear RGB only if requesting state owns it"""
        if self.current_state == state:
            self.rgb.off()
            self.current_state = "off"

    def off(self):
        """Force RGB off"""
        self.rgb.off()
        self.current_state = "off"


# ============================================
# MQTT WRAPPER (safe publish)
# ============================================

class MQTTWrapper:
    """Wrapper for safe MQTT operations"""

    def __init__(self):
        self.mqtt = MQTT()
        self.connected = False

    def connect(self):
        try:
            if self.mqtt.connect():
                self.connected = True
                print("[MQTT] Connected")
                return True
        except Exception as e:
            print(f"[MQTT] Failed: {e}")
        self.connected = False
        return False

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


# ============================================
# SETUP
# ============================================

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

# Connect WiFi
print("\n[WiFi] Connecting...")
wifi = WiFi()
wifi.connect()

# Sync time
print("\n[Time] Syncing...")
sync_time()

# Connect MQTT
print("\n[MQTT] Connecting...")
mqtt = MQTTWrapper()
mqtt.connect()

# Initialize shared components
rgb = RGBController()
print("\n[LCD] Initializing...")
time.sleep(1)  # Longer delay before LCD init
lcd = LCD()
print(f"[LCD] Connected: {lcd.is_connected()}")

# Initialize tasks
print("\n[Tasks] Initializing...")
tasks = {
    "led": LEDControlTask(),
    "temp": TemperatureTask(mqtt, lcd),
    "motion": MotionTask(mqtt, rgb),
    "steam": SteamTask(rgb),
    "gas": GasTask(mqtt, rgb),
    "rfid": AccessControlTask(mqtt, rgb),
}
tasks["asthma"] = AsthmaTask(mqtt, lcd, tasks["temp"])

print("\nTasks:")
print("  1. LED (8pm-7am)")
print("  2. Temperature (30min)")
print("  3. Motion -> MQTT")
print("  4. Steam -> local")
print("  5. Gas -> MQTT")
print("  6. Asthma -> MQTT")
print("  7. RFID -> MQTT")
print("=" * 40)

# Initial updates
tasks["led"].update()

# Direct LCD test
if lcd.is_connected():
    print("[LCD] Testing direct write...")
    lcd.display_alert("Smart House", "Starting...")
    time.sleep(2)

tasks["temp"].update()

print("\nRunning...")
print("=" * 40)


# ============================================
# MAIN LOOP
# ============================================

while True:
    try:
        # Update all tasks
        for task in tasks.values():
            task.update()

        # Check MQTT / reconnect
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
