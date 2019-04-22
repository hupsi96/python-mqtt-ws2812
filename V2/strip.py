from neopixel import *
import logging
import time
import numpy as np

class strip_config:

    #define strip globaly and set default values
    global strip
    strip = Adafruit_NeoPixel(177, 12, 800000, 5, False, 255) #default setting """Adafruit_NeoPixel"""

    #confic logging module
    logging.basicConfig(filename='WS2812Controller.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d.%m.%y %I:%M:%S %p')
    #define global List to store Colurs for all LEDs
    global colorList

    #Constructor
    def __init__(self, num, pin):
        # config strip
        self.strip = Adafruit_NeoPixel(num,pin,800000,10,False,255)
        strip.begin()

        #Test Color
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,100,100,100)
        strip.setBrightness(100)
        #strip.show()
        # List to store current color values
        self.colorList = [[0,0,0]] * num

    #Resets whole LED strip
    def clear(self):
        logging.info('Strip cleared')
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
        strip.show()

    #Sets the brightness of the whole strip
    def setStripBrightness(self,value):
        currentBirghtness = strip.getBrightness()
        print(currentBirghtness)
        delta = currentBirghtness - value
        print(delta)

        boundary = delta if delta > 0 else (delta * (-1))
        for x in range(0,boundary +1):
            if delta < 0:
                print(currentBirghtness+x)
            elif delta > 0:
                print(currentBirghtness-x)



    def switch(self, value):
        if value == "OFF":
            strip.setBrightness(0)
            strip.show()
        elif value == "ON":
            print("two")