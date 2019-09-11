#!/usr/bin/python

# Lab 3-2
# AWS Region Ireland olduguna emin olun.

import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json
import time
import os 
import random

#MQTT Shadow Istemci olusturma ve guvenlik sertifikalarini tanimlama
#Sertifa isimleri ile AWS IoT Thing indirdiginiz sertifika isimlerinin ayni olmasina dikkat edin.

currentPath=os.getcwd()
roboName=os.path.basename(currentPath)
print("RoboName--> "+roboName)

shadowClient=AWSIoTMQTTShadowClient(roboName)

#Ayarlar sayfasindaki IoTEndpoint buraya ekleyin
shadowClient.configureEndpoint("ENDPOINT BURAYA KOPYALANACAK",8883)
shadowClient.configureCredentials("../root-CA.crt","PrivateKey.pem","certificate.pem.crt")

shadowClientHandler=shadowClient.createShadowHandlerWithName("Robo1",True) # Robo1 Thing adi olarak statik tanimli, parametre de olabilir.
#JSON formatina encode eden fonksiyon
def toJSON(string):
        return json.dumps(string)

shadowClient.toJSON=toJSON

#Function to encode a payload into JSON
def json_encode(string):
        return json.dumps(string)

shadowClient.json_encode=json_encode
shadowClientHandler.json_encode=json_encode

def on_message(message, response, token):
    print (message)

shadowClient.on_message = on_message
shadowClientHandler.on_message= on_message

shadowClient.connect()
print ("Baglandi")
shadowClientHandler.shadowRegisterDeltaCallback(on_message) #Delta degerini okuyan method.
print ("Delta Mesajlarini Dinliyorum")

# Sonsuz Dongu
while True:
        pass
