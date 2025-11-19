from machine import Pin, SPI
import sys
sys.path.append('/lib')
from mfrc522 import MFRC522
import config


class RFID:
    """RFID RC522 reader for access control"""
    def __init__(self):
        self.spi = SPI(
            2,
            baudrate=1000000,
            polarity=0,
            phase=0,
            sck=Pin(config.RFID_SCK),
            mosi=Pin(config.RFID_MOSI),
            miso=Pin(config.RFID_MISO)
        )
        self.sda = Pin(config.RFID_SDA, Pin.OUT)
        self.rst = Pin(config.RFID_RST, Pin.OUT)

        self.reader = MFRC522(self.spi, self.sda, self.rst)

    def scan(self):
        """Scan for RFID card

        Returns:
            str: Card ID in hex format (e.g., "0x12345678") or None if no card
        """
        try:
            stat, tag_type = self.reader.request(self.reader.REQIDL)

            if stat == self.reader.OK:
                stat, raw_uid = self.reader.anticoll()

                if stat == self.reader.OK:
                    card_id = "0x%02x%02x%02x%02x" % (
                        raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]
                    )
                    return card_id
        except Exception as e:
            print(f"RFID scan error: {e}")

        return None

    def wait_for_card(self, timeout=5):
        """Wait for a card to be scanned

        Args:
            timeout: Maximum seconds to wait

        Returns:
            str: Card ID or None if timeout
        """
        import time
        start = time.time()

        while time.time() - start < timeout:
            card_id = self.scan()
            if card_id:
                return card_id
            time.sleep(0.1)

        return None
