"""Quick test for LCD and temperature display"""
import time
from machine import Pin, I2C
import config
import sys
sys.path.append('/lib')

print("=" * 30)
print("LCD + Temperature Test")
print("=" * 30)

# Test I2C
print("\n[I2C] Scanning...")
i2c = I2C(0, scl=Pin(config.I2C_SCL_PIN), sda=Pin(config.I2C_SDA_PIN), freq=100000)
devices = i2c.scan()
print(f"[I2C] Found devices: {[hex(d) for d in devices]}")

# Test LCD
if 0x27 in devices or 0x3F in devices:
    addr = 0x27 if 0x27 in devices else 0x3F
    print(f"[LCD] Found at {hex(addr)}")

    from i2c_lcd import I2cLcd
    lcd = I2cLcd(i2c, addr, 2, 16)
    lcd.clear()
    lcd.putstr("LCD Working!")
    time.sleep(2)

    # Test DHT
    print("\n[DHT] Reading...")
    import dht
    d = dht.DHT11(Pin(config.DHT_PIN))
    try:
        d.measure()
        temp = d.temperature()
        humidity = d.humidity()
        print(f"[DHT] Temp: {temp}C, Humidity: {humidity}%")

        # Display on LCD
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(f"Temp: {temp}C")
        lcd.move_to(0, 1)
        lcd.putstr(f"Humidity: {humidity}%")
        print("[LCD] Displayed temperature!")
    except Exception as e:
        print(f"[DHT] Error: {e}")
else:
    print("[LCD] NOT FOUND!")

print("\nDone!")
