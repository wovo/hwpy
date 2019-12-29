"""
Blink a LED that is connected to pin d13 (the on-board LED).
"""

import sys
sys.path.append( "../.." )
import hwpy

led = hwpy.gpo( 13 )
hwpy.blink( led )