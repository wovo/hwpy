# ===========================================================================
#
# part of hwpy: an OO hardware interface library
#
# home: https://www.github.com/wovo/hwpy
#
# ===========================================================================

# ===========================================================================
#
# Raspberry Pi gpio implementation
#
# ===========================================================================

class _rapi_gpio:
    """A Raspberry Pi gpio (input and output) pin.
    """

    def __init__(self, pin: int):
        """Create a gpio pin from its pin (BCM) number.
        """
        import RPi.GPIO as _gpio
        self.GPIO = _gpio
        self._init()
        self._pin = pin

        self.GPIO.setup(self._pin, self.GPIO.OUT)

    def _init(self):
        """Internal function that initializes RPi.GPIO.
        """
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)

    def make_input(self, pullup: bool = True, pulldown: bool = False):
        """Make the gpio an input, by default, the pullup is enabled
        """
        if pulldown:
            pull_mode = self.GPIO.PUD_DOWN
        elif pullup:
            pull_mode = self.GPIO.PUD_UP
        else:
            pull_mode = self.GPIO.PUD_OFF

        self.GPIO.setup(
            self._pin,
            self.GPIO.IN,
            pull_up_down=pull_mode)

    def make_output(self):
        """Make the gpio an output.
        """
        self.GPIO.setup(
            self._pin,
            self.GPIO.OUT)
       
    def write( self, v ):
        """Write v (evaluated as boolean) to the gpio.
      
        Note: the pin must be an output.
        """
        RPi.GPIO.output( self._pin, 1 if v else 0 )   
      
    def read( self ):
        """Read and retuirn the value (boolean) of the gpio. 
      
        Note: the pin must be an input.
        """
        return True if RPi.GPIO.input( self._pin ) else False        

gpio = _rapi_gpio