# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

import typing

from hwpy_modules.xy import *
from hwpy_modules.gpio import *
from hwpy_modules.port import *
from hwpy_modules.pcf8574 import *


# ===========================================================================
#
# hd44780
#
# ===========================================================================

class hd44780:
    """4-bit interface to an HD44780 (character) LCD.

    Some characters are treated special:
      - '\\n' puts the cursor at the first position of the next line
      - '\\r' puts the cursor at the start of the current line
      - '\\f' puts the cursor at the top-left position and clears the lcd
      - '\\txxyy' puts the cursor at the position (xx,yy)
    """

    @classmethod
    def from_pcf8574(cls, pcf_port: pcf8574, size: xy) -> 'hd44780':
        """Create an HD44780 instance from an i2c bus

        This should be used when using a pcf8574 i2c backpack with the lcd"""
        pcf_port.p3.write(True)
        port_4bit = port([pcf_port.pins[i] for i in range(4, 8)])
        return hd44780(pcf_port.p0, pcf_port.p2, port_4bit, size)

    def __init__(self, pin_rs: gpo, pin_e: gpo, port_data: port, size: xy):
        """Interface to a hd44780.

        Construct an interface to an LCD controlled by an hd44780 chip
        from the RS and E pins, the 4-bit port to the D4..D8 pins,
        and the size (number of characters per line, and number of lines),
        and initializes the controller.
        """
        self._rs = pin_rs
        self._e = pin_e
        self._data = port_data
        self.size = size
        self._position = xy(0, 0)

        self._e.write(0)
        self._rs.write(0)
        wait_ms(100)

        # interface initialization: make sure the LCD is in 4 bit mode
        # (magical sequence, taken from the HD44780 data-sheet)
        self._write4(0x03)
        wait_ms(15)
        self._write4(0x03)
        wait_us(100)
        self._write4(0x03)
        self._write4(0x02)  # 4 bit mode

        # functional initialization
        self.command(0x28)  # 4 bit mode, 2 lines, 5x8 font
        self.command(0x0C)  # display on, no cursor, no blink
        self.clear()  # clear display, 'cursor' home
        self.command(0x06)  # Set mode left-to-right
        self._goto_state = 0

    def _write4(self, nibble: int):
        """Write a nibble (4 bits) to the chip.
        """
        wait_us(10)
        self._data.write(nibble)
        wait_us(20)
        self._e.write(1)
        wait_us(20)
        self._e.write(0)
        wait_us(100)

    def _write8(self, is_data: int, byte: int):
        """Write a byte (two nibbles) as command or data.
        """
        self._rs.write(is_data)
        self._write4((byte >> 4))
        self._write4(byte)

    def command(self, cmd: int):
        """Write a command byte to the LCD

        Use this function only for features that are not
        provided by the console interface, like the definition
        of the user-defined characters.
        """
        self._write8(0, cmd)

    def data(self, char: typing.Union[str, bytes]):
        """Write a data byte to the LCD

        Use this function only for features that are not
        provided by the console interface, like the definition
        of the user-defined characters.
        """
        self._write8(1, ord(char))

    def clear(self):
        """Clear the display and put the cursor at (0,0).
        """
        self.command(0x01)
        wait_ms(5)
        self.cursor(xy(0, 0))

    def cursor(self, position: xy):
        """Place the cursor at the position.
        """
        self._position = position

        if self.size.y == 1:
            if self._position.x < 8:
                self.command(0x80 + self._position.x)
            else:
                self.command(0x80 + 0x40 + (self._position.x - 8))
        else:
            if self.size.y == 2:
                self.command(
                    0x80
                    + (0x40 if (self._position.y > 0) else 0x00)
                    + self._position.x)
            else:
                self.command(
                    0x80
                    + (0x40 if (self._position.y & 0x01) else 0x00)
                    + (0x14 if (self._position.y & 0x02) else 0x00))

    def write_char(self, char):
        """Write a single char.
        """
        if self._goto_state == 0:
            pass
        elif self._goto_state == 1:
            self._position.x = 10 * ( ord( char ) - ord( '0' ) )
            self._goto_state += 1
            return
        elif self._goto_state == 2:
            self._position.x += ( ord( char ) - ord( '0' ) )
            self._goto_state += 1
            return
        elif self._goto_state == 3:
            self._position.y = 10 * ( ord( char ) - ord( '0' ) )
            self._goto_state += 1
            return

        elif self._goto_state == 4:
            self._position.y += ( ord( char ) - ord( '0' ) )
            self._goto_state = 0
            self.cursor(self._position)
            return

        if (char == '\n'):
            self.cursor(xy(0, self._position.y + 1))

        elif (char == '\r'):
            self.cursor(xy(0, self._position.y))

        elif (char == '\v'):
            self.cursor(xy(0, 0))

        elif (char == '\f'):
            self.clear()

        elif (char == '\t'):
            self._goto_state = 1

        elif (
                (self._position.x >= 0)
                and (self._position.x < self.size.x)
                and (self._position.y >= 0)
                and (self._position.y < self.size.y)
        ):

            # handle the gap for 1-line displays
            if (self.size.x == 1) and (self._position.x == 8):
                self.cursor(self._position)
            self.cursor(self._position)
            self.data(char)

            self._position.x += 1

    def write(self, text: str):
        """Write a string.
        """
        for c in text:
            self.write_char(c)
