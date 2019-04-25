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

    global switchStatus
    #Constructor
    def __init__(self, num, pin):
        # config strip
        self.strip = Adafruit_NeoPixel(num,pin,800000,10,False,255)
        strip.begin()

        # List to store current color values
        #The tupel show the values (brightness,red,green,blue,brightness)
        self.stripStatusList = [(0,0,0,0)] * num
        self.switchStatus = False
        #Test Color
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,100,100,100)
            self.stripStatusList[x] = (0,100,100,100,10)
        strip.setBrightness(10)
        self.switchStatus = True
        #strip.show() #to be included after testing

        #test
        #print(self.ColorRGB(0,100,150,200))
        #print(bin(self.ColorRGB(0,100,150,200)))
        #print(self.ColorNum(self.ColorRGB(0,100,150,200)))

        

    #Resets whole LED strip
    def clear(self):
        logging.info('Strip cleared')
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
            self.stripStatusList[x] = (0,0,0,0,0)
        strip.show()

    #Sets the brightness of the whole strip | update is a bool to indicate 
    #if the status List should be updated or not
    #this is set to false when the strip is switched off in order
    #to store the last brightness value of the strip
    def fadeStripBrightness(self,value,update):
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
        if update:
            for x in range(strip.numPixels()):
                current = self.stripStatusList[x]
                current[4] = value
                self.stripStatusList[x] = current

    def turn_on_animation (self):
        for y in range(1,2):
            print(y)
            print(y*2)
            print((y*2)%4)
            print(float(((y*2)%4)/(-4)))
            print((float(((y*2)%4)/(-4)))+1.0)
            for x in range(strip.numPixels()):
                current = self.stripStatusList[x]
                print(float((((y*2)%4)/(-4))+1))
                strip.setPixelColorRGB(x,current[1] * ((((y*2)%4)/-4)+1),current[2] * ((((y*2)%4)/-4)+1),current[3] * ((((y*2)%4)/-4)+1))
                strip.setBrightness(current[4] * ((((y*2)%4)/-4)+1))
                #strip.show()
                #time.sleep(fadeTime)

    def switch(self, value):
        if value == "OFF":
            self.fadeStripBrightness(0,False)
            strip.show()
            logging.info('Strip switched off')
            self.switchStatus = False
        elif value == "ON":
            if self.switchStatus:
                self.switchStatus = True
            else:
                self.turn_on_animation()

    def ColorRGB (self,white,red,green,blue):
        return (white << 24) | (red << 16)| (green << 8) | blue

    def ColorNum (self,num):
        #using Binary logic to decode numeric input to (white,red,green.blue) tupel
        # bin of num is a 32 bit sequemce
        # using logical & to get bit sequence of the first, second, third and fourth
        # block of 8 bit e.g.
        # 10100010010101010101110000 & 00000000111111110000000000000000

        white = (4278190080 & num) >> 24
        red = (16711680 & num) >> 16
        green = (65280 & num) >> 8
        blue = 255 & num
        return (int(white),int(red),int(green),int(blue))
