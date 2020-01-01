# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

# ===========================================================================
#
# port
#
# ===========================================================================

class port:
   """A port is a set of pins.
   
   port.n is the number of pins.
   port.pins are the pins themselves.
   """
   
   def __init__( self, pins ):
      """Create a port from a list of pins.
      """
      self.pins = pins[ : ]
      self.n = len( self.pins )

   def read( self ):
      """Read from a port.
      
      The result is an integer, 
         with in bit 0 the value read from the first pin,
         in bit 1 the value read from the 2nd pin, etc.
      The pins must support read().
      """      
      result = 0
      mask = 1
      for pin in self.pins:
         if pin.read():
            result = result + mask
         mask = mask << 1
      return result      
      
   def write( self, v ):
      """Write to port.
      
      v must be an integer. 
      The lowest bit in v is written to the first pin,
         the lowest-but-one is written to the second pin, etc.
      The pins must support write().
      """      
      mask = 1
      for pin in self.pins:
         pin.write( ( v & mask ) != 0 )
         mask = mask << 1
         
   def make_input( self ):
      """Make all pins inputs. 
      
      Note: the pins must be gpio.
      """
      for pin in self.pins:
         pin.make_input()

   def make_output( self ):
      """Make all pins outputs. 
      
      Note: The pins must be gpio.
      """
      for pin in self.pins:
         pin.make_output()