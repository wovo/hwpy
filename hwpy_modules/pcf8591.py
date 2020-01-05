# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

from hwpy_modules.i2c_interface import *

# ===========================================================================
#
# pcf8591
#
# ===========================================================================

class pcf8591:
    """Interface to pcf8591 i2c A/D converter

    The pcf8591 provides 4 A/D inputs 
    """

    def __init__(self, i2c: i2c_interface, address: int = 0x0 ):
        """A pcf8591 interface from an i2c port and the slave address.

        Note: the address is the 3-bit address set by the 3 address pins.
        """
        
        self._i2c = i2c
        self._address = 0x48 + address
        self._configuration = 0x40


    def read( self, channel: int) -> int:
      """Read and return the A/D value of the specified A/D channel.
      """
        
      # select the correct channel
      control = ( self._configuration & ( not 0x03 )) + channel
      self._i2c.write(self._address, [control])
      
      # read results, note that the first byte is the 
      # *previous* ADC result, the second byte is what we want
      results = self._i2c.read( self._address, 2 )
      return results[ 1 ]