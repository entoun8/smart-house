from machine import Pin, I2C
import config
import sys
sys.path.append('/lib')


class LCD:
    """LCD1602 Display (16x2)"""
    def __init__(self):
        import time
        self.lcd = None
        self.i2c = None
        self.addr = None

        # Try to initialize with retries
        for attempt in range(3):
            try:
                # Use slower I2C frequency for LCD stability
                self.i2c = I2C(0, scl=Pin(config.I2C_SCL_PIN), sda=Pin(config.I2C_SDA_PIN), freq=100000)
                time.sleep(0.1)

                # Find LCD address (0x27 or 0x3F)
                devices = self.i2c.scan()
                self.addr = 0x27 if 0x27 in devices else (0x3F if 0x3F in devices else None)

                if self.addr:
                    from i2c_lcd import I2cLcd
                    self.lcd = I2cLcd(self.i2c, self.addr, 2, 16)
                    print(f"[LCD] Connected at 0x{self.addr:02X}")
                    break
                else:
                    print(f"[LCD] Not found (attempt {attempt+1})")
                    time.sleep(0.5)
            except Exception as e:
                print(f"[LCD] Init error (attempt {attempt+1}): {e}")
                time.sleep(0.5)

    def is_connected(self):
        """Check if LCD is available"""
        return self.lcd is not None

    def clear(self):
        """Clear the LCD display"""
        if self.lcd:
            self.lcd.clear()

    def write(self, text, row=0, col=0):
        """Write text to LCD at specified position"""
        if self.lcd:
            self.lcd.move_to(col, row)
            self.lcd.putstr(text)

    def display_alert(self, line1, line2=""):
        """Display alert message (2 lines)"""
        if self.lcd:
            try:
                self.lcd.clear()
                self.lcd.move_to(0, 0)
                self.lcd.putstr(line1[:16])  # Max 16 chars
                if line2:
                    self.lcd.move_to(0, 1)
                    self.lcd.putstr(line2[:16])  # Max 16 chars
            except OSError as e:
                print(f"[LCD] Write error: {e}")
