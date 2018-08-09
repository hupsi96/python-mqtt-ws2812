#!/usr/bin/env python
import paho.mqtt.client as mqtt
from neopixel import *
import numpy as np 
import time


strip = Adafruit_NeoPixel(16, 18, 800000, 5, False, 255)
strip.begin()
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
    strip.setPixelColorRGB(1, 0, 255, 0)
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
    currentColor = hex(np.asscalar(np.uint32(strip.getPixelColor(10))))
    value = currentColor.lstrip('0x')
    value = value.rstrip('L')
    lv = len(value)
    rgbCurrentColor = tuple(int(value[i:i + lv // 3], 16) for i in range(0,lv, lv // 3))
    print(currentColor)
    print(output)
    for x in range(strip.numPixels()):
        print("test")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.114", 1883, 60)

client.loop_forever()


