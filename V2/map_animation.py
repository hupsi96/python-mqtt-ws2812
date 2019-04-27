from neopixel import *
import logging
import time

class animation_setup:

    global waveArray
    global strip

    def __init__(self,stripInput):

        self.strip = stripInput
        #to be further developed - animation for map to usefull in my opinion
        self.waveArray = [[103],[102,104],[101,105,106],[100,107,108,109,57,99,110,111]]

    def waveAnimation(self):
        for x in self.waveArray:
            for y in x:
                self.strip.setPixelColorRGB(y,0,100,0)
            self.strip.show()
            time.sleep(5)