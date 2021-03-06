"""
An alternate (left 4 on, right 4 on) LEDs
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)

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