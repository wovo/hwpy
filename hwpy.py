# ===========================================================================
#
# hwpy: an OO hardware interface library for the Raspberry Pi
#
# home: https://www.github.com/wovo/hwpy
#
# author: Wouter van Ooijen (wouter.vanooijen@hu.nl)
#
# uses http://domoticx.com/python-library-rpi-gpio/
# (which is pre-installed on the common RaPi Linux distributions)
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
# delays
#
# ===========================================================================
      
def wait_s( n ):
   time.sleep( n )

def wait_ms( n ):
   wait_s( n / 1000.0 )

def wait_us( n ):
   wait_ms( n / 1000.0 )


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
      
      RPi.GPIO.setup( 
         self.pin, 
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
      
   def read( self ):
      """
      Read the value (0 or 1) of the gpio. 
      It must be an input."""
      
      return RPi.GPIO.input( self.pin )  
      
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
   Decorator that inverts the value that is read or written
   to or from a pin or port."""

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
      Return the inverse of the value read from the minion.
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
      The minion must support make_output()."""
      
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
# matrix keypad
#
# ===========================================================================

class keypad:
   """
   Interface for a matrix keypad."""

   def __init__( self, rows, columns, characters ):
      """
      Create a matrix keypad from the rows and columns ports,
      and the list of characters to be returned for pressed keys.
      The characters list is by row.
      The length of the list must be the number of rows multiplied
      by the number of columns.
      The rows must be inputs or open-collector, 
      the columns must be outputs or open-collector."""
      
      self.rows = rows
      self.columns = columns
      self.characters = characters
      
      # in case the rows are open collector, they must be high
      try:
         self.rows.write( ~ 0 )
      except:
         pass      
      
      if ( self.rows.n * self.columns.n ) != len( characters ):
         raise( "keypad error %n rows %n columns %n characters" %
            ( self.rows.n, self.columns.m, len( self.characters )))
   
   def is_pressed( self, key ):
      """
      Return true if and only if the specified key is pressed."""
      
      i = self.characters.find( key )
      self.columns.write( ~ ( 1 << ( i / self.rows.n )))
      return ( self.rows.read() & ( 1 << i % self.rows.n )) == 0
      
   def read_nonblocking( self, default ):
      """
      Scan the keys until one is found that is pressed.
      When found, return the pressed key.
      When none is found, return the default."""
      
      for c in self.characters:
         if self.is_pressed( c ):
            return c
      return default            
   
   def read( self ):
      """
      Scan the keyboard until a key is found pressed.
      Return that key."""
   
      while True:
         key = self.read_nonblocking( None )
         if key != None:
            return Key
      
      
# ===========================================================================
#
# simple pin and port demos
#
# ===========================================================================
      
def blink( pin, t = 0.5 ):
   """
   Blink a LED on the pin.
   t is the period. 
   The pin must be an output."""
   
   while True:
      pin.write( 0 )
      time.sleep( 1.0 * t / 2 )
      pin.write( 1 )
      time.sleep( 1.0 * t / 2 )
      
def kitt( port, t = 0.5 ):
   """
   Kitt display on the pins in the port. 
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
# bit-banged i2c
#
# ===========================================================================
      
class i2c_from_scl_sda:
   """
   A bit-banged (slow, but pin-agnostic) i2c interface."""

   def __init__( self, scl, sda ):
      """
      Create a bit-banged i2c from the scl and sda pins"""
      
      self.scl = scl
      self.sda = sda
      self.scl.write( 1 )
      self.sda.write( 1 )
      
   def wait( self ):
      """
      Internal function that waits half a bit-cell.
      Currently this does nothing, 
      because bit-banged i2c is already slow."""
      
      pass   

   def _write_one_bit( self, v ):
      self.scl.write( 0 )
      self.wait()
      self.sda.write( v )
      self.scl.write( 1 )
      
      while not self.scl.read():
         self.wait()      
   
   def _read_one_bit( self ):
      self.scl.write( 0 )
      self.sda.write( 1 )
      self.wait()
      self.scl.write( 1 )
      
      while not self.scl.read():
         self.wait()
         
      b = self.sda.read()
      self.wait()
      return b      
   
   def _write_ack( self ):
      self._write_one_bit( 0 )
   
   def _write_nack( self ):
      self._write_one_bit( 1 )
      
   def _write_start( self ):
      self.sda.write( 0 )
      self.wait()
      self.scl.write( 0 )      
      self.wait()
      
   def _write_stop( self ):
      self.scl.write( 0 )
      self.wait()
      self.sda.write( 0 )
      self.wait()
      self.scl.write( 1 )      
      self.wait()
      self.sda.write( 1 )
      self.wait()
      
   def _read_ack( self ):
      return not self._read_one_bit()   

   def _read_one_byte( self ):
      result = 0
      mask = 0x80
      for i in range( 0, 8 ):
         if self._read_one_bit():
            result = result | mask
         mask = mask >> 1
      return result         
 
   def _write_one_byte( self, byte ):
      mask = 0x80
      for i in range( 0, 8 ):
         self._write_one_bit( byte & mask )
         mask = mask >> 1
   
   def write( self, address, bytes ):
      """
      Perform an i2c write transaction:
      write the bytes to the chip with
      the (7-bit) address."""
      
      self._write_start()
      self._write_one_byte( ( address << 1 ) + 0x01 )   
      self._read_ack()
      
      self._write_start()
      self._write_one_byte( address << 1 )
      for b in bytes:
         self._write_one_byte( b )
   
   def read( self, address, n ):
      """
      Perform an i2c read transaction:
      read and return n bytes from the chip with
      the (7-bit) address."""

      self._write_start()
      self._write_one_byte( address << 1 )   
      self._read_ack()
      
      result = []
      first = 1
      for i in range( 0, n ):
         if first:
            self._write_ack()
         first = 0            
         result.append( self._read_one_byte() )
         
      self._write_nack()
      self._write_stop()      
      return result         
         
         
# ===========================================================================
#
# pcf8574(a)
#
# ===========================================================================

class _buffered_pin:

   def __init__( self, master, mask ):
      self.master = master
      self.mask = mask
      
   def write( self, v ):
      if v:
         self.master.write_buffer |= self.mask
      else:
         self.master.write_buffer &= ~ self.mask
      self.master.flush()

   def read( self ):
      self.master.refresh();
      return ( self.master.read_buffer & mask ) != 0      
      
class _pcf8574x:
   def __init__( self, i2c, address ):
      self.i2c = i2c
      self.address = address
      self.pins = []
      self.read_buffer = 0
      self.write_buffer = 0
      for i in range( 0, 8 ):
         self.pins.append( _buffered_pin( self, 1 << i ))
      
   def flush( self ):
      self.i2c.write( self.address, self.write_buffer )   
   
   def refresh( self ):   
      self.read_buffer = self.i2c.read( self.address )    
      
   def write( self, value ):
      self.write_buffer = value
      self.flush()
      
   def read( self ):
      self.refresh()
      return self.read_buffer
   
def pcf8574( i2c, address = 0 ):
   return _pcf8574x( i2c, 0x20 + address ) 
         
def pcf8574a( i2c, address = 0 ):
   return _pcf8574x( i2c, 0x28 + address ) 
         
         
# ===========================================================================
#
# hd44780
#
# ===========================================================================

class hd44780:
   """
   4-bit interface to an HD44780 (character) LCD.
   
   Some characters are treated special:
     - '\\n' puts the cursor at the first position of the next line
     - '\\r' puts the cursor at the start of the current line
     - '\\f' puts the cursor at the top-left position and clears the lcd
     - '\\txxyy' puts the cursor at the position (xx,yy)
   """

   def __init__( self, pin_rs, pin_e, port_data, size ):
      """
      Construct an interface to an LCD controlled by an hd44780 chip
      from the RS and E pins, the 4-bit port to the D4..D8 pins, 
      and the size (number of characters per line, and number of lines),
      and initializes the controller."""
      
      self.rs = pin_rs
      self.e = pin_e
      self.data = port_data
      self.size = size
      
      pin_e.write( 0 )
      pin_rs.write( 0 )
      wait_ms( 100  )

      # interface initialization: make sure the LCD is in 4 bit mode
      # (magical sequence, taken from the HD44780 data-sheet)
      self._write4( 0x03 )
      wait_ms( 15 )
      self._write4( 0x03 )
      wait_us( 100 )
      self._write4( 0x03 )
      self._write4( 0x02 )     # 4 bit mode

      # functional initialization
      self.command( 0x28 )             # 4 bit mode, 2 lines, 5x8 font
      self.command( 0x0C )             # display on, no cursor, no blink
      self.clear()                     # clear display, 'cursor' home  
      self.goto_state = 0
      
   def _write4( self, nibble ):
      wait_us( 10 )
      self.data.write( nibble )
      wait_us( 20 )
      self.e.write( 1 )
      wait_us( 20 )
      self.e.write( 0 )
      wait_us( 100 )

   def _write8( self, is_data, byte ):
      self.rs.write( is_data )
      self.write4( byte >> 4 )
      self.write4( byte )
   
   def command( self, cmd ):
      """
      Write a command byte to the LCD

      Use this function only for features that are not 
      provided by the console interface, like the definition
      of the user-defined characters."""
      
      self._write8( 0, cmd )

   def data( self, chr ):
      """
      Write a data byte to the LCD
    
      Use this function only for features that are not 
      provided by the console interface, like the definition
      of the user-defined characters."""
      
      self._write8( 1, chr )

   def clear( self ):
      """  
      Clear the display and put the cursor at (0,0)."""
      
      self.command( 0x01 )
      wait_ms( 5 )
      self.cursor_set( xy( 0, 0 ) )
      
   def cursor( self, position ):
      self.postion = position
      
      if( self.size.y == 1 ):
         if( self.position.x < 8 ):
            self.command( 0x80 + self.position.x )
         else:
            self.command( 0x80 + 0x40 + ( self.position.x - 8 ))
      else:
         if( self.size.y == 2 ):
            self.command( 
               0x80
               + ( 0x40 if ( self.position.y > 0 ) else 0x00 )
               + ( self.position.x ))
         else:
            self.command( 
                0x80
                + ( 0x40 if ( self.position.y & 0x01 ) else 0x00 )
                + ( 0x14 if ( self.position.y & 0x02 ) else 0x00 ))

   def write_char( self, char ):

      if self.goto_state == 0:
         pass
         
      elif self.goto_state == 1:

         self.position.x = 10 * ( char - '0' )
         self.goto_state += 1;
         return

      elif self.goto_state == 2:
         self.position.x += ( char - '0' )
         self.goto_state += 1;
         return

      elif self.goto_state == 3:
         self.position.y = 10 * ( char - '0' )
         self.goto_state += 1;
         return

      elif self.goto_state == 4:
         self.position.y += ( c - '0' )
         self.goto_state = 0;
         self.cursor( self.position );
         return

      if( char == '\n' ):
         self.cursor( xy( 0, self.position.y + 1 ) )

      elif( char == '\r' ):
         self.cursor( xy( 0, self.position.y ) );

      elif( c == '\v' ):
         self.cursor( xy( 0, 0 ) )

      elif( c == '\f' ):
         self.clear()

      elif( c == '\t' ):
         self.goto_state = 1

      elif(
         ( self.position.x >= 0 )
         and ( self.position.x < size.x )
         and ( self.position.y >= 0 )
         and ( self.position.y < size.y )
      ):
      
         # handle the gap for 1-line displays
         if( ( size.x == 1 ) and ( self.position.x == 8 ) ):
            self.cursor( self.position )
      
         self.data( char )      
         self.position.x += 1
      
   def write( self, text ):
      for c in text:
         self.write_char( c )
      
      
# ===========================================================================
#
# todo
#
# ===========================================================================
      
# pcf demos
# pcf keypad      
# serial backpack HD44780
# SPI
# MPU6050?
# card reader
# HC595?
# servo
         
      