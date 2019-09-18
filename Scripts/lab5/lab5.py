#!/usr/bin/python

# Lab 5
# AWS Region Ireland olduguna emin olun.

import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.core.greengrass.discovery.providers import DiscoveryInfoProvider
from AWSIoTPythonSDK.core.protocol.connection.cores import ProgressiveBackOffCore
from AWSIoTPythonSDK.exception.AWSIoTExceptions import DiscoveryInvalidRequestException
import json
import time
import os 
import random
import uuid

#MQTT Istemci olusturma ve guvenlik sertifikalarini tanimlama
#Sertifa isimleri ile AWS IoT Thing indirdiginiz sertifika isimlerinin ayni olmasina dikkat edin.


currentPath=os.getcwd()
roboName=os.path.basename(currentPath)
print(roboName)
roboName=roboName.capitalize()
latitude = 0
longtitude = 0
battery = 100
isBusy = 'false'
ID= 10000
headLight="Off"
print("RoboName--> "+roboName)

GROUP_CA_PATH = "./groupCA/"


#discoveryEndpoint ="https://greengrass-ats.iot.eu-west-1.amazonaws.com:8443/greengrass/discover/thing/"+roboName

discoveryEndpoint="a100y3wur4j1gq-ats.iot.eu-west-1.amazonaws.com"


rootCAPath= "../root-CA.crt"
privateKeyPath="PrivateKey.pem"
certificatePath="certificate.pem.crt"

discoveryInfoProvider = DiscoveryInfoProvider()
discoveryInfoProvider.configureEndpoint(discoveryEndpoint)
discoveryInfoProvider.configureCredentials(rootCAPath,certificatePath,privateKeyPath)

groupCA = None
coreInfo = None

try:
    discoveryInfo = discoveryInfoProvider.discover(roboName)
    caList = discoveryInfo.getAllCas()
    coreList = discoveryInfo.getAllCores()
    
    # We only pick the first ca and core info
    groupId, ca = caList[0]
    coreInfo = coreList[0]
    groupCA = GROUP_CA_PATH + groupId + "_CA_" + str(uuid.uuid4()) + ".crt"
    print("GROUP_CA -->" + groupCA)
    if not os.path.exists(GROUP_CA_PATH):
        os.makedirs(GROUP_CA_PATH)
    groupCAFile = open(groupCA, "w")
    groupCAFile.write(ca)
    groupCAFile.close()
    
    
except DiscoveryInvalidRequestException as e:
    print("Yanil discovery istegi geldi!")
    print("Tip: %s" % str(type(e)))
    print("Hata Mesaji: %s" % e.message)
    print("Sonlandiriliyor...")
    
except BaseException as e:
    print("Discovery Hatasi!")
    print("Tip: %s" % str(type(e)))
    print("Hata Mesaji: %s" % e.message)


#groupCA = "/greengrass/certs/28032a2a10.cert.pem"

# Iterate through all connection options for the core and use the first successful one
mqttClient = AWSIoTMQTTClient(roboName)
mqttClient.configureCredentials(groupCA,"PrivateKey.pem","certificate.pem.crt")



#for connectivityInfo in coreInfo.connectivityInfoList:
#    currentHost = connectivityInfo.host
#    currentPort = connectivityInfo.port
#    print("Trying to connect to core at %s:%d" % (currentHost, currentPort))
currentHost ="172.31.31.189"
currentPort ="8883"

mqttClient.configureEndpoint(currentHost,currentPort)
try:
    mqttClient.connect()
    connected = True
#    break
except BaseException as e:
    print("Baglanti Hatasi!")
    print("Tip: %s" % str(type(e)))
    print("Hata Mesaji: %s" % e.message)


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
  'isBusy': random.randint(0,2),
  'headLight':"Off",
  'ID': random.randint(10000,100000)
}


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
        'headLight':"Off",
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
