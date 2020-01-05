"""
Read and print the 4 pins a0..a3
"""

import sys
sys.path.append( "../.." )
import hwpy

import time

port = hwpy.port([
   hwpy.gpi( hwpy.pins.a0 ), 
   hwpy.gpi( hwpy.pins.a1 ), 
   hwpy.gpi( hwpy.pins.a2 ), 
   hwpy.gpi( hwpy.pins.a3 )
])

def bits( v, n ):
   r = ""
   for i in range( 0, n ):
      r = ( "0" if v % 2 == 0 else "1" ) + r
      v = v // 2
   return r   

print( __doc__ )
while True:
   print( bits( port.read(), port.n ))
   time.sleep( 0.5 )