# MFRC522 I2C Driver for MicroPython
# Fixed for KS5009 Smart Home Kit
from machine import Pin, I2C
import time

# Import config if available, otherwise use defaults
try:
    import mfrc522_config as config
except:
    class config:
        MI_OK = 0
        MI_ERR = 2
        PCD_RESETPHASE = 0x0F
        PCD_TRANSCEIVE = 0x0C
        PCD_AUTHENT = 0x0E
        PICC_REQIDL = 0x26
        PICC_ANTICOLL = 0x93
        CommandReg = 0x01
        CommIEnReg = 0x02
        CommIrqReg = 0x04
        ErrorReg = 0x06
        FIFODataReg = 0x09
        FIFOLevelReg = 0x0A
        ControlReg = 0x0C
        BitFramingReg = 0x0D
        ModeReg = 0x11
        TxControlReg = 0x14
        TxAutoReg = 0x15
        RFCfgReg = 0x26
        TModeReg = 0x2A
        TPrescalerReg = 0x2B
        TReloadRegH = 0x2C
        TReloadRegL = 0x2D


class MFRC522_I2C:
    """MFRC522 RFID reader driver using I2C (fixed for KS5009)"""

    def __init__(self, scl=22, sda=21, addr=0x28):
        self.addr = addr
        # Use hardware I2C for better reliability
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda), freq=400000)
        self.init_device()

    def _write_reg(self, reg, val):
        """Write to MFRC522 register"""
        try:
            self.i2c.writeto(self.addr, bytes([reg, val]))
        except:
            pass

    def _read_reg(self, reg):
        """Read from MFRC522 register"""
        try:
            self.i2c.writeto(self.addr, bytes([reg]))
            return self.i2c.readfrom(self.addr, 1)[0]
        except:
            return 0

    def init_device(self):
        """Initialize MFRC522"""
        # Hard reset
        self._write_reg(config.CommandReg, config.PCD_RESETPHASE)
        time.sleep_ms(100)

        # Timer config
        self._write_reg(config.TModeReg, 0x8D)
        self._write_reg(config.TPrescalerReg, 0x3E)
        self._write_reg(config.TReloadRegL, 30)
        self._write_reg(config.TReloadRegH, 0)

        # TX config
        self._write_reg(config.TxAutoReg, 0x40)
        self._write_reg(config.ModeReg, 0x3D)

        # Set maximum antenna gain (48dB)
        self._write_reg(config.RFCfgReg, 0x70)

        # Turn on BOTH antenna outputs
        val = self._read_reg(config.TxControlReg)
        self._write_reg(config.TxControlReg, val | 0x03)

    def _to_card(self, command, data):
        """Send command to card"""
        irq = 0x00
        irq_wait = 0x00
        last_bits = None
        n = 0

        if command == config.PCD_AUTHENT:
            irq = 0x12
            irq_wait = 0x10

        if command == config.PCD_TRANSCEIVE:
            irq = 0x77
            irq_wait = 0x30

        # Write data to FIFO
        self._write_reg(config.CommIEnReg, irq | 0x80)
        self._write_reg(config.CommIrqReg, 0x7F)
        self._write_reg(config.FIFOLevelReg, 0x80)

        for byte in data:
            self._write_reg(config.FIFODataReg, byte)

        self._write_reg(config.CommandReg, command)

        if command == config.PCD_TRANSCEIVE:
            # Set StartSend bit to start transmission
            val = self._read_reg(config.BitFramingReg)
            self._write_reg(config.BitFramingReg, val | 0x80)

        # Wait for command to complete
        i = 2000
        while True:
            n = self._read_reg(config.CommIrqReg)
            i -= 1
            if not ((i != 0) and not (n & 0x01) and not (n & irq_wait)):
                break

        self._write_reg(config.BitFramingReg, 0x00)

        if i != 0:
            if (self._read_reg(config.ErrorReg) & 0x1B) == 0x00:
                status = config.MI_OK

                if command == config.PCD_TRANSCEIVE:
                    n = self._read_reg(config.FIFOLevelReg)
                    last_bits = self._read_reg(config.ControlReg) & 0x07

                    if last_bits != 0:
                        back_len = (n - 1) * 8 + last_bits
                    else:
                        back_len = n * 8

                    if n == 0:
                        n = 1

                    if n > 16:
                        n = 16

                    # Read data from FIFO
                    back_data = []
                    for _ in range(n):
                        back_data.append(self._read_reg(config.FIFODataReg))

                    return (status, back_data, back_len)
                else:
                    return (status, None, None)
            else:
                return (config.MI_ERR, None, None)

        return (config.MI_ERR, None, None)

    def request(self, req_mode=config.PICC_REQIDL):
        """Request card"""
        self._write_reg(config.BitFramingReg, 0x07)
        (status, back_data, back_bits) = self._to_card(config.PCD_TRANSCEIVE, [req_mode])

        if (status != config.MI_OK) or (back_bits != 0x10):
            status = config.MI_ERR

        return (status, back_bits)

    def anticoll(self):
        """Anti-collision detection"""
        back_data = []
        serial_num = []

        serial_num_check = 0

        self._write_reg(config.BitFramingReg, 0x00)

        (status, back_data, back_bits) = self._to_card(config.PCD_TRANSCEIVE, [config.PICC_ANTICOLL, 0x20])

        if status == config.MI_OK:
            if len(back_data) == 5:
                for i in range(4):
                    serial_num_check = serial_num_check ^ back_data[i]

                if serial_num_check != back_data[4]:
                    status = config.MI_ERR
                else:
                    serial_num = back_data[:4]

        return (status, serial_num)

    def scan(self):
        """Scan for RFID card and return UID"""
        (status, tag_type) = self.request()

        if status == config.MI_OK:
            (status, uid) = self.anticoll()

            if status == config.MI_OK and len(uid) == 4:
                card_id = "0x%02x%02x%02x%02x" % (uid[0], uid[1], uid[2], uid[3])
                return card_id

        return None

    def read_card(self):
        """Read card UID (alias for scan)"""
        return self.scan()
