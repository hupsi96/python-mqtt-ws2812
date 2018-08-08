#!/usr/bin/env python
import paho.mqtt.client as mqtt
from neopixel import *
import numpy as np 
import time


strip = Adafruit_NeoPixel(16, 18, 800000, 5, False, 255)
strip.begin()
global currrentBrightness
currrentBrightness = np.uint8(strip.getBrightness())
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("zimmer/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    global currrentBrightness
#Brightness
    if msg.topic == "zimmer/map/brightness/set":
        
        fade_brightness(msg.payload,.030)
        
        bright = np.uint8(strip.getBrightness())
        print("before: " + str(currrentBrightness) + " / msg:: " + str(msg.payload) + " / actual: " + str(bright) + " / CURRENTvalue: " + str(currrentBrightness))

    elif msg.topic == "zimmer/map/light/switch":
        if msg.payload == "ON" and currrentBrightness == 0:
            fade_brightness(currrentBrightness,.030)
        elif msg.payload == "OFF" and currrentBrightness != 0:
            fade_brightness(0,.050)
        else:
            print("ignoreee")


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
        currrentBrightness = np.uint8(strip.getBrightness())
    elif dif < 0:
        dif = dif * (-1)
        for x in range(1,dif+1):
            strip.setBrightness(currrentBrightness - x)
            strip.show
            print(str(currrentBrightness - x))
            time.sleep(speed)
        currrentBrightness = np.uint8(strip.getBrightness())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.114", 1883, 60)

client.loop_forever()


