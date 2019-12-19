"""
Copy pin d2 to the on-board LED.
"""

import sys
sys.path.append( "../.." )
import hwpy

led = hwpy.gpo( 13 )
button = hwpy.gpi( 2 )
while True:
   led.write( button.read() )