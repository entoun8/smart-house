"""
Task 5: Gas Detection - BUTTON TEST VERSION
Press LEFT button to simulate gas detection
"""

from machine import Pin
import time
import sys
sys.path.append('/lib')
from neopixel import NeoPixel

print("\n" + "="*50)
print("TASK 5: GAS DETECTION (Button Test)")
print("="*50)

# Components
fan_pin1 = Pin(19, Pin.OUT)
fan_pin2 = Pin(18, Pin.OUT)
rgb = NeoPixel(Pin(26), 4)
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)

# RGB colors
def set_rgb(color):
    for i in range(4):
        rgb[i] = color
    rgb.write()

# Fan control
def fan_on():
    fan_pin1.on()
    fan_pin2.off()

def fan_off():
    fan_pin1.off()
    fan_pin2.off()

# Start with fan off, RGB off
fan_off()
set_rgb((0, 0, 0))

print("\nFan is OFF")
print("\nReady! Press LEFT button to simulate gas")
print("="*50)

gas_active = False
last_press = 0

while True:
    # Debounce - only allow button press every 2 seconds
    if time.time() - last_press < 2:
        time.sleep(0.1)
        continue

    # Left button pressed - simulate gas
    if btn_left.value() == 0:
        last_press = time.time()

        if not gas_active:
            print("\n" + "="*50)
            print("Gas detected!")
            print("="*50)
            print("Turning on fan...")
            fan_on()
            print("RGB: RED")
            set_rgb((255, 0, 0))
            gas_active = True
            print("\nPress LEFT button again to clear gas")
        else:
            print("\n" + "="*50)
            print("Gas cleared!")
            print("="*50)
            print("Turning off fan...")
            fan_off()
            print("RGB: OFF")
            set_rgb((0, 0, 0))
            gas_active = False
            print("\nPress LEFT button to simulate gas again")

    time.sleep(0.1)
