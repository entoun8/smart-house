from TestingSuite import PicoTestBase
from components.displays.lcd import LCD

class LCDTest(PicoTestBase):
    def test_lcd_initialization(self):
        lcd = LCD()
        assert lcd is not None
        assert lcd.i2c is not None

    def test_lcd_clear_method_exists(self):
        lcd = LCD()
        assert hasattr(lcd, 'clear')
        assert callable(lcd.clear)

    def test_lcd_write_method_exists(self):
        lcd = LCD()
        assert hasattr(lcd, 'write')
        assert callable(lcd.write)

    def test_lcd_set_cursor_method_exists(self):
        lcd = LCD()
        assert hasattr(lcd, 'set_cursor')
        assert callable(lcd.set_cursor)

    def test_lcd_write_text(self):
        lcd = LCD()
        lcd.clear()
        lcd.write("Test")
        assert True

    def test_lcd_set_cursor_position(self):
        lcd = LCD()
        lcd.set_cursor(0, 0)
        lcd.set_cursor(1, 0)
        assert True

    def test_lcd_multiple_lines(self):
        lcd = LCD()
        lcd.clear()
        lcd.set_cursor(0, 0)
        lcd.write("Line 1")
        lcd.set_cursor(1, 0)
        lcd.write("Line 2")
        assert True
