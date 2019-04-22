from neopixel import *

class strip:
    strip = Adafruit_NeoPixel(177, 18, 800000, 5, False, 255) #Pin = 18 (2nd Param)
    def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False, brightness=255):
        strip = Adafruit_NeoPixel(num,pin,freq_hz,dma,invert,brightness)
        strip.begin()

    def clear():
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
        strip.show()

        