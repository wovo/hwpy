import hwpy, time
sda = hwpy.gpoc( 2 ) 
scl = hwpy.gpoc( 3 )
i2c = hwpy.i2c_from_scl_sda( scl, sda )
chip = hwpy.pcf8574( i2c )

while True:

   chip.write( 0xF0 )
   time.sleep( 0.100 )
   