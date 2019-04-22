from neopixel import *
#import logging

class strip_config:
    global strip
    strip = Adafruit_NeoPixel(177, 18, 800000, 5, False, 255) #Pin = 18 (2nd Param)
    def __init__(self, num, pin):
        strip = Adafruit_NeoPixel(num,pin,800000,10,False,255)
        strip.begin()

    def clear(self):
        #logging.basicConfig(filename='WS2812Controller.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d.%m.%y %I:%M:%S %p')
        #logging.info('Strip cleared')
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
        strip.show()

test = strip_config(177,19)
test.clear()