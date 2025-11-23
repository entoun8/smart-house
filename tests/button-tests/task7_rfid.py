"""
Task 7: RFID Access Control
Scans actual RFID cards for access control
Press BOTH buttons to stop test
Publishes to MQTT for website updates
"""

import time
import sys
sys.path.append('/lib')
from machine import Pin, PWM
from components import Buzzer, RGBStrip, WiFi, MQTT
from mfrc522_i2c import MFRC522_I2C
from config import TOPICS
import config

print("\n" + "="*50)
print("TASK 7: RFID ACCESS CONTROL")
print("="*50)

# Components
buzzer = Buzzer()
rgb = RGBStrip()
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

# Door servo - direct control for reliability
door_pwm = PWM(Pin(config.DOOR_SERVO_PIN), freq=50)

def door_open():
    print("Opening door...")
    door_pwm.duty(128)  # 180 degrees

def door_close():
    print("Closing door...")
    door_pwm.duty(26)   # 0 degrees

# Initialize RFID reader
print("\n[RFID] Initializing...")
rfid = MFRC522_I2C(scl=22, sda=21, addr=0x28)
print("[RFID] Ready!")

# Connect WiFi and MQTT
print("[WiFi] Connecting...")
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
door_close()
buzzer.off()
rgb.off()

# CARD CONFIGURATION
# White card = AUTHORIZED (opens door)
# Blue keychain = DENIED (buzzer + red flash)
AUTHORIZED_CARD = "0x7cdab502"  # White card - AUTHORIZED
DENIED_CARD = "0x5a6e25b6"      # Blue keychain - DENIED

print("\nDoor is CLOSED")
print(f"\nAuthorized: {AUTHORIZED_CARD} (white card)")
print(f"Denied: {DENIED_CARD} (blue keychain)")
print("\nHold RFID card near reader to scan")
print("Press BOTH buttons to stop test")
print("="*50)

last_card = None
last_scan_time = 0

while True:
    # Check for exit (both buttons)
    if btn_left.value() == 0 and btn_right.value() == 0:
        print("\n" + "="*50)
        print("STOPPING TEST...")
        print("="*50)
        door_close()
        buzzer.off()
        rgb.off()
        door_pwm.deinit()
        if mqtt_connected:
            mqtt.disconnect()
        break

    # Scan for RFID card
    card_id = rfid.scan()

    if card_id:
        # Debounce - don't read same card repeatedly
        current_time = time.time()
        if card_id != last_card or (current_time - last_scan_time) > 3:
            last_card = card_id
            last_scan_time = current_time

            print("\n" + "="*50)
            print(f"Card scanned: {card_id}")
            print("="*50)

            if card_id == AUTHORIZED_CARD:
                # AUTHORIZED - Open door
                print("ACCESS GRANTED!")

                # Publish to MQTT
                if mqtt_connected:
                    try:
                        mqtt.publish(TOPICS.event("rfid_scan"),
                            f'{{"card":"{card_id}","status":"authorized"}}')
                        print("[MQTT] Published: authorized")
                    except Exception as e:
                        print(f"[MQTT] Error: {e}")

                # Open door with green LED
                rgb.green()
                door_open()

                time.sleep(3)

                # Close door
                door_close()
                rgb.off()

            else:
                # UNAUTHORIZED - Deny access
                print("ACCESS DENIED!")

                # Publish to MQTT
                if mqtt_connected:
                    try:
                        mqtt.publish(TOPICS.event("rfid_scan"),
                            f'{{"card":"{card_id}","status":"unauthorized"}}')
                        print("[MQTT] Published: unauthorized")
                    except Exception as e:
                        print(f"[MQTT] Error: {e}")

                # Flash red and buzzer
                for _ in range(3):
                    rgb.red()
                    buzzer.on()
                    time.sleep(0.2)
                    rgb.off()
                    buzzer.off()
                    time.sleep(0.2)

            print("="*50)

    time.sleep(0.1)

print("Test ended.")
