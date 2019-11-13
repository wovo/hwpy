"""
A kitt display on LEDs connected to the pins 1,2,3,4,5,6.
"""

import hwpy

leds = hwpy.port([ 
   hwlib.gpo( 1 ),
   hwlib.gpo( 2 ),
   hwlib.gpo( 3 ),
   hwlib.gpo( 4 ),
   hwlib.gpo( 5 ),
   hwlib.gpo( 6 )
])   
hwpy.kitt( leds )