"""
A kitt display on LEDs connected to the pins 17,
"""

import hwpy

leds = hwpy.port([ 
   hwpy.gpo( 17 ),
   hwpy.gpo( 27 ),
   hwpy.gpo( 22 ),
   hwpy.gpo( 10 ),
   hwpy.gpo(  9 ),
   hwpy.gpo( 11 ),
   hwpy.gpo(  0 ),
   hwpy.gpo(  5 ),
])   
hwpy.kitt( leds )