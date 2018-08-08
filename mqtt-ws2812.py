#!/usr/bin/env python
import paho.mqtt.client as mqtt
from neopixel import *

strip = Adafruit_NeoPixel(16, 18, 800000, 5, False, 255)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("zimmer/#")
    strip.begin()
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    switch (msg.topic) 
    {
        case zimmer/map/brightness/set:
            print("testtest");
            break;
        default:
            print("default")
            break;
    }
    
    
    strip.setPixelColorRGB(1, 0, 255, 0)
    strip.show()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.114", 1883, 60)

client.loop_forever()


