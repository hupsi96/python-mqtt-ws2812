#!/usr/bin/env python
import paho.mqtt.client as mqtt
from neopixel import *
import numpy as np 
import time
from random import randint
import requests
import config
import multiprocessing
import json

stateoff = False
strip = Adafruit_NeoPixel(92, 18, 800000, 5, False, 255)
strip.begin()
defaultColor = (255,255,255)
fadeTime = 1000

myToken = '&APPID=' + config.weatherApiToken
weatherList = [""] * int(strip.numPixels())
cityList = [""] * int(strip.numPixels())
weatherColorList = [""] * int(strip.numPixels())
#North America City Mapping:
cityList = [("5994339","Kuluktuk"),("5916134","Cape Parry"),("5914276","Camp Farewell"),("5865670","Kaktovik"),("4181182","Barrow County"),("5871778","Point Lay"),
("5866726","Kotzebue"),("5860695","Dillingham"),("5877389","Valdez"),("6180550","Whitehorse"),("5986080","Jedway"),("6173331","Vancouver"),
("4152291","Crescent City"),("5391959","San Francisco"),("5368361","Los Angeles"),("4004898","Hermosillo"),("4005539","Guadalajara"),("4699066","Houston"),
("4241704","Jacksonville"),("4145381","Wilmington"),("5128638","New York"),("6138517","Saint John"),("5927969","Corner Brook"),("5970458","Happy Valley-Goose Bay"),
("5989203","Kangiqsualujjuaq"),("5882994","Akulivik"),("5955950","Fort Severn"),("5927708","Coral Harbour"),("5961560","Gjoa Haven"),("5913698","Cambridge Bay"),
("5994339","Kuluktuk"),("5994339","Kuluktuk"),("5994339","Kuluktuk")]

global p2

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
        strip.setPixelColorRGB(pos,0,255,0)#randint(0,255),randint(0,255),randint(0,255)) order g,r,b
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
    stateoff = True if int(value) == 0 else False
    print("fadetime: " + str(speed))

    for pos in range(strip.numPixels()):
        #print("pos: " + str(pos))
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
            #print(matrix[pos][y])
        #print("")

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
        #print(str(float((speed * 1.0 /1000.0)/(itterations * 1.0))))
        strip.show()
        if itterations > 0:
            time.sleep(float((speed * 1.0 /1000.0)/(itterations * 1.0)))

#O(n) = n*5 + n + n * 3 + itt * n = 9*n + itt*n        
def fadeStripRGB(red,green,blue,speed):
    print("fadetime: " + str(speed))
    matrix = [[0 for x in range(8)] for y in range(strip.numPixels())]
    value = [int(green),int(red),int(blue)]
    stateoff = False
    #O(n) = n * 5
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
    #O(n) = n
    for x in range(strip.numPixels()):
        minValue[x] = matrix[x][3]
        maxValue[x] = matrix[x][4]
    difMaxValue = max(maxValue) - min(value)
    DifMinValue = min(minValue) - max(value)
    itterations = abs(DifMinValue) if abs(DifMinValue) > abs(difMaxValue) else abs(difMaxValue)
    #O(n) = n * 3    
    for x in range(strip.numPixels()):
        for y in range(3):

            matrix[x][y+5] = 0 if itterations == 0 else ((value[y] - rgbColor[y]) * 1.0) / (itterations * 1.0)
    #O(n) = numberOfFadesteps * n -> max: 255 * n min: n
    for itt in range(itterations + 1):
        for x in range(strip.numPixels()):
            #print(str(matrix[x][0]) + ":" + str(matrix[x][1]) + ":" + str(matrix[x][2]) + ":" + str(matrix[x][3]) + ":" + str(matrix[x][4]) + ":" + str(matrix[x][5]) + ":" + str(matrix[x][6]) + ":" + str(matrix[x][7]))
            #print(str(x) + ", " + str(int(matrix[x][0])) + " + (" + str(int(itt)) + " * " + str(int(matrix[x][5])) + "), ...")
            strip.setPixelColorRGB(x,int(matrix[x][0]+ (itt * matrix[x][5])),int(matrix[x][1]+ (itt * matrix[x][6])),int(matrix[x][2]+ (itt * matrix[x][7])))
        strip.show()
        if itterations > 0:
            time.sleep(float((speed * 1.0 /1000.0)/(itterations * 1.0)))

def weatherMap():
    while True:
        for x in range(len(cityList)):
            myUrl = 'http://api.openweathermap.org/data/2.5/weather?id=' + cityList[x][0] + myToken
            print(myUrl)
            #errors have to be caught here 
            response = requests.get(myUrl)
            print(str(response.status_code))
            output = json.loads(response.text)
            temp = output.get('main').get('temp')
            tempCels = temp -  273.15
            weatherList[x] = tempCels
        print(str(weatherList))

        for x in range(len(weatherList)):
            red = 0
            green = 0
            blue = 0
            if weatherList[x] >= 50:
                red = 255
            elif weatherList[x] < 50 and weatherList[x] >= 30:
                red = 255
                green = int(100 - ((weatherList[x]-30) * 5))
            elif weatherList[x] < 30 and weatherList[x] >= 20:
                red = 255
                green = int(100 + ((30 - weatherList[x]) * 15.5))
            elif weatherList[x] < 20 and weatherList[x] >= 10:
                red = int(105 + ((weatherList[x] - 10)* 15))
                green = 255
                blue = int((20 - weatherList[x]) * 15)
            elif weatherList[x] < 10 and weatherList[x] >= 0:
                red = int(weatherList[x] * 10.5)
                green = 255
                blue = int(255 - (weatherList[x] * 10.5))
            elif weatherList[x] < 0 and weatherList[x] >= -10:
                green = int(255 - (abs(weatherList[x]) *10))
                blue = 255
            elif weatherList[x] < -10 and weatherList[x] >= -50:
                green = int(155 - ((abs(weatherList[x]) - 10) * 3.875))
                blue = 255
            elif weatherList[x] < -50:
                blue = 255
            weatherColorList[x] = (red,green,blue)
            strip.setPixelColorRGB(x,green,red,blue)
        print(str(weatherColorList))
        strip.show()
        time.sleep(360)
    print("Thread closed")



def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    global defaultColor
    global stateoff
    global defaultColor
    global fadeTime
    global p2

    #Brightness
    if msg.topic == "zimmer/map/brightness/set":
        fadeStripBrightness(int(msg.payload),fadeTime)
        stateoff = False

    #Switch        
    elif msg.topic == "zimmer/map/light/switch":
        if msg.payload == "OFF":
            #fade_brightness(currrentBrightness,.030)
            fadeStripBrightness(0,fadeTime)
            stateoff = True

        elif msg.payload == "ON" and stateoff == True:
            fadeStripRGB(int(defaultColor[0]),int(defaultColor[1]),int(defaultColor[2]),fadeTime)
            stateoff = False

    #RGB
    elif msg.topic == "zimmer/map/rgb/set":
        print(p2.is_alive())
        if p2.is_alive() == True:
            p2.terminate()
            p2.join()
        data = str(msg.payload).split(",")
        red = int(data[0])
        green = int(data[1])
        blue = int(data[2])
        defaultColor = data
        fadeStripRGB(red,green,blue,fadeTime)
        stateoff = False
    elif msg.topic == "zimmer/map/effect/set":
        if msg.payload == "fade1":
            fadeTime = 1000
        if msg.payload == "fade3":
            fadeTime = 3000
        if msg.payload == "fade5":
            fadeTime = 5000
        if msg.payload == "fade10":
            fadeTime = 10000
        if msg.payload == "weather":
            
            p2.start()
            #thread.start_new_thread(weatherMap,())
            #weatherThread.run()
    print("done")
        
#weatherThread = threading.Thread(target = weatherMap)
def startMQTT():

    clear()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("127.0.0.1", 1883, 60)
    #client.connect("192.168.2.114", 1883, 60)

    global p2 
    p2 = multiprocessing.Process(target=weatherMap)
    p2.daemon = True

    client.loop_forever()


p1 = multiprocessing.Process(target=startMQTT)
p1.start()