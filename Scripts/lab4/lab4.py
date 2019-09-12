import sys
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import os 


currentPath=os.getcwd()
senderRobo=os.path.basename(currentPath)

# Set the destinationDeviceName depending on this deviceName
if senderRobo == 'robo1':
    receiverRobo = 'robo2'
else:
    receiverRobo = 'robo1'
    
print(receiverRobo)
mqttClient = AWSIoTMQTTClient(senderRobo)

#Ayarlar sayfasindaki IoTEndpoint buraya ekleyin
mqttClient.configureEndpoint("ENDPOINT BURAYA GELECEK",8883)
mqttClient.configureCredentials("../root-CA.crt","PrivateKey.pem","certificate.pem.crt")

mqttClient.connect()

# Publish ve Subscription Topic'lerinin tanımlanması, ornegin iot/mesaj/robo1 topic'lerden birisi olacak
subscriptionTopic = 'iot/mesaj/' + senderRobo
publishTopic = 'iot/mesaj/' + receiverRobo


def onMessageCallback(client, userdata, message):
    print("Mesaj Alindi " + message.topic + ": " + message.payload)

# Abone olunan Topic'ten mesaj okuma
mqttClient.subscribe(subscriptionTopic, 1, onMessageCallback)

# Topic'e mesaj iletme
def publishToIoTTopic(topic, payload):
    mqttClient.publish(topic, payload, 1)


while True:
    message = raw_input('Mesajinizi Yaziniz ' + publishTopic + ':\r\n')
    publishToIoTTopic(publishTopic, message)
