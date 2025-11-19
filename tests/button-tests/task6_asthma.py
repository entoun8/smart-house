"""
Task 6: Asthma Alert - BUTTON TEST VERSION
Press LEFT button to simulate asthma alert conditions
"""

from machine import Pin, I2C
import time
import sys
sys.path.append('/lib')

print("\n" + "="*50)
print("TASK 6: ASTHMA ALERT (Button Test)")
print("="*50)

# Initialize I2C for LCD
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# LCD1602 I2C class
class LCD1602:
    def __init__(self, i2c, addr=0x27):
        self.i2c = i2c
        self.addr = addr
        self.init_lcd()

    def init_lcd(self):
        try:
            self.write_cmd(0x33)
            self.write_cmd(0x32)
            self.write_cmd(0x06)
            self.write_cmd(0x0C)
            self.write_cmd(0x28)
            self.write_cmd(0x01)
            time.sleep(0.2)
            print("LCD initialized!")
        except Exception as e:
            print(f"LCD init error: {e}")

    def write_cmd(self, cmd):
        try:
            self.i2c.writeto(self.addr, bytes([cmd]))
            time.sleep(0.002)
        except:
            pass

    def display(self, line1, line2=""):
        try:
            self.clear()
            # Line 1
            self.write_cmd(0x80)
            for char in line1[:16]:
                self.i2c.writeto(self.addr, bytes([ord(char)]))
                time.sleep(0.001)
            # Line 2
            if line2:
                self.write_cmd(0xC0)
                for char in line2[:16]:
                    self.i2c.writeto(self.addr, bytes([ord(char)]))
                    time.sleep(0.001)
        except Exception as e:
            print(f"LCD display error: {e}")

    def clear(self):
        try:
            self.write_cmd(0x01)
            time.sleep(0.002)
        except:
            pass

# Initialize components
try:
    lcd = LCD1602(i2c)
    lcd_available = True
except Exception as e:
    print(f"LCD not available: {e}")
    lcd_available = False

btn_left = Pin(16, Pin.IN, Pin.PULL_UP)

# Display normal state
if lcd_available:
    lcd.display("Temp: 25C", "Humidity: 45%")
    print("LCD showing normal conditions")

print("\nNormal conditions (no alert)")
print("\nReady! Press LEFT button to simulate asthma alert")
print("="*50)

alert_active = False
last_state = 1  # Button not pressed (pull-up)

while True:
    current_state = btn_left.value()

    # Detect button press (transition from 1 to 0)
    if current_state == 0 and last_state == 1:
        time.sleep(0.05)  # Small debounce delay

        if not alert_active:
            print("\n" + "="*50)
            print("⚠️  ASTHMA ALERT!")
            print("="*50)
            print("Conditions: High humidity + High temperature")
            if lcd_available:
                lcd.display("! ASTHMA ALERT !", "H>50% T>27C")
                print("LCD: Alert displayed")
            alert_active = True
            print("\nPress LEFT button to clear alert")
        else:
            print("\n" + "="*50)
            print("✅ Asthma alert cleared")
            print("="*50)
            if lcd_available:
                lcd.display("Temp: 25C", "Humidity: 45%")
                print("LCD: Normal display")
            alert_active = False
            print("\nPress LEFT button to simulate asthma alert again")

    last_state = current_state
    time.sleep(0.1)
