# Test: LCD1602 Display (I2C)
# 16 characters x 2 rows display

print("=" * 50)
print("TEST: LCD1602 DISPLAY")
print("=" * 50)
print()

from machine import Pin, I2C
import time
import sys
sys.path.append('/lib')
from i2c_lcd import I2cLcd
from config import I2C_SCL_PIN, I2C_SDA_PIN

print("LCD display test starting...")
print(f"Using I2C pins: SCL={I2C_SCL_PIN}, SDA={I2C_SDA_PIN}")
print()

# Setup I2C
i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)

print("[1/5] Scanning for I2C devices...")
devices = i2c.scan()

if len(devices) == 0:
    print("      ✗ No I2C devices found!")
    print()
    print("Troubleshooting:")
    print("  - Check LCD is connected")
    print("  - Check I2C wiring (SCL, SDA, VCC, GND)")
    print("  - Try different I2C address (0x27 or 0x3F)")
else:
    print(f"      ✓ Found {len(devices)} device(s)")
    for device in devices:
        print(f"      I2C Address: 0x{device:02X}")

print()

# Common LCD I2C addresses
LCD_ADDR = 0x27  # Try 0x3F if this doesn't work

if LCD_ADDR in devices or 0x3F in devices:
    # Use detected address
    if 0x27 in devices:
        LCD_ADDR = 0x27
    elif 0x3F in devices:
        LCD_ADDR = 0x3F

    print(f"[2/5] Using LCD at address 0x{LCD_ADDR:02X}")
    print()

    print("[3/5] Initializing LCD...")
    try:
        lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)
        print("      ✓ LCD initialized successfully")
    except Exception as e:
        print(f"      ✗ LCD initialization failed: {e}")
        print()
        print("=" * 50)
        print("LCD TEST FAILED")
        print("=" * 50)
        sys.exit()

    print()
    print("[4/5] Displaying text on LCD...")

    try:
        # Clear and display simple message
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("  Smart House")
        lcd.move_to(0, 1)
        lcd.putstr("  ESP32 Ready!")
        print("      ✓ Text displayed on LCD")

    except Exception as e:
        print(f"      ✗ Display failed: {e}")

    print()
    print("[5/5] LCD test complete!")
    print()
    print("=" * 50)
    print("LCD TEST COMPLETE!")
    print("=" * 50)
    print()
    print(f"✓ LCD working at address 0x{LCD_ADDR:02X}")
    print("✓ Text displayed: 'Smart House' / 'ESP32 Ready!'")

else:
    print("[2/5] LCD not found at common addresses")
    print()
    print("=" * 50)
    print("LCD TEST - DEVICE NOT FOUND")
    print("=" * 50)
    print()
    print("Common LCD I2C addresses: 0x27, 0x3F")
    print("Check:")
    print("  - LCD power (VCC, GND)")
    print("  - I2C wiring (SCL to GPIO 22, SDA to GPIO 21)")
    print("  - Contrast adjustment (potentiometer on back)")

print()
print("Message displayed on LCD for 5 seconds...")
time.sleep(5)
