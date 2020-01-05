"""
Blink the backlight on a HD44780 LCD-keypad shield 
"""

import sys
sys.path.append( "../.." )
import hwpy

bl = hwpy.gpo( hwpy.pins.d10 )
print( __doc__ )
hwpy.blink( bl )