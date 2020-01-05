"""
Blink a LED that is connected to pin 17.
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)

led = hwpy.gpo( 17 )
hwpy.blink( led )