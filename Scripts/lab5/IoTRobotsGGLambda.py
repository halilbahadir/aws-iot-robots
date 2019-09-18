
import greengrasssdk
import platform
import time
import json

# GreenGrass IoT Client tanimlama
client = greengrasssdk.client('iot-data')


def function_handler(event, context):
    eventText = json.dumps(event)
    eventStr = json.loads(eventText)
    batteryValue=eventStr['battery']
    if batteryValue <= 10:
        print(eventStr)
    #Greengrass Core dan gelen EVENT bilgisi Robotlarin gonderdigi mesaji tasiyor. Bunu aynen iletiyoruz.
    #Burada veriyi isleyip gondermekte mumkun. Burada batter seviyesi 10 altinda ise gonderiyoruz ornegin.
    
        client.publish(
            topic='iot/gg/robots',
            payload=json.dumps(event)
        )
        
    time.sleep(5)
    return
