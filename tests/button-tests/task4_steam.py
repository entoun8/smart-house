"""
Task 4: Steam Detection - BUTTON TEST VERSION
Press LEFT button to simulate steam detection
Press RIGHT button to stop
"""

import time
from machine import Pin
from components import WindowServo, RGBStrip

print("\n" + "="*50)
print("TASK 4: STEAM DETECTION (Button Test)")
print("="*50)

# Components
window = WindowServo()
rgb = RGBStrip()
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

# Start with window open, RGB off
window.open()
rgb.off()

print("\nWindow is OPEN")
print("\nLEFT button: simulate steam")
print("RIGHT button: stop test")
print("="*50)

steam_active = False
last_press = 0

while True:
    # Right button - stop test
    if btn_right.value() == 0:
        print("\n" + "="*50)
        print("STOPPING TEST...")
        print("="*50)
        rgb.off()
        window.open()
        break

    # Debounce - only allow button press every 2 seconds
    if time.time() - last_press < 2:
        time.sleep(0.1)
        continue

    # Left button pressed - simulate steam
    if btn_left.value() == 0:
        last_press = time.time()

        if not steam_active:
            print("\n" + "="*50)
            print("STEAM DETECTED!")
            print("="*50)
            print("Closing window...")
            window.close()
            print("RGB: BLUE")
            rgb.blue()
            steam_active = True
            print("\nPress LEFT button again to clear steam")
        else:
            print("\n" + "="*50)
            print("STEAM CLEARED")
            print("="*50)
            print("Opening window...")
            window.open()
            print("RGB: OFF")
            rgb.off()
            steam_active = False
            print("\nPress LEFT button to simulate steam again")

    time.sleep(0.1)

print("Test ended.")
