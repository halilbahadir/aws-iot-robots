#!/usr/bin/python

# Lab 1
# AWS Region Ireland olduguna emin olun.

import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import os 
import random

#MQTT Istemci olusturma ve guvenlik sertifikalarini tanimlama
#Sertifa isimleri ile AWS IoT Thing indirdiginiz sertifika isimlerinin ayni olmasina dikkat edin.

currentPath=os.getcwd()
roboName=os.path.basename(currentPath)
latitude = 0
longtitude = 0
battery = 100
isBusy = 'false'
ID= 10000
print("RoboName--> "+roboName)

mqttClient = AWSIoTMQTTClient(roboName)

#Ayarlar sayfasindaki IoTEndpoint buraya ekleyin
mqttClient.configureEndpoint("ENDPOINT BURAYA KOPYALANACAK",8883)
mqttClient.configureCredentials("../root-CA.crt","PrivateKey.pem","certificate.pem.crt")

#JSON formatina encode eden fonksiyon
def toJSON(string):
        return json.dumps(string)

mqttClient.toJSON=toJSON

#Degiskenleri ve MQTT mesaji tanimlari
message ={
  'roboName': roboName,
  'latitude': random.uniform(-90.0,+90.0),
  'longtitude': random.uniform(-180.0,+180.0),
  'battery': random.randint(1,101),
  'isBusy': random.randint(0,1),
  'ID': random.randint(10000,100000)
}

#Mesaji JSON yap
#message = mqttClient.toJSON(randomRoboGenerator())

#Test mesajini IoT Topic'e gonder
def send():
    message = mqttClient.toJSON(randomRoboGenerator())
    mqttClient.publish("iot/robots", message, 0)
    print ("Mesaj Gonderildi")


def randomRoboGenerator():
    message ={
        'roboName': roboName,
        'latitude': random.uniform(-90.0,+90.0),
        'longtitude': random.uniform(-180.0,+180.0),
        'battery': random.randint(1,100),
        'isBusy': random.randint(0,1),
        'ID': random.randint(10000,99999)
    }
    return message


#iot gateway baglan
mqttClient.connect()
print ("IoT Core Baglandi")

#Sonlandirana kadar mesaj gondermeye 5 sn.de bir devam et
while True:
    send()
    time.sleep(5)

mqttClient.disconnect()
