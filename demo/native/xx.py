from time import sleep
 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
'''
# Import Luma.OLED libraries
from luma.core.interface.serial import spi
from luma.oled.device import ssd1331
# Configure the serial port
serial = spi(device=0, port=0)
device = ssd1331(serial)
'''
frameSize = (96, 64)
 
def main():
    image = Image.new('RGB', (frameSize), 'white')
    #font = ImageFont.truetype("FreeMonoBold.ttf", 12, encoding="unic")
    draw = ImageDraw.Draw(image)
    
    draw.rectangle([(1,1), (frameSize[0]-2,frameSize[1]-2)], 'yellow', 'blue')
    draw.text((5, 5), 'Hello World', fill='green')
    '''
    # Output to OLED/LCD display
    device.display(image)
    '''
    # Output to PC image viewer
    image.show()
    
    sleep(5)
    
if __name__ == "__main__":
    main()