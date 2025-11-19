import time
from components import GasSensor, Fan, RGBStrip, WiFi, MQTT
from utils.database import Database
from config import TOPICS

gas = GasSensor()
fan = Fan()
rgb = RGBStrip()
wifi = WiFi()
mqtt = MQTT()
db = Database()

previous_gas = False

def handle_gas_detected():
    """Handle gas detection event"""
    print("Gas detected!")

    fan.on()
    rgb.red()

    if mqtt.is_connected():
        mqtt.publish(TOPICS.event("gas_detected"), "1")

    db.log_gas()

def handle_gas_cleared():
    """Handle when gas clears"""
    print("Gas cleared!")
    fan.off()
    rgb.off()

print("=" * 50)
print("GAS DETECTION & FAN CONTROL - TASK 5")
print("=" * 50)

print("\nConnecting to WiFi...")
if not wifi.is_connected():
    if wifi.connect():
        print(f"WiFi connected! IP: {wifi.get_ip()}")
    else:
        print("WiFi connection failed!")
else:
    print(f"WiFi already connected! IP: {wifi.get_ip()}")

time.sleep(2)

print("Connecting to MQTT...")
if mqtt.connect():
    print("MQTT connected!")
else:
    print("MQTT connection failed! Bridge will handle logging.")

print("\nSetup complete! Monitoring for gas...")
print("=" * 50)

while True:
    try:
        gas_detected = gas.is_detected()

        if gas_detected and not previous_gas:
            handle_gas_detected()

        elif not gas_detected and previous_gas:
            handle_gas_cleared()

        previous_gas = gas_detected

        mqtt.check_messages()

        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\nStopping gas detector...")
        fan.off()
        rgb.off()
        mqtt.disconnect()
        break
    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(1)
