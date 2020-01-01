"""
Toggle the on=board LED pin as fast as possible.
(Which is ~ 1kHz at 115200 baud)
"""

import sys
sys.path.append( "../.." )
import hwpy

led = hwpy.gpo( hwpy.d13 )
while True:
   led.write( 0 )
   led.write( 1 )