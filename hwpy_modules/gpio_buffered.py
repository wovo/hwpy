# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

# ===========================================================================
#
# buffered pin
#
# ===========================================================================

class buffered_pin:
    """A buffered GPIO pin.

    A buffered GPIO pin performs GPIO read operations via a read_buffer
    that can be refreshed, and write operations via a write_buffer
    that can be flushed.
    
    This is usefull when the GPIO pins are on an external chip like a
    74HC594 or a PCF8574.
    """

    def __init__(self, master, nr: int):
        """Create a buffered pin from its master and it bit number.
        """
        self._master = master
        self._mask = 1 << nr

    def write(self, v: int):
        """Write the bit via the master.

        The bit value v is put in the master.write_buffer at the
        bit position nr (as specified to the constructor)
        and master.flush() is called.
        """
        if v:
            self._master._write_buffer |= self._mask
        else:
            self._master._write_buffer &= ~ self._mask
        self._master._flush()

    def read(self) -> bool:
        """Read the bit via the master and return it.

        The master.refresh() is called and the bit at position nr
        (as specified to the constructor) from the master.read_buffer
        is returned.
        """
        self._master._refresh()
        return (self._master._read_buffer & self._mask) != 0