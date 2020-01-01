# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

from hwpy_modules.i2c_implementation import *

# ===========================================================================
#
# i2c_registers
#
# ===========================================================================

class i2c_registers:
    """Access to registers in an i2c peripheral chip.

    This class implements access to registers of an i2c peripheral,
    addressed in the customary i2c style: a first byte written is
    the register address for subsequent written bytes (in the same
    transaction) or read bytes (in the next transaction).
    Word (2 byte) values are assumed to be high-byte-first.
    """

    def __init__(self, i2c: i2c_implementation, address: int):
        """Create a register access object.

        A register access object is created from an i2c bus
        and the i2c address of the peripheral.
        """
        self._i2c = i2c
        self._address = address

    def write_byte(self, register: int, value: int):
        """Write the specified byte to the specified register.
        """
        self._i2c.write_command(self._address, register, [value])

    def write_word(self, register: int, value: int):
        """Write the specified word (2 bytes) to the specified register.
        """
        self._i2c.write_command(self._address, register, [value >> 8, value & 0xFF])
        # self._i2c.write(self._address, [register, value >> 8, value & 0xFF])

    def read_byte(self, register: int) -> int:
        """Read and return a byte from the specified register.
        """
        return self._i2c.read_command(self._address, register, 1)[0]

    def read_word(self, register: int) -> int:
        """Read and return a word (2 bytes) from the specified register.
        """
        result = self._i2c.read_command(self._address, register, 2)
        return (result[0] << 8) + result[1]


