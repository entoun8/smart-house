# Test 4: WiFi Connection
# Tests if ESP32 can connect to your WiFi network

import network
import time
from config import WIFI_SSID, WIFI_PASSWORD

print("=" * 40)
print("TEST 4: WiFi CONNECTION")
print("=" * 40)
print(f"Network: {WIFI_SSID}")
print("Connecting...\n")

# Create WiFi station interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # Activate the interface

# Connect to WiFi
wlan.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for connection (max 10 seconds)
timeout = 10
while not wlan.isconnected() and timeout > 0:
    print(f"  Waiting... ({timeout}s left)")
    time.sleep(1)
    timeout -= 1

# Check if connected
if wlan.isconnected():
    print("\n✓ Connected to WiFi!")
    print(f"  IP Address: {wlan.ifconfig()[0]}")
    print(f"  Subnet: {wlan.ifconfig()[1]}")
    print(f"  Gateway: {wlan.ifconfig()[2]}")
    print(f"  DNS: {wlan.ifconfig()[3]}")
else:
    print("\n✗ Failed to connect to WiFi")
    print("  Check your SSID and password")

print("=" * 40)
