"""
Read a matrix keypad input.
"""

import sys
sys.path.append( "../.." )
import hwpy

import time

in_pins = hwpy.port([
   hwpy.gpi( hwpy.pins.a0 ), 
   hwpy.gpi( hwpy.pins.a1 ), 
   hwpy.gpi( hwpy.pins.a2 ), 
   hwpy.gpi( hwpy.pins.a3 )
])
out_pins = hwpy.port([
   hwpy.gpoc( hwpy.pins.a4 ), 
   hwpy.gpoc( hwpy.pins.a5 ), 
   hwpy.gpoc( hwpy.pins.a6 ), 
   hwpy.gpoc( hwpy.pins.a7 )
])
keypad = hwpy.keypad( out_pins, in_pins,  "147*2580369#ABCD" )

print( "read keypad" )
n = 0
while True:
   k = keypad.read()
   n += 1
   print( n, k )