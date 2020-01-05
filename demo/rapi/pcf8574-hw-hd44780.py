"""
Basic HD44780 character LCD interface using pcf8574 and hardware i2c
"""

import sys
sys.path.append( "../.." )
import hwpy
print( __doc__)


i2c = hwpy.i2c_hardware()
pcf = hwpy.pcf8574(i2c, 0x07)
lcd = hwpy.hd44780.from_pcf8574(pcf, hwpy.xy(16,2))

lcd.write( "\fHello world" )
n = 0
while True:
    n = ( n + 1 ) % 17
    lcd.write( "\t0001" + ( n * "=" ) + ( ( 16 - n ) * " " ))
    hwpy.wait_ms(200)

