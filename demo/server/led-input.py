"""
Copy pin d2 to the on-board LED.
"""

import sys
sys.path.append( "../.." )
import hwpy

led = hwpy.gpo( hwpy.d13 )
button = hwpy.gpi( hwpy.d2 )
while True:
   led.write( button.read() )