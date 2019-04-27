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
    fadeTime = 0.01

    global switchStatus
    #Constructor
    def __init__(self, num, pin):
        # config strip
        self.strip = Adafruit_NeoPixel(num,pin,800000,10,False,255)
        strip.begin()

        # List to store current color values
        #The tupel show the values (brightness,red,green,blue,brightness)
        self.stripStatusList = [[0,0,0,0]] * num
        self.switchStatus = False
        #Test Color
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,100,100,100)
            self.stripStatusList[x] = [0,100,100,100,10]
        strip.setBrightness(10)
        self.switchStatus = True
        #strip.show() #to be included after testing

        #test
        #print(self.ColorRGB(0,100,150,200))
        #print(bin(self.ColorRGB(0,100,150,200)))
        #print(self.ColorNum(self.ColorRGB(0,100,150,200)))
        self.stripStatusList[10] = [0,255,200,100,10]
        self.stripStatusList[20] = [0,0,0,255,10]

        

    #Resets whole LED strip
    def clear(self):
        logging.info('Strip cleared')
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,0,0,0)
            self.stripStatusList[x] = [0,0,0,0,0]
        strip.show()
        print("Done")

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
                current[4] = int(value)
                self.stripStatusList[x] = current
        print("Done - not jet finished")

    def turn_on_animation (self):
        for y in range(1,3):
            for x in range(strip.numPixels()):
                current = self.stripStatusList[x]
                if y == 1:
                    strip.setPixelColorRGB(x,int(current[1] * 0.5),int(current[2] * 0.5),int(current[3] * 0.5))
                    strip.setBrightness(int(current[4] * 0.5))
                    print(int(current[1] * 0.5))
                else:
                    strip.setPixelColorRGB(x,current[1],current[2],current[3])
                    strip.setBrightness(current[4])
                    print(current[1])
                #strip.show()
                time.sleep(fadeTime)
        logging.info('Animation done')
        print("Done")

    def switch(self, value):
        if value == "OFF":
            self.fadeStripBrightness(0,False)
            strip.show()
            logging.info('Strip switched off')
            self.switchStatus = False
        elif value == "ON":
            if not self.switchStatus:
                self.turn_on_animation()
        print("Done")

    def fadeColor(self,red,green,blue):
        print("GO")
        delta = 0

        #Define max fade range
        for x in self.stripStatusList:
            print(str(x[1])+","+str(x[2])+","#str(x[3]))
            if abs(red - x[1]) > abs(delta):
                delta = red - x[1]
            if abs(green - x[2]) > abs(delta):
                delta = green - x[2]
            if abs(blue - x[3]) > abs(delta):
                delta = blue - x[3]
        print(delta)
        #set Color steop by step in delta+1 steps to final value
        for y in range(abs(delta)+1):
            print(y)
            for x in range(strip.numPixels()):
                red_old = self.stripStatusList[x][1]
                green_old = self.stripStatusList[x][2]
                blue_old = self.stripStatusList[x][3]
                strip.setPixelColorRGB(x, red_old - (((red - red_old)/delta)*y), green_old - (((green - green_old)/delta)*y),
                 blue_old - (((blue - blue_old)/delta)*y))
                if x == 1:
                    print(str(red_old - (((red - red_old)/delta)*y))+","+ str(green_old - (((green - green_old)/delta)*y))+"," + 
                    str(blue_old - (((blue - blue_old)/delta)*y)))
            #strip.show()
            time.sleep(fadeTime)
        
        #adjust stored r,g,b values
        for x in range(strip.numPixels()):
            current = self.stripStatusList[x]
            current[1] = red
            current[2] = green
            current[3] = blue
            self.stripStatusList[x] = current
        print("Done")
                 



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
        return [int(white),int(red),int(green),int(blue)]