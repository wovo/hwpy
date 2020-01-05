"""
Blink a LED that is connected to pin p06 in a while loop
"""

import sys
sys.path.append( "../.." )
import hwpy

import time

led = hwpy.gpo( hwpy.db103.p06 )
print( "blink LED in while loop" )
while True:
   led.write( 0 )
   time.sleep( 0.2 )
   led.write( 1 )
   time.sleep( 0.2 )