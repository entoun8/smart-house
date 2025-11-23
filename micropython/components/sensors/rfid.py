import sys
sys.path.append('/lib')
from mfrc522_i2c import MFRC522_I2C
import config

class RFID:
    def __init__(self):
        self.reader = MFRC522_I2C(
            scl=config.I2C_SCL_PIN,  
            sda=config.I2C_SDA_PIN,  
            addr=0x28
        )

    def scan(self):
        try:
            return self.reader.scan()
        except Exception as e:
            print(f"RFID scan error: {e}")
            return None

    def wait_for_card(self, timeout=5):
        import time
        start = time.time()

        while time.time() - start < timeout:
            card_id = self.scan()
            if card_id:
                return card_id
            time.sleep(0.1)

        return None
