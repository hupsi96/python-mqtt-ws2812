from neopixel import *
import logging

class strip_config:

    global strip
    strip = Adafruit_NeoPixel(177, 18, 800000, 5, False, 255) #default setting

    logging.basicConfig(filename='WS2812Controller.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d.%m.%y %I:%M:%S %p')

    global colorList

    def __init__(self, num, pin):
        self.strip = Adafruit_NeoPixel(num,pin,800000,10,False,255)
        strip.begin()
        self.colorList = [none] * num

    def clear(self):
        logging.info('Strip cleared')
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
        strip.show()

    def setStripBrightness(value):
        strip.setBrightness(value)
        strip.show()

    def switch(value):
        if value == "OFF":

        elif value == "ON":