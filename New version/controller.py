from neopixel import *
import numpy as np 

strip = Adafruit_NeoPixel(177, 8, 800000, 5, False, 255) #Pin = 18 (2nd Param)
strip.begin()

def clear():
    for x in range(strip.numPixels()):
        strip.setPixelColorRGB(x,0,0,0)
    strip.show()

def setStripBrightness(value):
    strip.setBrightness(value)
    strip.show()

def getRrbColor(position):
    colorHex = hex(np.asscalar(np.uint32(strip.getPixelColor(position))))
    colorHex = colorHex.lstrip('0x')
    colorHex = colorHex.rstrip('L')
    if len(colorHex) < 6:
        output = ""
        for a in range(6-len(colorHex)):
            output = output + "0"
        colorHex = output + colorHex
    rgbColor = tuple(map(ord,colorHex.decode('hex')))
    return rgbColor

def fadeStripBrightness(value,speed):
    matrix = [[0 for x in range(7)] for y in range(strip.numPixels())]
    stateoff = True if int(value) == 0 else False

    for pos in range(strip.numPixels()):
        rgbColor = getRrbColor(pos)

        #write rate for color into matrix 
        maxValue = max(rgbColor)
        for y in range(7):
            if y < 3:
                #0-2 stores realy current rgb values
                matrix[pos][y] = rgbColor[y]
            elif y == 6:
                #3-5 stores the rates of the maximum value to the other
                matrix[pos][y] = maxValue
            else:
                #6 stores the max brightness
                matrix[pos][y] = 0 if maxValue == 0 else float((rgbColor[y-3] * 1.0) / (maxValue * 1.0))

    #define the number of fade steps
    brightness = [0] * int(strip.numPixels())
    for x in range(strip.numPixels()):
        brightness[x] = matrix[x][6]
    difMaxBrightness = max(brightness) - int(value)
    difMinBrightness = min(brightness) - int(value)
    itterations = abs(difMaxBrightness) if abs(difMaxBrightness) > abs(difMinBrightness) else abs(difMinBrightness)

    for x in range(strip.numPixels()):
        for y in range(3):
            if itterations != 0:
                matrix[x][y+3] = (((matrix[x][y+3] * value) - matrix[x][y]) / itterations)

    for itt in range(itterations+1):
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,int(matrix[x][0] + (itt * matrix[x][3])),int(matrix[x][1] + (itt * matrix[x][4])),int(matrix[x][2] + (itt * matrix[x][5])))
        strip.show()
        if itterations > 0:
            time.sleep(float((speed * 1.0 /1000.0)/(itterations * 1.0)))

def fadeStripBrightness2(value,speed):
    currentBrightness = 255 #to be implemented
    fadeRange = currentBrightness - value

if fadeRange > 0:
    fade(currentBrightness,fadeRange,-1)
elif fadeRange < 0:
    #fade up
    fade(currentBrightness,fadeRange,1)
else:
    fade(currentBrightness,0,0)
    #nothering

def fade (value,fadeRange,direction):
    for x in range(fadeRange):
        strip.setBrightness(value + (x*direction))
        strip.show()
        