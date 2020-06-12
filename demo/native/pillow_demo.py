"""
"""

from time import sleep

import PIL 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk
#from PIL import ImageFont

import tkinter
#from tkinter import *
# import Image, 
#import ImageTk


class lcd:
   def __init__( self, size ):
      self.size = size
      self.image = Image.new('RGB', self.size, 'white')
      self.draw = ImageDraw.Draw(self.image)
      
   def show( self ):
      self.image.show()   
      
   def flush( self ):
      root = tkinter.Tk()
      root.geometry('200x200')
      canvas = tkinter.Canvas(root,width=199,height=199)
      canvas.pack()
      self._screenshot = PIL.ImageTk.PhotoImage( self.image )
      imagesprite = canvas.create_image(self.size[0], self.size[1],image=self._screenshot)
      root.mainloop()   

def main():
    w = lcd( (128,64) )
    #image = Image.new('RGB', (frameSize), 'white')
    #font = ImageFont.truetype("FreeMonoBold.ttf", 12, encoding="unic")
    #draw = ImageDraw.Draw(image)
    
    #w.rectangle([(1,1), (w.size[0]-2,w.size[1]-2)], 'blue', 'yellow')
    #w.rectangle([(5,5), (10,10)], 'blue', 'yellow')
    #draw.text((5, 5), 'Hello World', fill='white', font=font)
    
    w.draw.rectangle([(1,1), (120,60)], 'yellow', 'blue')
    w.draw.text((5, 5), 'Hello World', fill='green')    
    '''
    # Output to OLED/LCD display
    device.display(image)
    '''
    # Output to PC image viewer
    w.show()
    w.flush()
    
    #sleep(5)
    
if __name__ == "__main__":
    main()
