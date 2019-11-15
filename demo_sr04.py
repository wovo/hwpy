"""
Demo for the sr04 ultra-sonic distance sensor
"""

import hwpy
sr04 = hwpy.sr04( hwpy.gpo( 2 ), hwpy.gpi( 3 ) )

for True:
   print( "%d cm" % sr04.read() )
   time.speed( 1 )