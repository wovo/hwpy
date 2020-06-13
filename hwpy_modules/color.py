"""
color

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

class color:
    def __init__( self, red : int, green : int, blue : int ):
        self.red = red
        self.green = green
        self.blue = blue

black       = color( 0,       0,    0 )
white       = color( 0xFF, 0xFF, 0xFF )
red         = color( 0xFF,    0,    0 ) 
green       = color( 0,    0xFF,    0 )
blue        = color( 0,       0, 0xFF )
gray        = color( 0x80, 0x80, 0x80 )
yellow      = color( 0xFF, 0xFF,    0 )
cyan        = color(    0, 0xFF, 0xFF )
magenta     = color( 0xFF,    0, 0xFF )
  
violet      = color( 0xEE, 0x82, 0xEE )        
sienna      = color( 0xA0, 0x52, 0x2D )        
purple      = color( 0x80, 0x00, 0x80 )         
pink        = color( 0xFF, 0xC8, 0xCB )        
silver      = color( 0xC0, 0xC0, 0xC0 )        
brown       = color( 0xA5, 0x2A, 0x2A )        
salmon      = color( 0xFA, 0x80, 0x72 )


