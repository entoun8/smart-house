# Test 1: Yellow LED
# Tests basic digital output - turning LED on and off

from machine import Pin
import time
from config import LED_PIN

print("=" * 40)
print("TEST 1: YELLOW LED")
print("=" * 40)
print(f"Pin: GPIO {LED_PIN}")
print("Starting test...\n")

# Create LED pin as OUTPUT
led = Pin(LED_PIN, Pin.OUT)

# Blink 5 times
for i in range(5):
    print(f"  Blink {i+1}/5 - LED ON")
    led.on()  # Turn LED on (HIGH signal)
    time.sleep(1)

    print(f"  Blink {i+1}/5 - LED OFF")
    led.off()  # Turn LED off (LOW signal)
    time.sleep(1)

print("\n✓ Test complete!")
print("Did you see the yellow LED blinking 5 times?")
print("=" * 40)
