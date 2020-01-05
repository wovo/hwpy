# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

from hwpy_modules.gpio import *
from hwpy_modules.i2c_interface import *

# ===========================================================================
#
# bit-banged i2c
#
# ===========================================================================

class i2c_from_scl_sda( i2c_interface):
    """Software i2c interface.

    This is a bit-banged i2c interface.
    This interface is slow, but can be used on any pin pair.
    """

    def __init__(self, scl: gpoc, sda: gpoc):
        """Create a bit-banged i2c from the scl and sda pins.
        """
        self._scl = scl
        self._sda = sda
        self._scl.write(1)
        self._sda.write(1)

    def _wait(self):
        """Internal function that waits half a bit-cell.

        Currently this function does nothing,
        because bit-banged i2c is already slow.
        """
        pass

    def _write_one_bit(self, v: int):
        """Write a single bit.
        """
        self._scl.write(0)
        self._wait()
        self._sda.write(v)
        self._scl.write(1)

        while not self._scl.read():
            self._wait()

    def _read_one_bit(self) -> int:
        """Read and return a single bit.
        """
        self._scl.write(0)
        self._sda.write(1)
        self._wait()
        self._scl.write(1)

        while not self._scl.read():
            self._wait()

        b = self._sda.read()
        self._wait()
        return b

    def _write_ack(self):
        """Write an i2c ACK.
        """
        self._write_one_bit(0)

    def _write_nack(self):
        """Write an i2c NACK
        """
        self._write_one_bit(1)

    def _write_start(self):
        """Write an i2c START condition.
        """
        self._sda.write(0)
        self._wait()
        self._scl.write(0)
        self._wait()

    def _write_stop(self):
        """Write an i2c STOP condition.
        """
        self._scl.write(0)
        self._wait()
        self._sda.write(0)
        self._wait()
        self._scl.write(1)
        self._wait()
        self._sda.write(1)
        self._wait()

    def _read_ack(self) -> bool:
        """Read and return an i2c ACK bit.
        """
        return not self._read_one_bit()

    def _read_one_byte(self) -> int:
        """Read an return a single byte (as part of an i2c transaction).
        """
        result = 0
        mask = 0x80
        for i in range(0, 8):
            if self._read_one_bit():
                result = result | mask
            mask = mask >> 1
        return result

    def _write_one_byte(self, byte: int):
        """Write a single byte (as part of an i2c transaction).
        """
        mask = 0x80
        for i in range(0, 8):
            self._write_one_bit(byte & mask)
            mask = mask >> 1

    def write(self, address: int, data: list):
        """An i2c write transaction

        Perform an i2c write transaction:
        write the bytes to the chip with
        the (7-bit) address.
        """
        self._write_start()
        self._write_one_byte((address << 1) + 0x00)
        self._read_ack()

        for b in data:
            self._write_one_byte(b)
            self._read_ack()

        self._write_stop()

    def read(self, address: int, n: int) -> list:
        """An i2c read transaction.

        Perform an i2c read transaction:
        read and return n bytes from the chip with
        the (7-bit) address.
        """
        self._write_start()
        self._write_one_byte((address << 1) + 0x01)
        self._read_ack()

        result = []
        first = 1
        for i in range(0, n):
            if not first:
                self._write_ack()
            first = 0
            result.append(self._read_one_byte())

        self._write_nack()
        self._write_stop()
        return result

    def read_command(self, address: int, command: int, n: int) -> list:
        """An i2c read transaction, with an 8 bit register address

        Writes the command byte, then reads and returns the next n bytes from the i2c bus"""
        self.write(address, [command])
        return self.read(address, n)

    def write_command(self, address: int, command: int, data: list):
        """An i2c write transaction, with an 8 bit register address

        Writes the command byte, then the data bytes to the i2c bus
        """
        self.write(address, [command])
        self.write(address, data)