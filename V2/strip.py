from neopixel import *
import logging
import time

class strip_config:

    #define strip globaly and set default values
    global strip
    strip = Adafruit_NeoPixel(177, 18, 800000, 5, False, 255) #default setting

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

        # List to store current color values
        self.colorList = [[0,0,0]] * num

    #Resets whole LED strip
    def clear(self):
        logging.info('Strip cleared')
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
            time.sleep(1)
        strip.show()

    #Sets the brightness of the whole strip
    def setStripBrightness(self,value):
        strip.setBrightness(value)
        strip.show()

    def switch(self, value):
        if value == "OFF":
            print("one")
        elif value == "ON":
            print("two")