"""
gpio

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

import os

if os.uname().machine == 'x86_64':
    from hwpy_modules.gpio_remote import *
else:
    from hwpy_modules.gpio_rapi import *

class gpi:
    """A gpi (input only) pin (with pull-up).
    """

    def __init__(self, pin: int, pullup: bool = True, pulldown: bool = False):
        """Create a gpi pin from its (BCM or Arduino) pin number.
        """

        self._pin = gpio(pin)
        self._pin.make_input(pullup, pulldown)

    def read(self) -> bool:
        """Read the value (False or True) of the pin.
        """

        return self._pin.read()


class gpo:
    """A gpo (output only) pin.
    """

    def __init__(self, pin: int):
        """Create a gpo pin from its (BCM or Arduino) pin number.
        """

        self._pin = gpio(pin)
        self._pin.make_output()

    def write(self, v: int):
        """Write v (0 or 1) to the gpio.
        """

        self._pin.write(v)


class gpoc:
   """A gpoc (open-collector input output) pin.
   """

   def __init__( self, pin ):
      """Create a gpoc pin from its (BCM or Arduino) pin number.
      """

      self._pin = gpio( pin )
      self._pin.make_input()

   def write( self, v ):
      """Write v (boolean value) to the gpio.
      """

      if v:
         self._pin.make_input()
      else:
         self._pin.make_output()
         self._pin.write( 0 )

   def read( self ):
      """Read the value (boolean value) of the gpio.
      """

      return self._pin.read()

