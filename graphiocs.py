import tKinter as tk

root = tk.Tk()

class window_native:

   def __init__( self, size ):
      self.size = size
      self.window = tk.Toplevel( root )
      
   def write( location, color ):
      self

class line:

   def __init__( self, start, end ):
      self.start = start
      self.end = end
      
   def write( self, window ):      
      x0 = start.x;
      y0 = start.y;
      x1 = end.x; 
      y1 = end.y;
                   
      // http://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
      // http://homepages.enterprise.net/murphy/thickline/index.html
     
      Dx = x1 - x0 
      Dy = y1 - y0
      steep = (abs(Dy) >= abs(Dx))
   
      if steep:
         ( x0, y0, x1, y1 ) = ( y0, x0, y1, x1 )
      
         // recompute Dx, Dy after swap
         Dx = x1 - x0
         Dy = y1 - y0
   
      xstep = 1
      if Dx < 0:
         xstep = -1
         Dx = -Dx
   
      ystep = 1
      if Dy < 0:
         ystep = -1
         Dy = -Dy
      
      TwoDy = 2 * Dy 
      TwoDyTwoDx = TwoDy - 2 * Dx   # 2*Dy - 2*Dx
      E = TwoDy - Dx                # 2*Dy - Dx
      y = y0
      x = x0
      while x != x1:
         if steep:
            xDraw = y
            yDraw = x
         else: 
            xDraw = x
            yDraw = y

         window.write( xy( xDraw, yDraw ), color );

         if E > 0:
            E += TwoDyTwoDx         # E += 2*Dy - 2*Dx;
            y = y + ystep 
         else:
            E += TwoDy              # E += 2*Dy;
         x += xstep
         
root.mainloop()         