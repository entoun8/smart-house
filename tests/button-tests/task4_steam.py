"""
Task 4: Steam Detection - BUTTON TEST VERSION
Press LEFT button to simulate steam detection
"""

from machine import Pin, PWM
import time
import sys
sys.path.append('/lib')
from neopixel import NeoPixel

print("\n" + "="*50)
print("TASK 4: STEAM DETECTION (Button Test)")
print("="*50)

# Components
window_servo = PWM(Pin(5), freq=50)
rgb = NeoPixel(Pin(26), 4)
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)

# Window positions
WINDOW_OPEN = 128
WINDOW_CLOSED = 77

# RGB colors
def set_rgb(color):
    for i in range(4):
        rgb[i] = color
    rgb.write()

# Start with window open, RGB off
window_servo.duty(WINDOW_OPEN)
set_rgb((0, 0, 0))

print("\nWindow is OPEN")
print("\nReady! Press LEFT button to simulate steam")
print("="*50)

steam_active = False
last_press = 0

while True:
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
            window_servo.duty(WINDOW_CLOSED)
            print("RGB: BLUE")
            set_rgb((0, 0, 255))
            steam_active = True
            print("\nPress LEFT button again to clear steam")
        else:
            print("\n" + "="*50)
            print("STEAM CLEARED")
            print("="*50)
            print("Opening window...")
            window_servo.duty(WINDOW_OPEN)
            print("RGB: OFF")
            set_rgb((0, 0, 0))
            steam_active = False
            print("\nPress LEFT button to simulate steam again")

    time.sleep(0.1)
