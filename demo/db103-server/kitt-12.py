"""
Kitt on 12 LEDs
"""

import sys
sys.path.append( "../.." )
import hwpy

import time

leds = hwpy.port( [
   hwpy.gpo( hwpy.db103.scl ),
   hwpy.gpo( hwpy.db103.sda ),
   hwpy.gpo( hwpy.db103.p06 ),
   hwpy.gpo( hwpy.db103.p07 ),
   
   hwpy.gpo( hwpy.db103.p10 ),
   hwpy.gpo( hwpy.db103.p11 ),
   hwpy.gpo( hwpy.db103.p12 ),
   hwpy.gpo( hwpy.db103.p13 ),
   
   hwpy.gpo( hwpy.db103.p14 ),
   hwpy.gpo( hwpy.db103.p15 ),
   hwpy.gpo( hwpy.db103.p18 ),
   hwpy.gpo( hwpy.db103.p19 )
])   

print( __doc__ )
hwpy.kitt( leds )