#!/usr/bin/env python
import paho.mqtt.client as mqtt
from neopixel import *
import numpy as np 
import time
from random import randint



stateoff = True
strip = Adafruit_NeoPixel(20, 18, 800000, 5, False, 255)
strip.begin()
global currrentBrightness
currrentBrightness = 255#np.uint8(strip.getBrightness())

def clear():
    for x in range(strip.numPixels()):
        strip.setPixelColorRGB(x,0,0,0)
    strip.show()

def setStripBrightness(value):
    strip.setBrightness(value)
    strip.show()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for pos in range(strip.numPixels()):
        strip.setPixelColorRGB(pos,randint(0,255),randint(0,255),randint(0,255))
    strip.show()
    print("Test color was turned on")
    client.subscribe("zimmer/#")

# converts the Hex value of the Pixel @position to the corresponding rgb value
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

    for pos in range(strip.numPixels()):
        print("pos: " + str(pos))
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
            print(matrix[pos][y])
        print("")

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
            #print(matrix[x][y+3])
        #print("")

    for itt in range(itterations+1):
        for x in range(strip.numPixels()):
            strip.setPixelColorRGB(x,int(matrix[x][0] + (itt * matrix[x][3])),int(matrix[x][1] + (itt * matrix[x][4])),int(matrix[x][2] + (itt * matrix[x][5])))
            #print("color set to: (" + str(int(matrix[x][0] + (itt * matrix[x][3]))) +"," + str(int(matrix[x][1] + (itt * matrix[x][4]))) +"," + str(int(matrix[x][2] + (itt * matrix[x][5]))) )
        
        strip.show()
        #time.sleep(float((speed/1000)/itterations))
        
def fadeStripRGB(red,green,blue):
    matrix = [[0 for x in range(7)] for y in range(strip.numPixels())]
    value = [int(red),int(green),int(blue)]
    for pos in range(strip.numPixels()):
        rgbColor = getRrbColor(pos)

        for y in range(5):
            if y < 3:
                matrix[pos][y] = rgbColor[y]
            elif y == 3:
                matrix[pos][y] = min(rgbColor)
            elif y == 4:
                matrix[pos][y] = max(rgbColor)

    #define the number of fading steps that are needed:
    maxValue = [0] * int(strip.numPixels())
    minValue = [0] * int(strip.numPixels())
    for x in range(strip.numPixels()):
        minValue[x] = matrix[x][3]
        maxValue[x] = matrix[x][4]
    difMaxValue = max(maxValue) - min(value)
    DifMinValue = min(minValue) - max(value)
    itterations = abs(DifMinValue) if abs(DifMinValue) > abs(difMaxValue) else abs(difMaxValue)
        

    
    




def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    #Brightness
    if msg.topic == "zimmer/map/brightness/set":
        fadeStripBrightness(int(msg.payload),1000)
    #Switch        
    elif msg.topic == "zimmer/map/light/switch":
        if msg.payload == "OFF":
            #fade_brightness(currrentBrightness,.030)
            fadeStripBrightness(0,1000)
            #print(currrentBrightness)
            #stateoff = False
        #elif msg.payload == "OFF" and stateoff ==False:
            #fade_brightness(0,.050)
            #print(currrentBrightness)
            #stateoff = True
        #else:
            #print("ignoreee")
            #print(currrentBrightness)
    #RGB
    elif msg.topic == "zimmer/map/rgb/set":
        data = str(msg.payload).split(",")
        red = int(data[0])
        green = int(data[1])
        blue = int(data[2])
        fadeStripRGB(red,green,blue)
        #print("red: " + str(red) + " green: " + str(green) + " blue: " + str(blue))
        #strip.setPixelColorRGB(10,50,50,50)
        #fade_color(red,green,blue,1000)


    #else:
        #print("else")
        #print(" ")
        #strip.setPixelColorRGB(0, 0, 255, 0)
        #strip.setPixelColorRGB(1, 0, 255, 0)
        #strip.setPixelColorRGB(2, 0, 255, 0)
        #strip.setPixelColorRGB(3, 0, 255, 0)
        #strip.setPixelColorRGB(4, 0, 255, 0)
        #strip.show()
        

clear()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.114", 1883, 60)

client.loop_forever()

#old code:

# def fade_brightness(value,speed):
#     curBright = currrentBrightness
#     dif = int(value) - int(curBright)
#     if dif > 0:
#         for x in range(1,dif+1):
#             strip.setBrightness(curBright + x)
#             strip.show()
#             print(str(curBright + x))
#             time.sleep(speed)
#     elif dif < 0:
#         dif = dif * (-1)
#         for x in range(1,dif+1):
#             strip.setBrightness(curBright - x)
#             strip.show()
#             print(str(curBright - x))
#             time.sleep(speed)
#     if value != 0:
#         global currrentBrightness
#         currrentBrightness = np.uint8(strip.getBrightness())

#def fade_color(red,green,blue,fadeTime):
    #dif = 0
    #for x in range(strip.numPixels()):
        #currentColor = hex(np.asscalar(np.uint32(strip.getPixelColor(x))))
        #value = currentColor.lstrip('0x')
        #value = value.rstrip('L')
        #lv = len(value)
        #rgbCurrentColor = tuple(int(value[i:i + lv // 3], 16) for i in range(0,lv, lv // 3))
        #if len(rgbCurrentColor) > 3:
            #if (int(rgbCurrentColor[0]) - int(red)) >= 0:
                #reddif = int(rgbCurrentColor[0]) - int(red)
            #else:
                #reddif = (int(rgbCurrentColor[0]) - int(red)) * (-1)
            #if (int(rgbCurrentColor[1]) - int(green)) >= 0:
                #greendif = int(rgbCurrentColor[1]) - int(green)
            #else:
                #greendif = (int(rgbCurrentColor[1]) - int(green)) * (-1)
            #if (int(rgbCurrentColor[2]) - int(blue)) >= 0:
                #bluedif = int(rgbCurrentColor[2]) - int(blue)
            #else:
                #bluedif = (int(rgbCurrentColor[2]) - int(blue)) * (-1)
            #if reddif > dif:
                #dif = reddif
            #if greendif > dif:
                #dif = greendif
            #if bluedif > dif:
                #dif = bluedif

        #for x in range(1,dif+1):
            #for pixel in range(strip.numPixel()):
                #currentColor = hex(np.asscalar(np.uint32(strip.getPixelColor(x))))
                #value = currentColor.lstrip('0x')
                #value = value.rstrip('L')
                #lv = len(value)
                #rgbCurrentColor = tuple(int(value[i:i + lv // 3], 16) for i in range(0,lv, lv // 3))
                #newRedValue = 0
                #newGreenValue = 0
                #newBlueValue = 0
                #if len(rgbCurrentColor) > 3:
                    #if red > rgbCurrentColor[0]:
                        #newRedValue = rgbCurrentColor[0] + 1
                    #elif red < rgbCurrentColor[0]:
                        #newRedValue = rgbCurrentColor[0] - 1
                    #else:
                        #newRedValue = red

                    #if green > rgbCurrentColor[1]:
                        #newGreenValue = rgbCurrentColor[1] + 1
                    #elif green < rgbCurrentColor[1]:
                        #newGreenValue = rgbCurrentColor[1] - 1
                    #else:
                        #newGreenValue = green

                    #if blue > rgbCurrentColor[3]:
                        #newBlueValue = rgbCurrentColor[3] + 1
                    #elif blue < rgbCurrentColor[3]:
                        #newBlueValue = rgbCurrentColor[3] - 1
                    #else:
                        #newBlueValue = blue
                    #strip.setPixelColorRGB(pixel,newRedValue,newGreenValue,newBlueValue)
        #strip.show