## Lab 5: AWS IoT GreenGrass


Not: AWS IoT GreenGrass için diğer LAB'ları yapmak zorunda değilsiniz. Sadece senaryo bütünlüğü ve daha kolay anlaşılması açısında LAB 1, yapmanızı tavsiye ederim.

Diğer Lab çalışmalarında olduğu gibi Robotlar (IoT Thing) doğrudan AWS bulut ortamındaki IoT Core servisinin Endpoint URL adresine gerekli sertifika ve yetki tanımlamaları ile erişebiliyorlar. AWS IoT Endpoint'e erişim için gerekli internet bağlantısının sürekli olduğu durumlarda, uç noktalar ile bulut veri merkezleri arasındaki network hızlarından dolayı gecikmelerin problem olmadığı durumlarda ya da tüm IoT mesajlarının işlenmeden (filtreleme, sadeleştirme, zenginleştirme vs.) IoT Servisine gönderilmesi gerektiği durumlarda bu yöntemi kullanmak anlamlı olabilir.  Fakat tersi durumlarda nasıl bir çözüm sağlayabiliriz. Örneğin tüm veriyi buluta göndermektense, uç noktada işleyip göndermek daha az anlamlı veri aktarımı yapmamızı sağlayabilir. AWS IoT servisleri içinde bu çözümü AWS IoT Greengrass servisi ile sağlamak mümkün.

Bu Lab çalışmasında Robotlar verilerini buluta AWS IoT Core'a göndermek yerine Greengrass Core'a gönderecekler. Yine aynı şekilde sertifika ve MQTT protokol kullanarak Greengrass Core'a bağlanacaklar fakat bağlantının yapılacağı endpoint ve Certificate Authority (CA), bizim örnek için Cloud9 ortamında kurulu olan Greengrass Core'un endpoint ve Certificate Authority (CA) olacak. 

şş

Although in this case, Greengrass Core will be running in the same server as Car1 and Car2, they would normally be separate. For the devices to know how to connect to Greengrass Core within the network, you can use the Greengrass Discovery API which will return all the different connectivity options (IP and Port) of your Greengrass Core.

To do processing of the data, you will use a Lambda function that you will deploy on your Greengrass Core. That's right, Lambda will be running on your server (your Cloud9 environment). In this case, the Lambda function will simply take the data that is sent by each of the devices (on the edx/telemetry Topic) and re-publish it to a different IoT Topic: edx/greengrass/telemetry.

You will configure Subscriptions within your Greengrass Core to manage how the data is flowing. By default, there is no data that can go anywhere, even between the devices connected on your Greengrass Core. To allow that, Subscriptions are made to say what the data flow should be. In this case, you will configure that all the telemetry data sent by the Cars should be sent to your Lambda function running on Greengrass Core and that the data re-published by that Lambda function should be sent to the AWS IoT Cloud.

Finally, you will be able to subscribe to the IoT Topic that your Lambda function is publishing to (edx/greengrass/telemetry) using the AWS IoT MQTT Client in the AWS Management Console to validate the flow of the data.
