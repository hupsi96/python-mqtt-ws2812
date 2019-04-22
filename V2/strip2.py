import time
import board
import neopixel

#pixel_pin = board.D18
num_pixels = 30
#ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(18, num_pixels) #, brightness=0.2, auto_write=False,pixel_order=neopixel.RGB)

