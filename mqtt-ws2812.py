#!/usr/bin/env python
import paho.mqtt.client as mqtt
from neopixel import *
import numpy as np 


strip = Adafruit_NeoPixel(16, 18, 800000, 5, False, 255)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("zimmer/#")
    strip.begin()

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    if msg.topic == "zimmer/map/brightness/set":
        print("Brightness of Strip will be changed to " + str(msg.payload))
        currrentBrightness = np.uint8(strip.getBrightness())
        dif = int(msg.payload) - currrentBrightness
        if dif > 0:
            for x in range(1,dif):
                strip.setBrightness(currrentBrightness + x)
                strip.show
        elif dif < 0:
            dif = dif * (-1)
            for x in range(1,dif):
                strip.setBrightness(currrentBrightness - x)
                strip.show

        strip.setBrightness(int(msg.payload))
        strip.show
        bright = np.uint8(strip.getBrightness())
        print("before: " + str(currrentBrightness) + " / msg:: " + str(msg.payload) + " / actual: " + str(bright))
    else:
        print("else")
    
    print(" ")
    strip.setPixelColorRGB(1, 0, 255, 0)
    strip.show()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.114", 1883, 60)

client.loop_forever()


