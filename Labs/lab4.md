## Lab 4: Robotların Birbirleriyle Haberleşmesi

Şimdiye kadar robotlarımız IoT Core'a kendi statuleri ve özellikleri ile ilgili MQTT mesajları iletiyorlar, iletilen mesajlara göre pil seviyesinin düşük olması durumunda Amazon SNS üzerinden operasyon birimine Eposta gönderiliyor, aynı zamanda tüm mesajlar ileride analiz edilmek üzere Amazon S3'de saklanıyordu. Bu aşamada ise robotlarımız (Robo1 ve Robo2) birbirleriyle haberleşmelerini sağlayacağız. Aslınd yapacağımız, her bir robotun diğerinin abone (Subscribe) olduğu IoT Topic'e mesaj iletmesi (publish) ile sağlanacak. Yani Pub/Sub modelini işleteceğiz. Göndereceğimiz mesajı robotların adına kendimiz elle  gireceğiz. 

Aşağıda bu lab'da oluşturup, kullanacağımız AWS kaynaklarını ve veri akışını görebilirsiniz.
 
![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab4.jpg)


**Robotların Mesajlaşması**



1. AWS Web Arayüzünden giriş yapın ve AWS Region olarak IRELAND (eu-west-1) seçili olduğundan emin olun. 

2. Sol üst köşedeki 'Services' menüsünden Cloud9 seçip, Cloud9 Dashboard'u açın. 

3. Ekranda kullandığınız IDE (**IoTRobotsIDE**) ortamını açmak için, Open IDE tıklayın.

4. _Environment
