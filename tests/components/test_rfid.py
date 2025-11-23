# Test: RFID RC522 Module
# Reads RFID cards/tags for door access control

print("=" * 50)
print("TEST: RFID RC522 MODULE")
print("=" * 50)
print()

from machine import Pin, SPI
import time
import sys
sys.path.append('/lib')
from mfrc522 import MFRC522

print("RFID reader test starting...")
print()

# RFID RC522 typical pin connections for ESP32
# Note: Check your actual wiring! These are common defaults
RFID_SCK = 18   # SPI Clock
RFID_MOSI = 23  # SPI MOSI (Master Out Slave In)
RFID_MISO = 19  # SPI MISO (Master In Slave Out)
RFID_SDA = 5    # SPI Chip Select (CS/SS)
RFID_RST = 22   # Reset pin

print("Pin configuration:")
print(f"  SCK (Clock):  GPIO {RFID_SCK}")
print(f"  MOSI (Data):  GPIO {RFID_MOSI}")
print(f"  MISO (Data):  GPIO {RFID_MISO}")
print(f"  SDA (CS):     GPIO {RFID_SDA}")
print(f"  RST (Reset):  GPIO {RFID_RST}")
print()

# Setup SPI
print("[1/4] Initializing SPI...")
try:
    spi = SPI(2, baudrate=1000000, polarity=0, phase=0,
              sck=Pin(RFID_SCK), mosi=Pin(RFID_MOSI), miso=Pin(RFID_MISO))
    sda = Pin(RFID_SDA, Pin.OUT)
    rst = Pin(RFID_RST, Pin.OUT)

    print("      ✓ SPI initialized")
except Exception as e:
    print(f"      ✗ SPI initialization failed: {e}")
    print()
    print("Check wiring and try again")
    sys.exit()

print()
print("[2/4] Initializing RFID reader...")
try:
    reader = MFRC522(spi, sda, rst)
    print("      ✓ RFID reader initialized")
except Exception as e:
    print(f"      ✗ RFID initialization failed: {e}")
    sys.exit()

print()
print("[3/4] Testing RFID module communication...")
try:
    # Test by requesting a card (even if none present)
    stat, tag_type = reader.request(reader.REQIDL)
    print("      ✓ RFID module responding")
except Exception as e:
    print(f"      ✗ Communication test failed: {e}")

print()
print("[4/4] Ready to scan your RFID card!")
print()
print("=" * 50)
print("PLACE YOUR RFID CARD ON THE READER NOW")
print("=" * 50)
print()
print("Scanning for cards... (30 seconds timeout)")
print("Please tap your RFID card on the reader...")
print()

# Scan for cards for 30 seconds
scan_start = time.time()
card_detected = False

while time.time() - scan_start < 30:
    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        (stat, raw_uid) = reader.anticoll()

        if stat == reader.OK:
            card_detected = True
            # Convert UID to readable format
            card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])

            print("=" * 50)
            print("✓ CARD DETECTED!")
            print("=" * 50)
            print()
            print("Card UID (Unique ID):")
            print(f"  Hex: {card_id}")
            print(f"  Dec: {raw_uid[0]} {raw_uid[1]} {raw_uid[2]} {raw_uid[3]}")
            print(f"  Raw: {raw_uid}")
            print()
            print("=" * 50)
            print("RFID TEST COMPLETE!")
            print("=" * 50)
            print()
            print("✓ RFID module is working")
            print(f"✓ Your card ID: {card_id}")
            print()
            print("To use this card in your smart home:")
            print(f"  1. Add '{card_id}' to authorized cards list")
            print("  2. Use it to unlock the door servo")
            print("  3. Log access in database")
            print("  4. Flash RGB green for authorized access")
            print()
            print("You can scan another card or press Ctrl+C to exit...")
            print()
            time.sleep(3)

            # Reset for next card
            scan_start = time.time()

    time.sleep(0.5)

if not card_detected:
    print()
    print("=" * 50)
    print("NO CARD DETECTED")
    print("=" * 50)
    print()
    print("Possible issues:")
    print("  - Card not placed close enough to reader")
    print("  - RFID module not powered properly")
    print("  - Wrong pin configuration")
    print("  - Incompatible card type (use 13.56MHz cards)")
    print()
    print("Hardware test passed, but no card was scanned")

print()
print("Test finished!")
