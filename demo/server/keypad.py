"""
Read a matrix keypad input.
"""

import sys
sys.path.append( "../.." )
import hwpy

out_pins = hwpy.port([
   hwpy.gpoc( hwpy.a4 ), 
   hwpy.gpoc( hwpy.a5 ), 
   hwpy.gpoc( hwpy.a5 ), 
   hwpy.gpoc( hwpy.a7 )
])
in_pins = hwpy.port([
   hwpy.gpi( hwpy.a0 ), 
   hwpy.gpi( hwpy.a1 ), 
   hwpy.gpi( hwpy.a2 ), 
   hwpy.gpi( hwpy.a3 )
])
keypad = hwpy.keypad( out_pins, in_pins,  "D#0*C987B654A321" )

p = hwpy.gpi( hwpy.d2 )
while True:
   print( p.read() )

while True:
   print( "=======================", keypad.read() )