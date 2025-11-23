# Test: Water/Steam Sensor
# Detects: Water droplets, steam, rain

print("=" * 50)
print("TEST: WATER/STEAM SENSOR")
print("=" * 50)
print()

from machine import Pin, ADC
import time
from config import WATER_SENSOR_PIN

# Setup water sensor (analog input)
water_sensor = ADC(Pin(WATER_SENSOR_PIN))
water_sensor.atten(ADC.ATTN_11DB)  # Full range: 0-3.3V
water_sensor.width(ADC.WIDTH_12BIT)  # 12-bit resolution: 0-4095

print("Water sensor test starting...")
print(f"Using pin: GPIO {WATER_SENSOR_PIN} (ADC)")
print()
print("How it works:")
print("  - Low values (0-1000) = Dry (no water)")
print("  - Medium values (1000-2500) = Damp/Steam")
print("  - High values (2500-4095) = Wet (water detected)")
print()
print("Reading for 10 seconds...")
print("Try:")
print("  - Breathe on sensor (steam)")
print("  - Touch with wet finger (water)")
print()

# Monitor for 10 seconds
start_time = time.time()
max_value = 0
min_value = 4095

while time.time() - start_time < 10:
    value = water_sensor.read()

    # Track min/max
    if value > max_value:
        max_value = value
    if value < min_value:
        min_value = value

    # Determine status
    if value < 1000:
        status = "DRY ✓"
    elif value < 2500:
        status = "DAMP 💧"
    else:
        status = "WET 🌧️"

    print(f"Water level: {value:4d} | {status}")
    time.sleep(1)

print()
print("=" * 50)
print("WATER SENSOR TEST COMPLETE!")
print("=" * 50)
print()
print(f"✓ Minimum reading: {min_value}")
print(f"✓ Maximum reading: {max_value}")
print(f"✓ Range detected: {max_value - min_value}")
print()

if max_value > 2000:
    print("✓ Sensor is WORKING - detected moisture!")
else:
    print("ℹ Sensor is ready - stayed dry during test")

print()
print("Next: Use in main.py to:")
print("  - Close window when rain detected")
print("  - Flash RGB LED blue")
print("  - Send MQTT alert")
