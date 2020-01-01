"""
Copy inverse of pin d2 to the on-board LED.

For a switch connected to ground, the input must be inverted
to get an 'active True' input.
"""

import sys
sys.path.append( "../.." )
import hwpy

led = hwpy.gpo( hwpy.pins.d13 )
button = hwpy.invert( hwpy.gpi( hwpy.pins.d2 ))

while True:
   led.write( button.read() )