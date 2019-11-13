"""
Blink a LED that is connected to pin 7
"""
import hwpy

led = hwpy.gpo( 7 )
hwpy.blink( led )