# Test: Window Servo Motor
# Tests the window opening and closing mechanism

from machine import Pin, PWM
import time
from config import WINDOW_SERVO_PIN

print("=" * 40)
print("TEST: WINDOW SERVO MOTOR")
print("=" * 40)
print(f"Pin: GPIO {WINDOW_SERVO_PIN}")
print("Watch the window!\n")

# Create PWM object for servo control
# Servos use 50Hz frequency (20ms period)
window_servo = PWM(Pin(WINDOW_SERVO_PIN), freq=50)

print("Step 1: Moving window to CLOSED position...")
# 0 degrees (closed) - 0.5ms pulse width = duty ~26
window_servo.duty(26)
time.sleep(2)

print("Step 2: Moving window to HALF OPEN position...")
# 90 degrees (half open) - 1.5ms pulse width = duty ~77
window_servo.duty(77)
time.sleep(2)

print("Step 3: Moving window to FULLY OPEN position...")
# 180 degrees (fully open) - 2.5ms pulse width = duty ~128
window_servo.duty(128)
time.sleep(2)

print("Step 4: Simulating STEAM DETECTION - closing window...")
# When steam is detected, window should close
print("  (This is what happens when water is detected)")
for duty in range(128, 26, -5):
    window_servo.duty(duty)
    time.sleep(0.1)

time.sleep(1)

print("Step 5: Opening window again...")
for duty in range(26, 128, 5):
    window_servo.duty(duty)
    time.sleep(0.1)

time.sleep(1)

print("Step 6: Return to closed position...")
window_servo.duty(26)
time.sleep(1)

# Stop PWM signal
window_servo.deinit()

print("\n" + "=" * 40)
print("✓ Window servo test complete!")
print("=" * 40)
print("\nDid you see the window:")
print("  1. Close completely")
print("  2. Open halfway")
print("  3. Open fully")
print("  4. Close automatically (steam detection simulation)")
print("  5. Open again")
print("  6. Return to closed position")
