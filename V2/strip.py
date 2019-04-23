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
    global stripStatusList

    #fadeTime for all fading functions - default value "medium"
    global fadeTime
    fadeTime = 0.05

    #Constructor
    def __init__(self, num, pin):
        # config strip
        self.strip = Adafruit_NeoPixel(num,pin,800000,10,False,255)
        strip.begin()

        # List to store current color values
        #The tupel show the values (brightness,red,green,blue)
        self.stripStatusList = [(0,0,0,0)] * num

        #Test Color
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,100,100,100)
            self.stripStatusList[x] = (10,100,100,100)
        strip.setBrightness(10)
        #strip.show() #to be included after testing

        #test
        print(self.ColorRGB(0,100,150,200))
        print(bin(self.ColorRGB(0,100,150,200)))
        print(self.ColorNum(self.ColorRGB(0,100,150,200)))

        

    #Resets whole LED strip
    def clear(self):
        logging.info('Strip cleared')
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
            self.stripStatusList[x] = (0,0,0,0)
        strip.show()

    #Sets the brightness of the whole strip
    def setStripBrightness(self,value):
        #current brightness of the whole strip
        currentBirghtness = strip.getBrightness()

        #steps needed to fade strip
        delta = currentBirghtness - value

        #value for for-loop - has to be positiv
        boundary = delta if delta > 0 else (delta * (-1))
        for x in range(0,boundary +1):
            if delta < 0:
                strip.setBrightness(currentBirghtness+x)
            elif delta > 0:
                strip.setBrightness(currentBirghtness-x)
            #strip.show() # to be included after testing
            time.sleep(fadeTime)
        logging.info('Brightness set to: +' + str(value))



    def switch(self, value):
        if value == "OFF":
            self.setStripBrightness(0)
            strip.show()
        elif value == "ON":
            print("two")

    def ColorRGB (self,white,red,green,blue):
        return (white << 24) | (red << 16)| (green << 8) | blue

    def ColorNum (self,num):
            return (self.extractKBits(num,8,25),self.extractKBits(num,8,17),self.extractKBits(num,8,9),self.extractKBits(num,8,1))

    def extractKBits(self,num,k,p): 

        # convert number into binary first 
        binary = bin(num) 
        print(binary)
        test = bin(binary << (34 - len(binary)))
        print test
        # remove first two characters 
        binary = binary[2:]
        print(binary)
        binary = binary << (32 - len(binary))
        if p > len(binary):
            return bin(0)
        else:
            end = len(binary) - p
            print(end)
            start = end - k + 1
            print(start)
  
            # extract k  bit sub-string 
            kBitSubStr = binary[start : end+1] 

            # convert extracted sub-string into decimal again 
            print(kBitSubStr)
            return kBitSubStr