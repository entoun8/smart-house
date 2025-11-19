# Test: Door Servo Motor
# Tests the door opening and closing mechanism

from machine import Pin, PWM
import time
from config import DOOR_SERVO_PIN

print("=" * 40)
print("TEST: DOOR SERVO MOTOR")
print("=" * 40)
print(f"Pin: GPIO {DOOR_SERVO_PIN}")
print("Watch the door!\n")

# Create PWM object for servo control
# Servos use 50Hz frequency (20ms period)
door_servo = PWM(Pin(DOOR_SERVO_PIN), freq=50)

print("Step 1: Moving door to CLOSED position...")
# 0 degrees (closed) - 0.5ms pulse width = duty ~26
door_servo.duty(26)
time.sleep(2)

print("Step 2: Moving door to HALF OPEN position...")
# 90 degrees (half open) - 1.5ms pulse width = duty ~77
door_servo.duty(77)
time.sleep(2)

print("Step 3: Moving door to FULLY OPEN position...")
# 180 degrees (fully open) - 2.5ms pulse width = duty ~128
door_servo.duty(128)
time.sleep(2)

print("Step 4: Closing door slowly...")
# Gradually close the door
for duty in range(128, 26, -5):
    door_servo.duty(duty)
    time.sleep(0.1)

time.sleep(1)

print("Step 5: Opening door slowly...")
# Gradually open the door
for duty in range(26, 128, 5):
    door_servo.duty(duty)
    time.sleep(0.1)

time.sleep(1)

print("Step 6: Return to closed position...")
door_servo.duty(26)
time.sleep(1)

# Stop PWM signal
door_servo.deinit()

print("\n" + "=" * 40)
print("✓ Door servo test complete!")
print("=" * 40)
print("\nDid you see the door:")
print("  1. Close completely")
print("  2. Open halfway")
print("  3. Open fully")
print("  4. Close slowly")
print("  5. Open slowly")
print("  6. Return to closed position")
