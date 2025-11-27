import time
import ntptime
from components import LCD, WiFi
from components.connectivity.mqtt_wrapper import MQTTWrapper

from tasks.led_control import LEDControlTask
from tasks.temperature import TemperatureTask
from tasks.motion import MotionTask
from tasks.steam import SteamTask
from tasks.gas import GasTask
from tasks.asthma import AsthmaTask
from tasks.access_control import AccessControlTask
from tasks.device_control import DeviceControlTask
from tasks.rgb_controller import RGBController

def sync_time():
    for _ in range(5):
        try:
            ntptime.settime()
            return True
        except:
            time.sleep(2)
    return False

wifi = WiFi()
wifi.connect()

sync_time()

mqtt = MQTTWrapper()
mqtt.connect()

device_control = DeviceControlTask(mqtt)

rgb = RGBController()

lcd = LCD()

tasks = {
    "led": LEDControlTask(),
    "temp": TemperatureTask(mqtt, lcd),
    "motion": MotionTask(mqtt, rgb),
    "steam": SteamTask(rgb, mqtt),
    "gas": GasTask(mqtt, rgb),
    "rfid": AccessControlTask(mqtt, rgb),
    "device_control": device_control,
}
tasks["asthma"] = AsthmaTask(mqtt, lcd, tasks["temp"])

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
        for task in tasks.values():
            task.cleanup()
        rgb.off()
        lcd.clear()
        mqtt.disconnect()
        break

    except Exception:
        time.sleep(1)
