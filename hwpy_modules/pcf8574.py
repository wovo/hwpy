# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

from hwpy_modules.i2c_interface import *
from hwpy_modules.gpio_buffered import *

# ===========================================================================
#
# pcf8574(a)
#
# ===========================================================================

class _pcf8574x:
    """Interface to pcf8754(a) i2c I/O extenders.

    The pcf8574 and pcf8574a are 8-bit i2c I/O extenders.
    The two chips differ only in the i2c (base) slave address.
    The 8 I/O pins provided by these chips are open-collector
    with built-in weak (think 100 kOhm) pull-ups.

    The I/O pins of a chip object can be used
       - as a port: chip.write( 0x55 )
       - as a single pin within the port: chip.pins[ 2 ].write( 0 )
       - as a single named pin: chip.p2.write( 0 )
    """

    def __init__(self, i2c: i2c_interface, address: int):
        """A pcf8574(a) interface from an i2c port and the slave address.

        Note: the address is the 7-bit i2c address.
        """
        self._i2c = i2c
        self._address = address
        self.pins = []
        self._read_buffer = 0
        self._write_buffer = 0
        self.n = 8
        for i in range(0, 8):
            self.pins.append(buffered_pin(self, i))
        self.p0, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7 = self.pins

    def _flush(self):
        """Flush (write) the _write_buffer to the chip.
        """
        self._i2c.write(self._address, [self._write_buffer])

    def _refresh(self):
        """Refresh (read) the _read_buffer from the chip.
        """
        self._read_buffer = self._i2c.read(self._address, 1)[0]

    def write(self, value: int):
        """Write the value to the chips pins.
        """
        self._write_buffer = value
        self._flush()

    def read(self) -> int:
        """Read and return the chip pins.
        """
        self._refresh()
        return self._read_buffer


def pcf8574(i2c: i2c_interface, address: int = 0) -> _pcf8574x:
    """pcf8574 I/O extender interface

    Create a pcf8574 interface from the i2c port and the
    (3-bit) address configured on the 3 address pins a0-a1-a2.
    """
    return _pcf8574x(i2c, 0x20 + address)


def pcf8574a(i2c: i2c_interface, address: int = 0) -> _pcf8574x:
    """pcf8574a I/O extender interface

    Create a pcf8574a interface from the i2c port and the
    (3-bit) address configured on the 3 address pins a0-a1-a2.
    """
    return _pcf8574x(i2c, 0x38 + address)