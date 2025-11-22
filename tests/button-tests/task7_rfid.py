"""
Task 7: RFID Access Control - BUTTON TEST VERSION
Press LEFT button to simulate authorized access
Press RIGHT button to simulate unauthorized access
Press BOTH buttons to stop test
Publishes to MQTT for website updates
"""

import time
from machine import Pin
from components import DoorServo, Buzzer, RGBStrip, WiFi, MQTT
from config import TOPICS

print("\n" + "="*50)
print("TASK 7: RFID ACCESS (Button Test)")
print("="*50)

# Components
door = DoorServo()
buzzer = Buzzer()
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

# Start with door closed, RGB off
door.close()
buzzer.off()
rgb.off()

# Simulated card IDs
AUTHORIZED_CARD = "0x12345678"
UNAUTHORIZED_CARD = "0xAABBCCDD"

print("\nDoor is CLOSED")
print("\nLEFT button: Authorized (Green + Open door)")
print("RIGHT button: Unauthorized (Red + Buzzer)")
print("BOTH buttons: Stop test")
print("="*50)

last_left = 1
last_right = 1

while True:
    current_left = btn_left.value()
    current_right = btn_right.value()

    # Both buttons - stop test
    if current_left == 0 and current_right == 0:
        print("\n" + "="*50)
        print("STOPPING TEST...")
        print("="*50)
        door.close()
        buzzer.off()
        rgb.off()
        if mqtt_connected:
            mqtt.disconnect()
        break

    # LEFT button - authorized access
    if current_left == 0 and last_left == 1:
        time.sleep(0.05)  # Debounce

        print("\n" + "="*50)
        print(f"RFID card scanned: {AUTHORIZED_CARD}")
        print("="*50)

        # Publish to MQTT (website)
        if mqtt_connected:
            mqtt.publish(TOPICS.event("rfid_scan"), f'{{"card":"{AUTHORIZED_CARD}","status":"authorized"}}')
            print("[MQTT] Published rfid_scan: authorized")

        print("ACCESS GRANTED!")
        print("Opening door...")

        # Open door
        door.open()
        rgb.green()
        time.sleep(3)

        # Close door
        print("Closing door...")
        door.close()
        rgb.off()

        print(f"Access complete: {AUTHORIZED_CARD}")
        print("="*50)

    # RIGHT button - unauthorized access
    if current_right == 0 and last_right == 1:
        time.sleep(0.05)  # Debounce

        print("\n" + "="*50)
        print(f"RFID card scanned: {UNAUTHORIZED_CARD}")
        print("="*50)

        # Publish to MQTT (website)
        if mqtt_connected:
            mqtt.publish(TOPICS.event("rfid_scan"), f'{{"card":"{UNAUTHORIZED_CARD}","status":"unauthorized"}}')
            print("[MQTT] Published rfid_scan: unauthorized")

        print("ACCESS DENIED!")

        # Flash red and buzzer
        for _ in range(3):
            rgb.red()
            buzzer.on()
            time.sleep(0.3)
            rgb.off()
            buzzer.off()
            time.sleep(0.3)

        print(f"Unauthorized: {UNAUTHORIZED_CARD}")
        print("="*50)

    last_left = current_left
    last_right = current_right
    time.sleep(0.1)

print("Test ended.")
