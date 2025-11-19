# Test: Gas Sensor (MQ-2)
# Detects: LPG, smoke, alcohol, propane, hydrogen, methane, carbon monoxide

print("=" * 50)
print("TEST: GAS SENSOR (MQ-2)")
print("=" * 50)
print()

from machine import Pin
import time
from config import GAS_SENSOR_PIN

# Setup gas sensor (digital output)
gas_sensor = Pin(GAS_SENSOR_PIN, Pin.IN)

print("Gas sensor test starting...")
print(f"Using pin: GPIO {GAS_SENSOR_PIN}")
print()
print("How it works:")
print("  - Value 0 = No gas detected (safe)")
print("  - Value 1 = Gas detected! (danger)")
print()
print("Testing for 10 seconds...")
print("Try holding lighter near sensor (don't ignite!)")
print()

# Monitor for 10 seconds
start_time = time.time()
gas_detected_count = 0

while time.time() - start_time < 10:
    gas_value = gas_sensor.value()

    if gas_value == 1:
        print("🚨 GAS DETECTED! Value: 1")
        gas_detected_count += 1
        time.sleep(0.5)
    else:
        print("✓ Safe. Value: 0")
        time.sleep(1)

print()
print("=" * 50)
print("GAS SENSOR TEST COMPLETE!")
print("=" * 50)
print()
print(f"✓ Gas detections during test: {gas_detected_count}")
print()
if gas_detected_count > 0:
    print("✓ Sensor is WORKING - detected gas!")
else:
    print("ℹ Sensor is ready - no gas detected during test")
print()
print("Next: Use in main.py to:")
print("  - Turn on fan when gas detected")
print("  - Flash RGB LED red")
print("  - Send MQTT alert")
