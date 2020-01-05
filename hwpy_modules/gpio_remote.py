"""
Remote (host-server) implementation of a gpio pin

part of hwpy: an OO hardware interface library

home: https://www.github.com/wovo/hwpy
"""

import time, enum

class pins( enum.Enum ):
   pass

class arduino( pins ):
   """Arduino pin designations
   """
   d2  =  2
   d3  =  3
   d4  =  4 
   d5  =  5
   d6  =  6
   d7  =  7
   d8  =  8
   d9  =  9
   d10 = 10
   d11 = 11
   d12 = 12
   d13 = 13
   d14 = 14
   d15 = 15
   d16 = 16
   d17 = 17
   d18 = 18
   d19 = 19
   d20 = 20
   d21 = 21
   d22 = 22
   d23 = 23
   d24 = 24
   d25 = 25

   a0 = 26
   a1 = 27
   a2 = 28
   a3 = 29
   a4 = 30
   a5 = 31
   a6 = 32
   a7 = 33
   
class db103( pins ):   
   scl = 2
   sda = 3
   p06 = 4
   p07 = 5
   p10 = 6
   p11 = 7
   p12 = 8
   p13 = 9
   p14 = 10
   p15 = 11
   p18 = 12
   p19 = 13
   
class _commands( enum.Enum ):   
   input   = 0
   output  = 1
   high    = 2
   low     = 3
   read    = 4

_serial_port = None
_serial_port_name = "COM3"
_serial_port_baudrate = 115200

_serial_port_name = "COM4"
_serial_port_baudrate = 115200

class _server_gpio:
    """A remote GPIO pin on a server.

    This is a GPIO pin that is provided by a GPIO server.
    It is used via serial connection.

    To use this class, you must install PySerial:
       python -m pip install pyserial
    """        
    
    _debug_log = False
    
    def __init__( self, nr : pins ):
      # d0 and d1 are claimed for the communication
      self.pin = nr.value - 2 
      
      global _serial_port
      if _serial_port == None:
         try:
             import serial
         except ImportError:
             serial = None
             print(
                "To use Host GPIO, you need the pyserial module," 
                "install it with \"python -m pip install pyserial\"." )
             print("Exiting...")
             exit()
         try:    
            _serial_port = serial.Serial( 
               _serial_port_name, 
               _serial_port_baudrate,
               timeout = 0,
               parity=serial.PARITY_NONE           
                              
            ) 
         except serial.serialutil.SerialException:
             print(
                "The serial port %s could not be opened. "
                "You can use the device manager to change the name of "
                "the port the Arduino server is connected to. " 
                "An Arduino Due must be disconnected and re-connected "
                "to effectuate a name change." % _serial_port_name )
             print("Exiting...")
             exit()        
             
         # reset-and-run sequence for a DB100/DB103 server    
         _serial_port.setRTS( 0 ) # run mode
         _serial_port.setDTR( 0 ) # reset
         time.sleep( 0.1 )
         _serial_port.setDTR( 0 ) # release reset
         
         
         # openening the port can cause the server to be reset, so
         # wait for the server to come to life
         time.sleep( 2.0 )
         
         # read and discard any junk that might be in the input
         self._empty_serial_input()
  
    def _empty_serial_input( self ):
      while True:
         d = _serial_port.read()
         if d == b'':
            return
         if self._debug_log: 
            print( "emptying ", d )
         time.sleep( 0.001 )
         
    def _read_byte( self ):
      for i in range( 0, 10 ):
         d = _serial_port.read()       
         if d != b'':
            if self._debug_log: 
               print( "response ", d )
            return d       
         time.sleep( 0.001 )
      return None   
         
    def _write_byte( self, b ):
       _serial_port.flush()
       if self._debug_log:
          print( 
             "command cmd=%d pin=%d byte=%d c=%c" 
             % ( b >> 5, b & 0x1F, b, chr( b )) )   
       _serial_port.write( chr( b ).encode( 'utf-8' ) )
      
    def _command(self, cmd, pin):
        self._empty_serial_input()    
        d = (cmd.value << 5) + pin
        if cmd != _commands.read:         
           self._write_byte(d)         
        else:
           while True:
              self._write_byte(d)
              x = self._read_byte()
              if x != None:
                 return x
            
    def make_input( self, pullup = True, pulldown = False ):
      """Make the gpio an input, default with (only) pull-up
      """
      self._command( 
         _commands.input, 
         self.pin 
      )
      
    def make_output( self ):
      """Make the gpio an output
      """
      self._command( 
        _commands.output, 
        self.pin
      )

    def write( self, v ):
      """Write v (evaluated as boolean) to the gpio. 
      
      Note: the gpio must be an output.
      """
      self._command( 
         _commands.high if v else _commands.low, 
         self.pin 
      )

    def read(self) -> bool:
        """Read the value (False or True) of the gpio.

        Note: the gpio must be an input.
        """
        c = self._command(
            _commands.read,
            self.pin
        )
        if not c in [ b'0', b'1' ]:
           print( "Invalid read response from server [%d]" % int( c ) )
        return False if c == b'0' else True

gpio = _server_gpio