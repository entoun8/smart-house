from machine import Pin, I2C
import config
import sys
sys.path.append('/lib')


class LCD:
    """LCD1602 Display (16x2)"""
    def __init__(self):
        self.i2c = I2C(0, scl=Pin(config.I2C_SCL_PIN), sda=Pin(config.I2C_SDA_PIN), freq=400000)
        # Find LCD address (0x27 or 0x3F)
        devices = self.i2c.scan()
        self.addr = 0x27 if 0x27 in devices else (0x3F if 0x3F in devices else None)

        self.lcd = None
        if self.addr:
            try:
                from i2c_lcd import I2cLcd
                self.lcd = I2cLcd(self.i2c, self.addr, 2, 16)
            except:
                self.lcd = None

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
            self.lcd.clear()
            self.lcd.move_to(0, 0)
            self.lcd.putstr(line1[:16])  # Max 16 chars
            if line2:
                self.lcd.move_to(0, 1)
                self.lcd.putstr(line2[:16])  # Max 16 chars
