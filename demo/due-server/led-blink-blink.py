"""
Blink a LED that is connected to pin d13 (the on-board LED)
using hwpy.blink()
"""

import sys
sys.path.append( "../.." )
import hwpy

led = hwpy.gpo( hwpy.d13 )
print( __doc__ )
hwpy.blink( led )