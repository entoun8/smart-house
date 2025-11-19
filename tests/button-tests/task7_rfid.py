"""
Task 7: RFID Access Control - BUTTON TEST VERSION
Press LEFT button to simulate authorized access
Press RIGHT button to simulate unauthorized access
"""

from machine import Pin, PWM
import time
import sys
sys.path.append('/lib')
from neopixel import NeoPixel

print("\n" + "="*50)
print("TASK 7: RFID ACCESS (Button Test)")
print("="*50)

# Components
door_servo = PWM(Pin(13), freq=50)
buzzer = Pin(25, Pin.OUT)
rgb = NeoPixel(Pin(26), 4)
btn_left = Pin(16, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

# Door positions
DOOR_OPEN = 128
DOOR_CLOSED = 77

# RGB colors
def set_rgb(color):
    for i in range(4):
        rgb[i] = color
    rgb.write()

# Start with door closed, RGB off
door_servo.duty(DOOR_CLOSED)
buzzer.off()
set_rgb((0, 0, 0))

print("\nDoor is CLOSED")
print("\nReady! Press buttons to test:")
print("  LEFT BUTTON  = Authorized (Green + Open door)")
print("  RIGHT BUTTON = Unauthorized (Red + Buzzer)")
print("="*50)

# Simulated card IDs
AUTHORIZED_CARD = "0x12345678"
UNAUTHORIZED_CARD = "0xAABBCCDD"

last_left = 1
last_right = 1

while True:
    current_left = btn_left.value()
    current_right = btn_right.value()

    # LEFT button - authorized access
    if current_left == 0 and last_left == 1:
        time.sleep(0.05)  # Debounce

        print("\n" + "="*50)
        print("RFID card scanned: " + AUTHORIZED_CARD)
        print("RFID check request: " + AUTHORIZED_CARD)
        print("="*50)

        # Wait for bridge response (simulated with delay)
        time.sleep(0.5)

        print("RFID authorized: " + AUTHORIZED_CARD)
        print("Opening door...")

        # Open door
        door_servo.duty(DOOR_OPEN)
        set_rgb((0, 255, 0))  # Green
        time.sleep(3)

        # Close door
        print("Closing door...")
        door_servo.duty(DOOR_CLOSED)
        set_rgb((0, 0, 0))

        print("RFID authorized complete: " + AUTHORIZED_CARD)
        print("="*50)

    # RIGHT button - unauthorized access
    if current_right == 0 and last_right == 1:
        time.sleep(0.05)  # Debounce

        print("\n" + "="*50)
        print("RFID card scanned: " + UNAUTHORIZED_CARD)
        print("RFID check request: " + UNAUTHORIZED_CARD)
        print("="*50)

        # Wait for bridge response (simulated with delay)
        time.sleep(0.5)

        print("RFID unauthorized: " + UNAUTHORIZED_CARD)
        print("Access denied!")

        # Flash red and buzzer
        for _ in range(3):
            set_rgb((255, 0, 0))
            buzzer.on()
            time.sleep(0.3)
            set_rgb((0, 0, 0))
            buzzer.off()
            time.sleep(0.3)

        print("RFID unauthorized complete: " + UNAUTHORIZED_CARD)
        print("="*50)

    last_left = current_left
    last_right = current_right
    time.sleep(0.1)
