# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

from hwpy_modules.gpio import *
from hwpy_modules.port import *
from hwpy_modules.invert import *


# ===========================================================================
#
# matrix keypad
#
# ===========================================================================

class keypad:
   """Interface for a matrix keypad.
   """

   def __init__( self, rows, columns, characters ):
      """Create a matrix keypad interface.
      
      Create a matrix keypad from the rows and columns ports,
      and the list of characters to be returned for pressed keys.
      The characters list is by row.
      The length of the list must be the number of rows multiplied
      by the number of columns.
      The rows must support write (msut be outputs or open-collector), 
      the columns must support read (muist be inputs or open-collector).
      """
      self._rows = invert( rows )
      self._columns = invert( columns )
      self._characters = characters
      self._last = None
      
      # in case the rows are open collector, they must be made high
      try:
         self._rows.write( ~ 0 )
      except:
         pass      
      
      if ( self._rows.n * self._columns.n ) != len( self._characters ):
         raise Exception( "keypad error %d rows %d columns %d characters" %
            ( self._rows.n, self._columns.n, len( self._characters )))
   
   def is_pressed( self, key ):
      """Test whether a key is pressed.
      
      Return true if and only if the specified key is pressed.
      """

      i = self._characters.find( key )      
      if 0:
         w = 1 << ( i // self._columns.n )
         self._rows.write( w )
         r = self._columns.read() 
      
         m = ( 1 << i % self._rows.n )
         x = ( self._columns.read() & ( 1 << i % self._rows.n )) != 0
         print( key, i, w, r, m, x )
         return x
      
      self._rows.write( 1 << ( i // self._columns.n ))
      return ( self._columns.read() & ( 1 << ( i % self._rows.n ))) != 0
      
   def read_pressed_nonblocking( self, default ):
      """Return a pressed key (non-blocking).
      
      Scan the keys until one is found that is pressed.
      When found, return the pressed key.
      When none is found, return the default.
      """
      for c in self._characters:
         if self.is_pressed( c ):
            return c
      return default            
   
   def read_pressed_blocking( self, t = 0.050 ):
      """Return a pressed key (blocking).
      
      Scan the keyboard until a key is found pressed.
      Return that key.
      
      Wait t seconds between keypad scans 
      to prevent lock-up of the system.      
      """
      while True:
         key = self.read_pressed_nonblocking( None )
         if key != None:
            return key
         time.sleep(t)
         
   def read( self, t = 0.050 ):
      """Read a newly pressed key.
      
      Scan the keyboard until a key is found pressed
      that wasn't pressed the last time.
      Return that key.
      
      Wait t seconds between keypad scans 
      to prevent lock-up of the system.
      """
      while True:
         key = self.read_pressed_nonblocking( None )
         if key != self._last:
            self._last = key
            if key != None:
               return key
         time.sleep(t)