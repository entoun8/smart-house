# Test: RGB LED Strip (NeoPixel)
# Tests the 4-LED color strip

from machine import Pin
import neopixel
import time
from config import RGB_LED_PIN, RGB_LED_COUNT

print("=" * 40)
print("TEST: RGB LED STRIP (NEOPIXEL)")
print("=" * 40)
print(f"Pin: GPIO {RGB_LED_PIN}")
print(f"Number of LEDs: {RGB_LED_COUNT}")
print("Testing colors...\n")

# Create NeoPixel object
np = neopixel.NeoPixel(Pin(RGB_LED_PIN), RGB_LED_COUNT)
NUM_LEDS = RGB_LED_COUNT

# Test 1: RED
print("Test 1: All LEDs RED")
for i in range(NUM_LEDS):
    np[i] = (255, 0, 0)  # (R, G, B)
np.write()
time.sleep(2)

# Test 2: GREEN
print("Test 2: All LEDs GREEN")
for i in range(NUM_LEDS):
    np[i] = (0, 255, 0)
np.write()
time.sleep(2)

# Test 3: BLUE
print("Test 3: All LEDs BLUE")
for i in range(NUM_LEDS):
    np[i] = (0, 0, 255)
np.write()
time.sleep(2)

# Test 4: ORANGE (for PIR motion detection)
print("Test 4: All LEDs ORANGE")
for i in range(NUM_LEDS):
    np[i] = (255, 165, 0)
np.write()
time.sleep(2)

# Test 5: Individual LED control
print("Test 5: Each LED different color")
np[0] = (255, 0, 0)    # Red
np[1] = (0, 255, 0)    # Green
np[2] = (0, 0, 255)    # Blue
np[3] = (255, 255, 0)  # Yellow
np.write()
time.sleep(2)

# Test 6: Rainbow cycle
print("Test 6: Rainbow animation")
colors = [
    (255, 0, 0),    # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (148, 0, 211),  # Violet
]

for color in colors:
    for i in range(NUM_LEDS):
        np[i] = color
    np.write()
    time.sleep(0.5)

# Turn off all LEDs
print("\nTurning off all LEDs...")
for i in range(NUM_LEDS):
    np[i] = (0, 0, 0)
np.write()

print("\n" + "=" * 40)
print("✓ RGB LED test complete!")
print("=" * 40)
print("\nDid you see all the colors?")
print("- Red, Green, Blue")
print("- Orange (for motion detection)")
print("- Rainbow animation")
