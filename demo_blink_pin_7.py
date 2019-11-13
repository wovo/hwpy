"""
Blink a LED that is connected to pin 16
"""
import hwpy

led = hwpy.gpo( 16 )
hwpy.blink( led )