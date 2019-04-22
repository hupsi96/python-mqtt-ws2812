import time
import board
import neopixel

#pixel_pin = board.D18
num_pixels = 30
#ORDER = neopixel.RGB

pixels = Adafruit_NeoPixel(board.D18, num_pixels) #, brightness=0.2, auto_write=False,pixel_order=neopixel.RGB)

pixels[0] = (255,0,0)
