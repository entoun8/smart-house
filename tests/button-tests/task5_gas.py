"""
Task 5: Gas Detection - BUTTON TEST VERSION
Press LEFT button to simulate gas detection
Press RIGHT button to stop test
Publishes to MQTT for website updates
"""

import time
from machine import Pin
from components import Fan, RGBStrip, WiFi, MQTT
from config import TOPICS

print("\n" + "="*50)
print("TASK 5: GAS DETECTION (Button Test)")
print("="*50)

# Components
fan = Fan()
rgb = RGBStrip()
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

# Connect WiFi and MQTT
print("\n[WiFi] Connecting...")
wifi = WiFi()
wifi.connect()

print("[MQTT] Connecting...")
mqtt = MQTT()
mqtt_connected = False
try:
    mqtt_connected = mqtt.connect()
    if mqtt_connected:
        print("[MQTT] Connected!")
except Exception as e:
    print(f"[MQTT] Failed: {e}")

# Start with fan off, RGB off
fan.off()
rgb.off()

print("\nFan is OFF")
print("\nLEFT button: simulate gas")
print("RIGHT button: stop test")
print("="*50)

gas_active = False
last_press = 0

while True:
    # Right button - stop test
    if btn_right.value() == 0:
        print("\n" + "="*50)
        print("STOPPING TEST...")
        print("="*50)
        fan.off()
        rgb.off()
        if mqtt_connected:
            mqtt.publish(TOPICS.event("gas_detected"), "0")
            mqtt.disconnect()
        break

    # Debounce - only allow button press every 2 seconds
    if time.time() - last_press < 2:
        time.sleep(0.1)
        continue

    # Left button pressed - simulate gas
    if btn_left.value() == 0:
        last_press = time.time()

        if not gas_active:
            print("\n" + "="*50)
            print("GAS DETECTED!")
            print("="*50)
            print("Turning on fan...")
            fan.on()
            print("RGB: RED")
            rgb.red()

            # Publish to MQTT (website)
            if mqtt_connected:
                mqtt.publish(TOPICS.event("gas_detected"), "1")
                print("[MQTT] Published gas_detected: 1")

            gas_active = True
            print("\nPress LEFT button again to clear gas")
        else:
            print("\n" + "="*50)
            print("GAS CLEARED")
            print("="*50)
            print("Turning off fan...")
            fan.off()
            print("RGB: OFF")
            rgb.off()

            # Publish to MQTT (website)
            if mqtt_connected:
                mqtt.publish(TOPICS.event("gas_detected"), "0")
                print("[MQTT] Published gas_detected: 0")

            gas_active = False
            print("\nPress LEFT button to simulate gas again")

    time.sleep(0.1)

print("Test ended.")
