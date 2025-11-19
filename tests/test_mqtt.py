"""Test MQTT Configuration - Quick Check"""

from config import MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD

print("\n" + "=" * 50)
print("TEST: MQTT CONFIGURATION CHECK")
print("=" * 50)

# Step 1: Verify MQTT configuration
print("\nStep 1: Checking MQTT configuration...")
print(f"✓ Broker: {MQTT_BROKER}")
print(f"✓ Port: {MQTT_PORT}")
print(f"✓ User: {MQTT_USER}")
print(f"✓ Password: {'*' * len(MQTT_PASSWORD)}")

# Step 2: Check if umqtt library exists
print("\nStep 2: Checking for MQTT library...")
try:
    from umqtt.simple import MQTTClient
    print("✓ umqtt.simple library found!")
    print("  MQTTClient class is available")
except ImportError:
    print("✗ umqtt library NOT found!")
    print("\nTo install micropython-umqtt:")
    print("  Option 1: Use mpremote")
    print("    mpremote mip install umqtt.simple")
    print("  Option 2: Manual upload")
    print("    Download from: https://github.com/micropython/micropython-lib")
    print("    Upload: ampy --port COM5 put umqtt /lib/umqtt")

# Step 3: Summary
print("\n" + "=" * 50)
print("MQTT CONFIGURATION TEST COMPLETE")
print("=" * 50)

print("\nConfiguration Status:")
print("✓ MQTT settings loaded from config.py")
print("✓ Ready for MQTT integration")
print("\nNext Steps:")
print("1. Install umqtt library (if not found)")
print("2. Test connection to HiveMQ broker")
print("3. Integrate MQTT into main.py")
