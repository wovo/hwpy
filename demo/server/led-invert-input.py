"""
Copy inverse of pin d2 to the on-board LED.

For a switch connected to ground, the input must be inverted
to get an 'active True' input.
"""

import sys
sys.path.append( "../.." )
import hwpy

led = hwpy.gpo( 13 )
button = hwpy.invert( hwpy.gpi( 2 ))
while True:
   led.write( button.read() )