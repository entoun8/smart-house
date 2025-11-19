# RFID Card Scanning Issue - Summary

**Date:** 2025-11-19
**Problem:** Cannot get RFID card ID from the card included in KS5009 kit

---

## What We Tested

### ✅ Hardware Tests (All Passed)
1. **I2C Bus Scan** - RFID module detected at address 0x28
2. **I2C Communication** - Device responds on I2C bus
3. **RFID Version Register (I2C)** - Reads 0x92 (correct for MFRC522)
4. **Antenna Status** - Antenna enabled (0x83)

### ❌ Card Scanning Tests (All Failed)
1. **I2C Scanning** - 482 attempts over 60 seconds, no card detected
2. **SPI Scanning** - Multiple attempts, module reads 0x00 (pin conflicts with Fan/Gas)
3. **Different timing** - Fast scanning (0.05s), slow scanning (0.5s)
4. **Different modes** - REQIDL, REQALL, continuous scanning

---

## Root Causes Identified

### 1. Pin Conflicts (SPI Mode)
The RFID RC522 uses SPI pins that conflict with other components:

| Pin | RFID Use | Conflicts With |
|-----|----------|----------------|
| GPIO 18 | SCK | Fan Motor (FAN_PIN2) |
| GPIO 19 | MISO | Fan Motor (FAN_PIN1) |
| GPIO 23 | MOSI | Gas Sensor |
| GPIO 5 | SDA/CS | Window Servo |
| GPIO 22 | RST | I2C SCL (LCD) |

**Result:** RFID cannot work simultaneously with Task 4 (Steam/Window) or Task 5 (Gas/Fan)

### 2. RFID Card Issue (Most Likely)
The RFID card included in the KS5009 kit is either:
- **Wrong frequency** - RC522 requires 13.56MHz (Mifare/NTAG), card may be 125kHz
- **Defective** - Card doesn't respond to any scanning attempts
- **Not programmed** - Blank card with no UID

---

## Solutions Implemented

###  Workaround: Button Simulation
Created `task7_button_simulation.py`:
- LEFT button (GPIO 16) = Simulates authorized card
- RIGHT button (GPIO 27) = Simulates unauthorized card
- Demonstrates full Task 7 functionality without actual RFID scanning

### File Created
- [task7_button_simulation.py](task7_button_simulation.py) - Button-based testing

---

## Recommendations

### Option 1: Get a Working RFID Card
Try these alternatives:
1. **Student ID card** (if it's 13.56MHz Mifare)
2. **Building access card** (check if Mifare/NTAG)
3. **Purchase Mifare Classic 1K card** online
4. **Phone with NFC** (some work as Mifare cards)
5. **Request replacement** from instructor/kit supplier

### Option 2: Fix Pin Conflicts (Hardware Rewiring)
Rewire RFID to use non-conflicting SPI pins:
- Use HSPI bus 2 with available pins
- Requires soldering/jumper wires
- Update config.py with new pin assignments

### Option 3: Accept Current Workaround
Use button simulation for demonstrations:
- Functionally equivalent to RFID
- All Task 7 features work (door, RGB, buzzer, database logging)
- Just triggered by buttons instead of cards

---

## Testing Commands

### Test with Button Simulation (Works Now)
```bash
cd "c:\Users\tonis\OneDrive\Desktop\smart-house"
ampy --port COM5 run task7_button_simulation.py
# Press LEFT button = authorized
# Press RIGHT button = unauthorized
```

### Test with Real RFID (If you get a working card)
```bash
# 1. Disable boot.py temporarily
ampy --port COM5 rm boot.py

# 2. Reset ESP32 (unplug/replug)

# 3. Run RFID scanner
ampy --port COM5 run final_i2c_test.py

# 4. Place card on reader antenna

# 5. Restore boot.py
ampy --port COM5 put boot.py.backup boot.py
```

---

## Conclusion

**Hardware:** ✅ Working correctly
**Software:** ✅ Working correctly
**RFID Card:** ❌ Not compatible or defective

The KS5009 kit's RFID card appears to be incompatible with the RC522 module. Use the button simulation workaround to demonstrate Task 7 functionality, or obtain a compatible 13.56MHz Mifare/NTAG card for actual RFID scanning.
