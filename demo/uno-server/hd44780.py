"""
Show text on an HD44780 16x2 LCD display
"""

import sys
sys.path.append( "../.." )
import hwpy

import time

d = hwpy.port([
   hwpy.gpo( hwpy.pins.d4 ), 
   hwpy.gpo( hwpy.pins.d5 ), 
   hwpy.gpo( hwpy.pins.d6 ), 
   hwpy.gpo( hwpy.pins.d7 )
])
rs = hwpy.gpo( hwpy.pins.d8 )
e  = hwpy.gpo( hwpy.pins.d9 )
bl = hwpy.gpo( hwpy.pins.d10 )
lcd = hwpy.hd44780( rs, e, d, hwpy.xy( 16, 2 ) )
bl.write( 1 )

print( __doc__ )
lcd.write( "\fHello world!" )
n = 0 
while True:
   n += 1
   lcd.write( "\t0001" + str( n ) )
   time.sleep( 1.0 )