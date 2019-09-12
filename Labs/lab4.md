## Lab 4: Robotların Birbirleriyle Haberleşmesi

Şimdiye kadar robotlarımız IoT Core'a kendi statuleri ve özellikleri ile ilgili MQTT mesajları iletiyorlar, iletilen mesajlara göre pil seviyesinin düşük olması durumunda Amazon SNS üzerinden operasyon birimine Eposta gönderiliyor, aynı zamanda tüm mesajlar ileride analiz edilmek üzere Amazon S3'de saklanıyordu. Bu aşamada ise robotlarımız (Robo1 ve Robo2) birbirleriyle haberleşmelerini sağlayacağız. Aslınd yapacağımız, her bir robotun diğerinin abone (Subscribe) olduğu IoT Topic'e mesaj iletmesi (publish) ile sağlanacak. Yani Pub/Sub modelini işleteceğiz. Göndereceğimiz mesajı robotların adına kendimiz elle  gireceğiz. 

Aşağıda bu lab'da oluşturup, kullanacağımız AWS kaynaklarını ve veri akışını görebilirsiniz.
 
![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab4.jpg)


**Robotların Mesajlaşması**



1. AWS Web Arayüzünden giriş yapın ve AWS Region olarak IRELAND (eu-west-1) seçili olduğundan emin olun. 

2. Sol üst köşedeki 'Services' menüsünden Cloud9 seçip, Cloud9 Dashboard'u açın. 

3. Ekranda kullandığınız IDE (**IoTRobotsIDE**) ortamını açmak için, Open IDE tıklayın.

4. _Environment_ ekranında **robo1** klasörünün üzerinde sağ tıklayın ve **New File** seçin.

5. Dosyanın adını **lab4.py** olarak değiştirin. Çift tıklayarak **lab4.py** dosyasını açın.

6. **lab4.py** dosyasının içine aşağıdaki dosyadaki kodu kopyalayın.

```
https://github.com/halilbahadir/aws-iot-robots/blob/master/Scripts/lab4/lab4.py

```

7. Dosyanın içinde **mqttClient.configureEndpoint("ENDPOINT BURAYA KOPYALANACAK",8883)** satırını bulup, tırnak işaretlerinin arasına **endpoint** adresini 'ENDPOINT BURAYA KOPYALANACAK' satırı yerine yapıştırın.

8. Aynı şekilde **robo2** içinde aynı işlemleri yapın.

9. _Environment_ ekranında **robo2** klasörünün üzerinde sağ tıklayın ve **New File** seçin.

10. Dosyanın adını **lab4.py** olarak değiştirin. Çift tıklayarak **lab4.py** dosyasını açın.

11. **lab4.py** dosyasının içine aşağıdaki dosyadaki kodu kopyalayın.

```
https://github.com/halilbahadir/aws-iot-robots/blob/master/Scripts/lab4/lab4.py

```

12. Dosyanın içinde **mqttClient.configureEndpoint("ENDPOINT BURAYA KOPYALANACAK",8883)** satırını bulup, tırnak işaretlerinin arasına **endpoint** adresini 'ENDPOINT BURAYA KOPYALANACAK' satırı yerine yapıştırın.

13. Kodu incelediğinizde, AWS IoT bağlandıktan sonra, robotların publish ve subscribe olacağı IoT Topic'lerini tanımlıyoruz (iot/mesaj/robo1 ve  iot/mesaj/robo2). Hangi robo olduğuna kod dosyasının bulunduğu klasör adından anlıyoruz. **onMessageCallback** methodu abone olunan (subscribe) IoT Topic'den alınan mesajı terminal konsoluna yazdırmayı sağlar. **subscribe** methodu IoT Topic'e abone olmayı (subscribe) **publish** methodu da IoT Topic'e mesaj iletmeyi sağlar. **raw_input** ile de terminalden mesaj girişi yapmanızı sağlar.

14. Her iki robo (robo1 ve robo2) klasörü altındaki **lab4.py** kodlarını çalıştırmak için iki tane terminal ekranına ihtiyacımız var. Cloud9 editöründe yeşil **+** işaretine tıklayın ve menüden **New Terminal** seçin.  Yeni terminal ekranı açılacaktır. Bir terminali orta bölümde, diğerini alt bölümde açılması takibi kolaylaştıracaktır.

15. Terminal alanında aşağıdaki komutları çalıştırın

``` 
cd robo1
python lab4.py

```

Ekranda aşağıdaki gibi mesaj görünecektir.

```
Mesajinizi Yaziniz iot/mesaj/robo2:

```

16. Diğer terminal alanında aşağıdaki komutları çalıştırın

``` 
cd robo2
python lab4.py

```

Ekranda aşağıdaki gibi mesaj görünecektir.

```
Mesajinizi Yaziniz iot/mesaj/robo1:

```

17. İlk terminal alanına geri dönüp ekrana **Merhaba** diye yazıp _enter_ basın.

18. Diğer terminal ekranında aşağıdaki çıktıyı göreceksiniz

```
Mesaj Alindi iot/mesaj/robo1: Merhaba
```

19. Aynı terminal ekranında gelen mesajın altına, **Sana da merhaba** yazıp _enter_ basın.

20. Diğer terminal ekranında aşağıdaki çıktıyı göreceksiniz

```
Mesaj Alindi iot/mesaj/robo2: Sana da merhaba
```

21. Her iki terminalde de uygulamayı durdurmak için **Ctrl+C** basınız. 


Tebrikler..!! Robotlar arasında mesaj gönderimini başarı ile tamamladınız.


