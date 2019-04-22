from neopixel import *

class strip:
    global strip  # = Adafruit_NeoPixel(177, 18, 800000, 5, False, 255) #Pin = 18 (2nd Param)
    def __init__(self, num, pin):
        strip = Adafruit_NeoPixel(num,pin,800000,10,False,255)
        strip.begin()

    def clear():
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
        strip.show()

