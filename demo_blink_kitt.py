"""
A kitt display on LEDs connected to the pins 17,
"""

import hwpy

leds = hwpy.port([ 
   hwlib.gpo( 17 ),
   hwlib.gpo( 27 ),
   hwlib.gpo( 22 ),
   hwlib.gpo( 10 ),
   hwlib.gpo(  9 ),
   hwlib.gpo( 11 ),
   hwlib.gpo(  0 ),
   hwlib.gpo(  5 ),
])   
hwpy.kitt( leds )