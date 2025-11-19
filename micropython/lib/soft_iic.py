# Software I2C implementation for MFRC522
from machine import Pin
import time

class SoftI2C:
    """Software I2C for MFRC522 RFID module"""

    def __init__(self, scl, sda, freq=100000):
        self.scl = Pin(scl, Pin.OUT)
        self.sda = Pin(sda, Pin.OUT)
        self.freq = freq
        self.delay = 1000000 // freq // 2  # microseconds

    def _delay(self):
        time.sleep_us(self.delay)

    def _start(self):
        """I2C start condition"""
        self.sda.init(Pin.OUT)
        self.sda.value(1)
        self.scl.value(1)
        self._delay()
        self.sda.value(0)
        self._delay()
        self.scl.value(0)
        self._delay()

    def _stop(self):
        """I2C stop condition"""
        self.sda.init(Pin.OUT)
        self.sda.value(0)
        self.scl.value(1)
        self._delay()
        self.sda.value(1)
        self._delay()

    def _write_bit(self, bit):
        """Write a single bit"""
        self.sda.init(Pin.OUT)
        self.sda.value(bit)
        self._delay()
        self.scl.value(1)
        self._delay()
        self.scl.value(0)
        self._delay()

    def _read_bit(self):
        """Read a single bit"""
        self.sda.init(Pin.IN)
        self.scl.value(1)
        self._delay()
        bit = self.sda.value()
        self.scl.value(0)
        self._delay()
        return bit

    def _write_byte(self, byte):
        """Write a byte and return ACK"""
        for i in range(8):
            self._write_bit((byte >> (7 - i)) & 1)
        # Read ACK
        ack = self._read_bit()
        return ack == 0

    def _read_byte(self, ack=True):
        """Read a byte and send ACK"""
        byte = 0
        for i in range(8):
            byte = (byte << 1) | self._read_bit()
        # Send ACK
        self._write_bit(0 if ack else 1)
        return byte

    def writeto(self, addr, data):
        """Write data to I2C address"""
        self._start()
        if not self._write_byte((addr << 1) | 0):  # Write address
            self._stop()
            raise OSError("No ACK from device")

        for byte in data:
            if not self._write_byte(byte):
                self._stop()
                raise OSError("No ACK during write")

        self._stop()

    def readfrom(self, addr, nbytes):
        """Read data from I2C address"""
        self._start()
        if not self._write_byte((addr << 1) | 1):  # Read address
            self._stop()
            raise OSError("No ACK from device")

        data = bytearray()
        for i in range(nbytes):
            data.append(self._read_byte(ack=(i < nbytes - 1)))

        self._stop()
        return data

    def scan(self):
        """Scan for I2C devices"""
        devices = []
        for addr in range(0x08, 0x78):
            try:
                self._start()
                ack = self._write_byte((addr << 1) | 0)
                self._stop()
                if ack:
                    devices.append(addr)
            except:
                pass
        return devices
