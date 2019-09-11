## Lab 3: AWS IoT Shadows


Bu Lab çalışmasında IoT Shadow kullanarak Robo1 (ya da Robo2) ile statü değerlerinde (özelliklerinde) uygulama ile değişiklik 
yapacağız. Senaryomuzda depo içinde görüntü olarak birbirinin aynısı yüzlerce Robo çalışıyor olacağı için, operatorler herhangi bir robota ulaşmak için onun lokasyonunu kullanacaklardır, ayrıca gerektiğinde hızla robutu bulmak için roboların üzerinde bulunan mavi ışığı yakmayı sağlayabiliriz, bunu bir mobil uygulama kullanarak yapabiliriz ama bu lab'da kolaylık olması açısından AWS IoT Core içindeki IoT MQTT Client kullanacağız. 
Işığı yakıp söndürmek için her bir robot üzerinde REST API talebi dinleyen minik bir web sunucu çalıştırıp sağlayabiliriz, fakat bu pil ömrü ve verimliliği için hiç uygun olmayacaktır. Bunun yerine AWS IoT servisini, aracı olarak kullanıp ışığı açıp kapatmayı sağlayabiliriz.  

Ya da daha önceki lab'da olduğu gibi IoT Topic kullanabiliriz, fakat bu durumda da mesajlar kısa ömürlü oldukları için, Robotlar sürekli bağlı olmak zorundalar. Eğer herhangi bir bağlantı kopması durumunda, o sırada eğer ışığı açıp-kapama mesajı gelirse Robotlar bunu hiç bilemeyebilir. IoT Thing'lerin sürekli bağlantıda olması çoğu zaman efektif bir çözüm olmayabilir, özellikle yeterli enerji yoksa ya da enerji tüketimini azaltma ihtiyacı varsa. 

Bu durumda önerilen çözüm IoT Thing Shadow. Shadow, IoT servisi içindeki robotların statülerini temsil eden bir fonksiyon sağlar. İstemciler, doğrudan IoT Thing'le iletişim kurmak yerine, Shadow ile iletişim kurup, Thing (Robotlar) bağlantısı kopsa bile statüleri güncelleyebilirler, Thing tekrar bağlandığında Shadow üzerindeki son statü değişikliğini alıp, gerekli güncellemeyi kendi üzerinde yapar. Bu sayede front-end ile (bizim örnekte AWS Console, fakat herhangi bir uygulama da olur, mobil, web vs.) back-end ile ayrıştırabiliriz (decoupling). İster doğrudan AWS IoT Thing ile ister AWS IoT Thing Shadow kullanalım, her durumda IoT Topic üzerinde çalıştığımız için, her türlü MQTT İstemci Thing Shadow ile de çalışabilir.

![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab3.jpg)



**Thin Shadow Tanımlama - 1**

Bu bölümde, Robolar Shadow'larını oluşturup, shadow'lar üzerinden statü değişikliği ve okuması yapacağız. Cloud9 üzerinden bir script kullanarak bu değişklikleri sağlayacağız, aynı zamanda AWS Web arayüzü üzerinden de IoT Shadow statülerini de takip edebileceğiz.


1. Sol üst köşedeki 'Services' menüsünden Cloud9 seçip, Cloud9 Dashboard'u açın.

2. Ekranda kullandığınız IDE (**IoTRobotsIDE**) ortamını açmak için, Open IDE tıklayın.

3. Environment penceresi üzerinde, _Robo1_ klasörünü seçip sağ tıklayın ve **New File** seçin.

4. Yeni oluşturulan dosyanın adını **lab3-1.py** olarak değiştirin.

5. **lab3-1.py** dosyası üzerinde çift tıklayın ve dosyayı açın.

6. Aşağıdaki kod parçasını kopyalayıp, **lab3-1.py** dosyası içine yapıştırın.

```
KOD BURAYA GELECEK..

```

7. Dosyanın içinde  * *shadowClient.configureEndpoint("ENDPOINT BURAYA KOPYALANACAK",8883)* * satırını bulup, tırnak işaretlerinin arasına kopyaladığınız **endpoint** adresini 'ENDPOINT BURAYA KOPYALANACAK' satırı yerine yapıştırın. 

8. Dosyayi kaydedin. Menüde File/Save tıklayın ya da (Ctrl+S) ya da (Cmd+S) 

9. Bu aşamada yaptığımız, bir shadow objesi oluşturup, o obje üzerinden bir shadow mesajı yayınlamak.

10. Bu Cloud9 sekmesi açık kalsın, şimdi başka bir browser sekmesinde IoT Core üzerinden IoT Thing Shadow izleyelim.


 **Thin Shadow Client (AWS Web Arayüz)**
 
 1. Eğer Cloud9 Dashboardunda iseniz, ekranın üstündeki Cloud9 menüsünün sol üst köşedeki **AWS Cloud9** tıklayıp açılan menüde 'Go to Your Dashboard' seçin. Yeni bir browser sekmesinde AWS Cloud9 Dashboard'u açılacaktır. 

2. AWS Cloud Dashboard'da üst menüden 'Services' tıklayıp, açılan servis listesinde **AWS IoT Core** seçin. Sorgu alanına 'IoT Core' yazarak listeyi filtreleyebilirsiniz.

3.  AWS IoT Core Dashboard açılacaktır. Sol üst köşeden AWS Region IRELAND seçili olduğuna emin olun, değilse de listeden EU  (ireland) seçin.

4. Ekranın sol tarafındaki menüden **Manage / Things** tıklayın.

5. Ekranda _Robo1_ ve _Robo2_  IoT Thing'leri göreceksiniz. 

6. **Robo1** tıklayın. Açılan ekranın sol tarafındaki menüden **Shadow** seçin. Daha önce herhangi bir shadow oluşturmadığımız için burada Shadow dokümanı yok. 

7. Bu ekran açık kalsın. Şimdi tekrar diğer sekmedeki Cloud9 ekranına geri gelelim. 

**Thin Shadow Tanımlama - 2**

1. Cloud9 Editöründe **Terminal** penceresinde aşağıdaki komutu çalıştırın. 

```
cd robo1
python lab3-1.py

```

2. Aşağıdaki mesajları terminale yazdıracaktır.

```
RoboName--> robo1
Baglandi
Shadow Guncelleme Gonderildi
Baglandi Kesildi
REQUEST TIME OUT

```

3. IoT Core açık olduğu Browser sekmesine geçin. Sayfayı yeniden yükleyin (refresh). Sol menüden **Showdow** tıklayın.

4. Bu sefer ekranda Shadow dokümanını göreceksiniz.

```
Shadow state:

{
  "desired": {
    "headLight": "On"
  },
  "delta": {
    "headLight": "On"
  }
}

```

Ayrıca Metadata alanında ('Timestamp' değerleri sizde kodun çalıştırma zamanından dolayı farklı olacaktır.)

```
Metadata:
{
  "metadata": {
    "desired": {
      "headLight": {
        "timestamp": 1568206689
      }
    }
  },
  "timestamp": 1568206704,
  "version": 13
}

```

5. IoT Core sekmesi açık kalsın. Tekrar geri döneceğiz. 


**Thin Shadow Değişkliğini İzleme - 1**

Bu bölümde AWS IoT shadow arayüzünden yaptığımız değişikliği, kod üzerinden takip edebilmek.  

1. Environment penceresi üzerinde, _Robo1_ klasörünü seçip sağ tıklayın ve **New File** seçin.

2. Yeni oluşturulan dosyanın adını **lab3-2.py** olarak değiştirin.

3. **lab3-2.py** dosyası üzerinde çift tıklayın ve dosyayı açın.

4. Aşağıdaki kod parçasını kopyalayıp, **lab3-2.py** dosyası içine yapıştırın.

```
KOD BURAYA GELECEK..

```

5. Dosyanın içinde  * *shadowClient.configureEndpoint("ENDPOINT BURAYA KOPYALANACAK",8883)* * satırını bulup, tırnak işaretlerinin arasına kopyaladığınız **endpoint** adresini 'ENDPOINT BURAYA KOPYALANACAK' satırı yerine yapıştırın. 

6. Dosyayi kaydedin. Menüde File/Save tıklayın ya da (Ctrl+S) ya da (Cmd+S) 

7. _Terminal_ ekranından aşağıdaki komutları çalıştırın. 


```
cd robo1
python lab3-2.py

```
8. Aşağıdaki mesajları terminale yazdıracaktır.

```
RoboName--> robo1
Connected
Listening for Delta Messages

```

9. Çalışan uygulama Shadow objesini dinliyor ve herhangi bir statü değişikliğinde ekrana Delta mesajını yazmak üzere bekliyor.

10. Browserda açık olan IoT Core sekmesine geçelim.

11. Eğer sayfayı değiştirmediyseniz en son **Robo1** IoT Thing detay sayfasında **Shadow** ekranında kalmıştık. Eğer sayfada değilseniz; AWS IoT Core Dashboard açın, sol üst köşeden AWS Region IRELAND seçili olduğuna emin olun, değilse de listeden EU  (ireland) seçin. Ekranın sol tarafındaki menüden **Manage / Things** tıklayın. Ekranda **Robo1** tıklayın. Açılan ekranın sol tarafındaki menüden **Shadow** tıklayın. 

12. Ekranda _Robo1_ için en son oluşturulan Shadow dokümanını görebilirsiniz.

13. _Shadow Document_ başlığının en solunda yer alan **Edit** butonuna tıklayın.

14. _Shadow State_ alanı editör haline aldığı için, doküman üzerinde değişiklik yapabiliriz. 

15. Desired State alanını ON durumundan OFF durumuna getirmek için aşağıdaki değişikliği yapın ya da tümğnğ kopyalayıp, mevcutu silerek kopyalayın.

```
{
  "desired": {
    "headLight": "Off"
  },
  "delta": {
    "headLight": "On"
  }
}

```

16. **Save** tıklayın.

17. **Shadow State** güncellendi. Güncellenme ile ilgili bilgini etkisini, çalıştırdığımız **lab3-2.py** terminalinden görebiliriz.

18. Browser'da Cloud9'un açık olduğu sekmeye geçip, daha önce çalıştırdığımız kodun _terminal_ deki çıktısına bakalım.

```
{"version":15,"timestamp":1568223725,"state":{"headLight":"OFF"},"metadata":{"headLight":{"timestamp":1568223725}}}

```
19. Shadow Objesinde yaptığımız değişiklik, IoT Topic üzerine atandı. IoT Thing bağlandığı durumda güncellemeyi üzerine yansıtacaktır.

Tebrikler IoT Thing Shadow adımını da tamamladınız.

