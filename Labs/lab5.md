## Lab 5: AWS IoT GreenGrass


Not: AWS IoT GreenGrass için diğer LAB'ları yapmak zorunda değilsiniz. Sadece senaryo bütünlüğü ve daha kolay anlaşılması açısında LAB 1'i yapmanızı tavsiye ederim.

Diğer Lab çalışmalarında olduğu gibi Robotlar (IoT Thing) doğrudan AWS bulut ortamındaki IoT Core servisinin Endpoint URL adresine gerekli sertifika ve yetki tanımlamaları ile erişebiliyorlar. AWS IoT Endpoint'e erişim için gerekli internet bağlantısının sürekli olduğu durumlarda, uç noktalar ile bulut veri merkezleri arasındaki network hızlarından dolayı gecikmelerin problem olmadığı durumlarda ya da tüm IoT mesajlarının işlenmeden (filtreleme, sadeleştirme, zenginleştirme vs.) IoT Servisine gönderilmesi gerektiği durumlarda bu yöntemi kullanmak anlamlı olabilir.  Fakat tersi durumlarda nasıl bir çözüm sağlayabiliriz. Örneğin tüm veriyi buluta göndermektense, uç noktada işleyip göndermek daha az anlamlı veri aktarımı yapmamızı sağlayabilir. AWS IoT servisleri içinde bu çözümü AWS IoT Greengrass servisi ile sağlamak mümkün.

Bu Lab çalışmasında Robotlar verilerini buluta AWS IoT Core'a göndermek yerine Greengrass Core'a gönderecekler. Yine aynı şekilde sertifika ve MQTT protokol kullanarak Greengrass Core'a bağlanacaklar fakat bağlantının yapılacağı endpoint ve Certificate Authority (CA), bizim örnek için Cloud9 ortamında kurulu olan Greengrass Core'un endpoint ve Certificate Authority (CA) olacak. 

Normal şartlarda Greengrass Core farklı bir sunucuda çalıştırılırken, bu lab kapsamında Robo1 ve Robo2 ile birlikte aynı sunucuda çalıştıracağız. Greengrass Core için x86 ya da ARM tabanlı işlemcisi olan endüstriyel sunucu ya da Raspberry Pi gibi cihazlar da kullanılabilir. IoT cihazlarının Greengrass Core'a network üzerinden nasıl bağlanacağını bulmak için Greengrass Discovery API kullanabilirsiniz, bu API ile Greengrass Core'a ait bütün IP/Port gibi bağlantı opsiyonlarına erişebilirsiniz.  

Yukarıda da bahsettiğimiz üzere uç noktalarda (Greengrass Core) toplanan veriyi, daha buluta (IoT Core) göndermeden işleyerek daha uygun bir yapıya getirmek mümkün. Bunun için AWS'in bir diğer servisinden yararlanacağız. Lambda (AWS Serverless Compute) servisini kullanarak uygulama geliştirip, IoT verilerini işleyeceğiz ve bunu AWS buluta gitmeden, uç noktada Greengrass üzerinde yapacağız. Bu noktada Lambda'nın uç noktada (bizim örnek için Cloud9) çalıştırılıyor olması ilginç gelebilir, fakat Greengrass üzerinde Lambda fonksiyonu çalıştırmayı sağlayan yapıyı barındırıyor. Bunun için AWS Lambda üzerinde geliştirdiğimiz ve veriyi işlemek için kullanacağımız kodu, Greengrass Core'a deploy edeceğiz.

Greengrass Core aynı IoT Core'da olduğu gibi pub/sub mantığı ile çalışır. Bu sebeple Greengrass Core'a gelecek veri akışını yönetmek için Publisher/Subscription konfigürasyonunu yapmak gerekiyor. Lab çalışması için Robo'lardan gelen veriyi, Greengrass üzerinde çalışan Lambda fonksiyonlarına göndermek için de pub/sub tanımlamalarına ihtiyacımız var. Sonrasında da Lambda fonksiyonu veriyi işleyip yine pub/sub ile bu sefer IoT Core'a veriyi gönderecek, yine burada da benzer bir konfigürasyon yapacağız. 

Yaptğımız konfigürasyon ve yazdığımız Lambda fonksiyonunun doğru çalışıp çalışmadığını denetlemek için de AWS IoT Core arayüzündeki AWS IoT MQTT Client kullanacağız. 


![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab5.jpg)





