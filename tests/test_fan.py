# Test: Fan Motor
# Tests the DC motor fan (forward, reverse, stop)

print("=" * 50)
print("TEST: FAN MOTOR")
print("=" * 50)
print()

from machine import Pin
import time
from config import FAN_PIN1, FAN_PIN2

# Setup fan pins
fan_pin1 = Pin(FAN_PIN1, Pin.OUT)
fan_pin2 = Pin(FAN_PIN2, Pin.OUT)

print("Fan motor test starting...")
print(f"Using pins: {FAN_PIN1}, {FAN_PIN2}")
print()

# Test 1: Spin forward
print("[1/4] Spinning fan FORWARD for 3 seconds...")
fan_pin1.on()
fan_pin2.off()
time.sleep(3)
print("      ✓ Forward complete")
print()

# Stop
print("[2/4] Stopping fan for 2 seconds...")
fan_pin1.off()
fan_pin2.off()
time.sleep(2)
print("      ✓ Fan stopped")
print()

# Test 2: Spin backward (reverse)
print("[3/4] Spinning fan BACKWARD for 3 seconds...")
fan_pin1.off()
fan_pin2.on()
time.sleep(3)
print("      ✓ Backward complete")
print()

# Stop
print("[4/4] Stopping fan...")
fan_pin1.off()
fan_pin2.off()
print("      ✓ Fan stopped")
print()

print("=" * 50)
print("FAN TEST COMPLETE!")
print("=" * 50)
print()
print("✓ Fan can spin forward (ventilation)")
print("✓ Fan can spin backward (reverse)")
print("✓ Fan can stop")
print()
print("Next: Use fan for gas detection ventilation")
