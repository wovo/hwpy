"""
A kitt display on 8 LEDs connected to indicated pins.
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)

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