#author= Christian Huppertz

import paho.mqtt.client as mqtt
import strip as st
import logging

class main:
    #Create logging module
    logging.basicConfig(filename='WS2812Controller.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d.%m.%y %I:%M:%S %p')
    logging.info('Main programm started')

    strip = st.strip(177, 18)

    def on_connect(client, userdata, flags, rc):
        logging.info("Mqtt connection established - " +str(rc))
        print("Connectet")
        
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("zimmer/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        strip.clear()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    #client.connect("127.0.0.1", 1883, 60) #local setup
    client.connect("192.168.2.114", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

mqqt_start = main()