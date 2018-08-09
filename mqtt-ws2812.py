#!/usr/bin/env python
import paho.mqtt.client as mqtt
from neopixel import *
import numpy as np 
import time


strip = Adafruit_NeoPixel(100, 18, 800000, 5, False, 255)
strip.begin()
strip.clean()
global currrentBrightness
global stateoff
stateoff = False
currrentBrightness = np.uint8(strip.getBrightness())
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("zimmer/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    global currrentBrightness
    global stateoff

#Brightness
    if msg.topic == "zimmer/map/brightness/set":
        fade_brightness(msg.payload,.030)
#Switch        
    elif msg.topic == "zimmer/map/light/switch":
        if msg.payload == "ON" and stateoff == True:
            fade_brightness(currrentBrightness,.030)
            print(currrentBrightness)
            stateoff = False
        elif msg.payload == "OFF" and stateoff ==False:
            fade_brightness(0,.050)
            print(currrentBrightness)
            stateoff = True
        else:
            print("ignoreee")
            print(currrentBrightness)
#RGB
    elif msg.topic == "zimmer/map/rgb/set":
        data = str(msg.payload).split(",")
        red = int(data[0])
        green = int(data[1])
        blue = int(data[2])
        print("red: " + str(red) + " green: " + str(green) + " blue: " + str(blue))
        strip.setPixelColorRGB(10,50,50,50)
        fade_color(red,green,blue,1000)


    else:
        print("else")
        print(" ")
        strip.setPixelColorRGB(0, 0, 255, 0)
        strip.setPixelColorRGB(1, 0, 255, 0)
        strip.setPixelColorRGB(2, 0, 255, 0)
        strip.setPixelColorRGB(3, 0, 255, 0)
        strip.setPixelColorRGB(4, 0, 255, 0)
        strip.show()
        
    

def fade_brightness(value,speed):
    dif = int(value) - currrentBrightness
    global currrentBrightness
    if dif > 0:
        for x in range(1,dif+1):
            strip.setBrightness(currrentBrightness + x)
            strip.show
            print(str(currrentBrightness + x))
            time.sleep(speed)
    elif dif < 0:
        dif = dif * (-1)
        for x in range(1,dif+1):
            strip.setBrightness(currrentBrightness - x)
            strip.show
            print(str(currrentBrightness - x))
            time.sleep(speed)
    if value != 0:
        currrentBrightness = np.uint8(strip.getBrightness())

def fade_color(red,green,blue,fadeTime):
    dif = 0
    for x in range(strip.numPixels()):
        currentColor = hex(np.asscalar(np.uint32(strip.getPixelColor(x))))
        value = currentColor.lstrip('0x')
        value = value.rstrip('L')
        lv = len(value)
        rgbCurrentColor = tuple(int(value[i:i + lv // 3], 16) for i in range(0,lv, lv // 3))
        if len(rgbCurrentColor) > 3:
            if (int(rgbCurrentColor[0]) - int(red)) >= 0:
                reddif = int(rgbCurrentColor[0]) - int(red)
            else:
                reddif = (int(rgbCurrentColor[0]) - int(red)) * (-1)
            if (int(rgbCurrentColor[1]) - int(green)) >= 0:
                greendif = int(rgbCurrentColor[1]) - int(green)
            else:
                greendif = (int(rgbCurrentColor[1]) - int(green)) * (-1)
            if (int(rgbCurrentColor[2]) - int(blue)) >= 0:
                bluedif = int(rgbCurrentColor[2]) - int(blue)
            else:
                bluedif = (int(rgbCurrentColor[2]) - int(blue)) * (-1)
            if reddif > dif:
                dif = reddif
            if greendif > dif:
                dif = greendif
            if bluedif > dif:
                dif = bluedif

        for x in range(1,dif+1):
            for pixel in range(strip.numPixel()):
                currentColor = hex(np.asscalar(np.uint32(strip.getPixelColor(x))))
                value = currentColor.lstrip('0x')
                value = value.rstrip('L')
                lv = len(value)
                rgbCurrentColor = tuple(int(value[i:i + lv // 3], 16) for i in range(0,lv, lv // 3))
                newRedValue = 0
                newGreenValue = 0
                newBlueValue = 0
                if len(rgbCurrentColor) > 3:
                    if red > rgbCurrentColor[0]:
                        newRedValue = rgbCurrentColor[0] + 1
                    elif red < rgbCurrentColor[0]:
                        newRedValue = rgbCurrentColor[0] - 1
                    else:
                        newRedValue = red

                    if green > rgbCurrentColor[1]:
                        newGreenValue = rgbCurrentColor[1] + 1
                    elif green < rgbCurrentColor[1]:
                        newGreenValue = rgbCurrentColor[1] - 1
                    else:
                        newGreenValue = green

                    if blue > rgbCurrentColor[3]:
                        newBlueValue = rgbCurrentColor[3] + 1
                    elif blue < rgbCurrentColor[3]:
                        newBlueValue = rgbCurrentColor[3] - 1
                    else:
                        newBlueValue = blue
                    strip.setPixelColorRGB(pixel,newRedValue,newGreenValue,newBlueValue)
        strip.show



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.114", 1883, 60)

client.loop_forever()


