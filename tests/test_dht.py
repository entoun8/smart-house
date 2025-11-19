# Test: DHT11 Temperature & Humidity Sensor
# Tests temperature and humidity readings

import dht
from machine import Pin
import time
from config import DHT_PIN

print("=" * 40)
print("TEST: DHT11 TEMPERATURE & HUMIDITY")
print("=" * 40)
print(f"Pin: GPIO {DHT_PIN}")
print("Reading sensor...\n")

# Create DHT sensor object
sensor = dht.DHT11(Pin(DHT_PIN))

# Take 5 readings
for i in range(5):
    try:
        sensor.measure()  # Trigger measurement
        temp = sensor.temperature()  # Get temperature in Celsius
        humidity = sensor.humidity()  # Get humidity in %

        print(f"Reading {i+1}/5:")
        print(f"  Temperature: {temp}°C")
        print(f"  Humidity: {humidity}%")
        print()

        time.sleep(2)  # Wait 2 seconds between readings

    except OSError as e:
        print(f"  Failed to read sensor: {e}")
        print("  (Make sure DHT11 is properly connected)")
        time.sleep(2)

print("=" * 40)
print("✓ DHT sensor test complete!")
print("=" * 40)
