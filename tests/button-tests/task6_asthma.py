"""
Task 6: Asthma Alert - BUTTON TEST VERSION
Press LEFT button to simulate asthma alert conditions
Press RIGHT button to stop test
Publishes to MQTT for website updates
"""

import time
from machine import Pin
from components import LCD, WiFi, MQTT
from config import TOPICS

print("\n" + "="*50)
print("TASK 6: ASTHMA ALERT (Button Test)")
print("="*50)

# Components
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

# Initialize LCD
print("\n[LCD] Initializing...")
time.sleep(0.5)
lcd = LCD()
print(f"[LCD] Connected: {lcd.is_connected()}")

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

# Display normal state
if lcd.is_connected():
    lcd.display_alert("Temp: 25C", "Humidity: 45%")
    print("[LCD] Showing normal conditions")

print("\nNormal conditions (no alert)")
print("\nLEFT button: simulate asthma alert")
print("RIGHT button: stop test")
print("="*50)

alert_active = False
last_press = 0

while True:
    # Right button - stop test
    if btn_right.value() == 0:
        print("\n" + "="*50)
        print("STOPPING TEST...")
        print("="*50)
        if lcd.is_connected():
            lcd.clear()
        if mqtt_connected:
            mqtt.publish(TOPICS.event("asthma_alert"), "0")
            mqtt.disconnect()
        break

    # Debounce
    if time.time() - last_press < 2:
        time.sleep(0.1)
        continue

    # Left button pressed - simulate asthma alert
    if btn_left.value() == 0:
        last_press = time.time()

        if not alert_active:
            print("\n" + "="*50)
            print("ASTHMA ALERT!")
            print("="*50)
            print("Conditions: Humidity >50% + Temp >27C")

            if lcd.is_connected():
                lcd.display_alert("! ASTHMA ALERT !", "H>50% T>27C")
                print("[LCD] Alert displayed")

            # Publish to MQTT (website)
            if mqtt_connected:
                mqtt.publish(TOPICS.event("asthma_alert"), "1")
                print("[MQTT] Published asthma_alert: 1")

            alert_active = True
            print("\nPress LEFT button to clear alert")
        else:
            print("\n" + "="*50)
            print("ASTHMA ALERT CLEARED")
            print("="*50)

            if lcd.is_connected():
                lcd.display_alert("Temp: 25C", "Humidity: 45%")
                print("[LCD] Normal display")

            # Publish to MQTT (website)
            if mqtt_connected:
                mqtt.publish(TOPICS.event("asthma_alert"), "0")
                print("[MQTT] Published asthma_alert: 0")

            alert_active = False
            print("\nPress LEFT button to simulate asthma alert again")

    time.sleep(0.1)

print("Test ended.")
