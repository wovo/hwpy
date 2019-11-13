# ===========================================================================
#
# hwpy: an OO hardware interface library for the RaPi
#
# home: https://www.github.com/wovo/hwpy
#
# uses http://domoticx.com/python-library-rpi-gpio/
#
# ===========================================================================

import RPi, RPi.GPIO, time

def init():  
   """
   Internal function that initializes RPi.GPIO.
   This function is called automatically when needed.""" 
   
   RPi.GPIO.setmode( RPi.GPIO.BCM )
   RPi.GPIO.setwarnings( False )
   
   
# ===========================================================================
#
# xy class
#
# ===========================================================================
      
class xy:
   """
   A container for an (x,y) value pair"""
   
   def __init( self, x, y ):
      """
      Create an xy object from x and y values"""
      
      self.x = copy( x )
      self.y = copy( y )      
      
      
# ===========================================================================
#
# gpio, gpi, gpo, gpoc
#
# ===========================================================================
      
class gpio:
   """
   A gpio (input and output) pin"""

   def __init__( self, pin ):
      """
      Create a gpio pin from its pin (BCM) number"""
      
      init()
      self.pin = pin      
      RPi.GPIO.setup( self.pin, RPi.GPIO.OUT )
      
   def make_input( self ):
      """
      Make the gpio an input, with pull-up"""
      
      RPi.RPIO.setup( 
         pin, 
         RPi.GPIO.IN, 
         pull_up_down = RPi.GPIO.PUD_UP )   
      
   def make_output( self ):
      """
      Make the gpio an output"""
      
      RPi.GPIO.setup( 
         self.pin, 
         RPi.GPIO.OUT ) 
      
   def write( self, v ):
      """
      Write v (0 or 1) to the gpio. 
      It must be an output."""
      
      RPi.GPIO.output( self.pin, v & 0x01 )   
      
   def read( self, v ):
      """
      Read the value (0 or 1) of the gpio. 
      It must be an input."""
      
      return RPi.GPIO.output( self.pin, v )  
      
class gpi:
   """
   A gpi (input only)  pin (with pull-up)"""
   
   def __init__( self, pin ):  
      """
      Create a gpi pin from its (BCM) pin number"""
      
      self.pin = gpio( pin )
      self.pin.make_input()
      
   def read( self ):
      """
      Read the value (0 or 1) of the gpio. """
      
      return self.pin.read()
      
class gpo:
   """
   A gpo (output only) pin"""
   
   def __init__( self, pin ):  
      """
      Create a gpo pin from its (BCM) pin number"""
      
      self.pin = gpio( pin )
      self.pin.make_output()
      
   def write( self, v ):
      """
      Write v (0 or 1) to the gpio."""

      self.pin.write( v ) 
      
class gpoc:
   """
   A gpoc (open-collector input output) pin"""

   def __init__( self, pin ):  
      """
      Create a gpoc pin from its (BCM) pin number."""   
   
      self.pin = gpio( pin )
      self.pin.make_input()
      
   def write( self, v ):
      """
      Write v (0 or 1) to the gpio."""

      if v:
         self.pin.make_input()      
      else:   
         self.pin.make_output()
         self.pin.write( 0 )    

   def read( self ):
      """
      Read the value (0 or 1) of the gpio."""

      return self.pin.read()


# ===========================================================================
#
# port
#
# ===========================================================================
      
class port:
   """
   A port is a set of pins.
   port.n is the number of pins.
   port.pins are the pins."""
   
   def __init__( self, pins ):
      "Create a port from a list of pins."
      self.pins = pins
      self.n = len( self.pins )

   def read( self ):
      """
      Read from a port.
      The result is an integer, 
         with in bit 0 the value read from the first pin,
         in bit 1 the value read from the 2nd pin, etc.
      The pins must support read()."""      
      
      result = 0
      mask = 1
      for pin in pins:
         mask = mask << 1
         if pin.read():
            result = result + mask
      return result      
      
   def write( self, v ):
      """
      Write to port.
      v must be an integer. 
      The lowest bit in v is written to the first pin,
         the lowets-but-one is written to the second pin, etc.
      The pins must support write()."""      
      
      mask = 1
      for pin in self.pins:
         pin.write( v & mask )
         mask = mask << 1
         
   def make_input( self ):
      """
      Make all pins inpits. The pins must be gpio."""
      for pin in self.pins:
         pin.make_input()

   def make_output( self ):
      """
      Make all pins outputs. The pins must be gpio."""
      for pin in self.pins:
         pin.make_output()
         
         
# ===========================================================================
#
# invert
#
# ===========================================================================

class invert:
   """
   Decorator that inverts the value that is reasd or written."""

   def __init__( self, minion ):
      """
      Create an invert from its minion."""
      
      self.minion = minion
      
   def write( self, v ):
      """
      Write the inverse of v to the minion.
      The minion must support write()."""
      
      self.minion.write( ~ v )
 
   def read( self ):
      """
      Return the invrese of the value read from the minion.
      The minion must support read()."""
      
      return ~ self.minion.read()
      
   def make_input():
      """
      Make the minion an input.
      The minion must suppoiert make_input()."""
      
      self.minion.make_input()

   def make_output():
      """
      Make the minion output.
      The minion must suppoiert make_output()."""
      
      self.minion.make_output()   
     
     
# ===========================================================================
#
# all
#
# ===========================================================================

class all:
   """
   Decorator that writes to all its minions."""

   def __init__( self, minions ):
      """
      Create an all from its list of miniions."""
      
      self.minions = minions
      
   def write( self, v ):
      """
      Write v to all minions."""
      
      for m in self.minions:
         m.write( v ) 
      
      
# ===========================================================================
#
# matix keypad
#
# ===========================================================================

class keypad:
   """
   Interface for a matrix keypad."""

   def __init__( self, rows, columns, characters ):
      """
      Create a matrix keypad from the rows and columns ports,
      and the list of characters to be returned.
      The rows must be inpuits, the columns must be outputs."""
   
   def is_pressed( self, key ):
      pass
   
   def pressed( self ):
      pass      
      
   def read_nonblocking( self ):
      pass   
   
   def read( self ):
      pass
      
      
# ===========================================================================
#
# simple pin and port demos
#
# ===========================================================================
      
def blink( pin, t = 0.5 ):
   """
   Blink a LED on the pin.
   t is the period. 
   The pin must be output."""
   
   while True:
      pin.write( 0 )
      time.sleep( 1.0 * t / 2 )
      pin.write( 1 )
      time.sleep( 1.0 * t / 2 )
      
def kitt( port, t = 0.5 ):
   """
   Kitt display on the pins in port. 
   t is the sweep time. 
   The pins must be outputs."""
   
   while True:
      for p in range( 0, port.n ):
         port.write( 1 << p )
         time.sleep( 1.0 * t / port.n )
      for p in range( port.n - 1, 1, -1 ):
         port.write( 1 << p )
         time.sleep( 1.0 * t / port.n )      
        
        
# ===========================================================================
#
# i2c
#
# ===========================================================================
      
class i2c_from_scl_sda:
   """
   A bit-banged (slow, but pin-agnostic) i2c interface"""

   def __init__( self, scl, sda ):
      """
      Create an i2c from the scl and sda pins"""
      
      self.scl = scl
      self.sda = sda
      self.scl.write( 1 )
      self.sda.write( 1 )
      
   def wait( self ):
      """
      Internal function: wait half a bit-cell.
      Currently does nothing."""
      
      pass   

   def write_one_bit( self, v ):
      self.scl.write( 0 )
      self.wait()
      sda.write( v )
      scl.write( 1 )
      
      while not self.scl.read():
         self.wait()      
   
   def read_one_bit( self ):
      self.scl.write( 0 )
      self.sda.write( 1 )
      self.wait()
      self.scl.write( 1 )
      
      while not self.scl.read():
         self.wait()
         
      b = self.sda.read()
      wait()
      return b      
   
   def write_ack( self ):
      self.write_one_bit( 0 )
   
   def write_nack( self ):
      self.write_one_bit( 1 )
      
   def write_start( self ):
      self.sda.write( 0 )
      self.wait()
      self.scl.write( 0 )      
      self.wait()
      
   def write_stop( self ):
      self.scl.write( 0 )
      self.wait()
      self.sda.write( 0 )
      self.wait()
      self.scl.write( 1 )      
      self.wait()
      self.sda.write( 1 )
      self.wait()
      
   def read_ack( self ):
      return not self.read_one_bit()   

   def read_one_byte( self ):
      result = 0
      mask = 0x80
      for i in range( 0, 8 ):
         if rad_one_bit():
            result = result | mask
         mask = mask >> 1
      return result         
 
   def write_one_byte( self, byte ):
      mask = 0x80
      for i in range( 0, 8 ):
         self.write_one_byte( byte & mask )
         mask = mask >> 1
   
   def write( self, address, bytes ):
      self.write_start()
      self.write( ( address << 1 ) + 0x01 )   
      self.read_ack()
      
      self.write_start()
      self.write( address << 1 )
      for b in bytes:
         self.writeOne_byte( b )
   
   def read( self, address, n ):
      self.write_start()
      self.write( address << 1 )   
      self.read_ack()
      
      result = []
      first = 1
      for i in range( 0, n ):
         if first:
            self.write_ack()
         first = 0            
         result.append( self.read_one_byte() )
         
      self.write_nack()
      self.write_stop()      
      return result         
         
         
# ===========================================================================
#
# pcf857a(a)
#
# ===========================================================================

class buffered_pin:
   def __init__( self, master, mask ):
      self.master = master
      self.mask = mask
      
   def write( self, v ):
      if v:
         self.master.write_buffer |= mask
      else:
         self.master.write_buffer &= ~ mask
      self.master.flush()

   def read( self ):
      self.master.refresh();
      return ( self.master.read_buffer & mask ) != 0      
      
class pcf8574x:
   def __init__( self, i2c ):
      self.i2c = i2c
      self.address = address
      self.pins = []
      for i in range( 0, 8 ):
         self.pins.append( bufefered_pin( self, 1 << i ))
      
   def flush( self ):
      i2c.write( self.address, self.write_buffer )   
   
   def refresh( self ):   
      self.read_buffer = i2c.read( self.address )    
      
   def write( self, value ):
      self.write_buffer = value
      self.flush()
      
   def read( self ):
      self.refresh()
      return self.read_buffer
   
def pcf8574( i2c, address = 0 ):
   return pcf8574( i2c, 0x20 + address ) 
         
def pcf8574a( i2c, address = 0 ):
   return pcf8574( i2c, 0x28 + address ) 
         
         
# ===========================================================================
#
# todo
#
# ===========================================================================
      
# hd44780
# I2C
# SPI
# MPU6050?
# card reader
# PCF8574(A)
# HC595
# matrix keypad
         
      