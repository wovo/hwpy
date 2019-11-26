"""
Demo for the sr04 ultra-sonic distance sensor
"""

import time, hwpy
sr04 = hwpy.sr04( hwpy.gpo( 19 ), hwpy.gpi( 26 ) )

while True:
   print( "%d cm" % sr04.read() )
   time.sleep( 1 )