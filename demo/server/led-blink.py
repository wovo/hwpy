"""
Blink a LED that is connected to pin d13 (the on-board LED).
"""

import sys
sys.path.append( "../.." )
import hwpy

import time

led = hwpy.gpo( hwpy.pins.d13 )
print( "blink LED in while loop" )
while True:
   led.write( 0 )
   time.sleep( 0.2 )
   led.write( 1 )
   time.sleep( 0.2 )