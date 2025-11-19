# Test 3: PIR Motion Sensor
# Tests if motion sensor can detect movement

from machine import Pin
import time
from config import PIR_SENSOR_PIN

print("=" * 40)
print("TEST 3: PIR MOTION SENSOR")
print("=" * 40)
print(f"Pin: GPIO {PIR_SENSOR_PIN}")
print("Starting test...\n")

# Create PIR pin as INPUT
pir = Pin(PIR_SENSOR_PIN, Pin.IN)

print("Wave your hand in front of the PIR sensor!")
print("Testing for 10 seconds...\n")

# Monitor for 10 seconds
start_time = time.time()
motion_count = 0

while (time.time() - start_time) < 10:
    if pir.value() == 1:  # Motion detected
        motion_count += 1
        print(f"  ✓ MOTION DETECTED! (Count: {motion_count})")
        time.sleep(1)  # Debounce - wait 1 second
    time.sleep(0.1)  # Check 10 times per second

print(f"\n✓ Test complete!")
print(f"Total motion detections: {motion_count}")
if motion_count > 0:
    print("✓ PIR sensor is working!")
else:
    print("⚠ No motion detected. Try waving your hand again.")
print("=" * 40)
