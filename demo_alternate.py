"""
A kitt display on LEDs connected to the pins 17,
"""

import hwpy

leds = hwpy.all([ 
   hwpy.gpo( 17 ),
   hwpy.gpo( 27 ),
   hwpy.gpo( 22 ),
   hwpy.gpo( 10 ),
   hwpy.invert( hwpy.gpo(  9 )),
   hwpy.invert( hwpy.gpo( 11 )),
   hwpy.invert( hwpy.gpo(  0 )),
   hwpy.invert( hwpy.gpo(  5 )),
])   
hwpy.blink( leds )