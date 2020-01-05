"""
invert

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

class invert:
   """Invert a pin or port.
   
   This decorator inverts the value that is read from 
   or written to a pin or port.
   """

   def __init__( self, minion ):
      """Create an invert from its minion.
      """
      
      self._minion = minion
      
      # the minion *might* be a port and hence have an n
      try:
         self.n = self._minion.n
         self._is_port = True
         
      except:
         self._is_port = False
      
   def write( self, v ):
      """Write the inverse of v to the minion.
      
      Note: the minion must support write().
      """
      
      if self._is_port:
         
         # port: write bitwise inverse
         self._minion.write( ~ v )
         
      else:
      
         # single pin: write logic inverse      
         self._minion.write( not v )
 
   def read( self ):
      """Return the inverse of the value read from the minion.
      
      Note: the minion must support read().
      """

      if self._is_port:
         
         # port: return bitwise inverse
         return ~ self._minion.read()

      else:
      
         # single pin: return logic inverse
         return not self._minion.read()
      
   def make_input(self):
      """Make the minion an input.
      
      Note: The minion must suppoirt make_input().
      """

      self._minion.make_input()

   def make_output(self):
      """Make the minion an output.
      
      Note: The minion must support make_output().
      """

      self._minion.make_output()   