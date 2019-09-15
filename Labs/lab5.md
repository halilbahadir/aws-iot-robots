## Lab 5: AWS IoT GreenGrass


Not: AWS IoT GreenGrass için diğer LAB1 dışındaki diğer LAB'ları yapmak zorunda değilsiniz. 

Diğer Lab çalışmalarında olduğu gibi Robotlar (IoT Thing) doğrudan AWS bulut ortamındaki IoT Core servisinin Endpoint URL adresine gerekli sertifika ve yetki tanımlamaları ile erişebiliyorlar. AWS IoT Endpoint'e erişim için gerekli internet bağlantısının sürekli olduğu durumlarda, uç noktalar ile bulut veri merkezleri arasındaki network hızlarından dolayı gecikmelerin problem olmadığı durumlarda ya da tüm IoT mesajlarının işlenmeden (filtreleme, sadeleştirme, zenginleştirme vs.) IoT Servisine gönderilmesi gerektiği durumlarda bu yöntemi kullanmak anlamlı olabilir.  Fakat tersi durumlarda nasıl bir çözüm sağlayabiliriz. Örneğin tüm veriyi buluta göndermektense, uç noktada işleyip göndermek daha az anlamlı veri aktarımı yapmamızı sağlayabilir. AWS IoT servisleri içinde bu çözümü AWS IoT Greengrass servisi ile sağlamak mümkün.

Bu Lab çalışmasında Robotlar verilerini buluta AWS IoT Core'a göndermek yerine Greengrass Core'a gönderecekler. Yine aynı şekilde sertifika ve MQTT protokol kullanarak Greengrass Core'a bağlanacaklar fakat bağlantının yapılacağı endpoint ve Certificate Authority (CA), bizim örnek için Cloud9 ortamında kurulu olan Greengrass Core'un endpoint ve Certificate Authority (CA) olacak. 

Normal şartlarda Greengrass Core farklı bir sunucuda çalıştırılırken, bu lab kapsamında Robo1 ve Robo2 ile birlikte aynı sunucuda çalıştıracağız. Greengrass Core için x86 ya da ARM tabanlı işlemcisi olan endüstriyel sunucu ya da Raspberry Pi gibi cihazlar da kullanılabilir. IoT cihazlarının Greengrass Core'a network üzerinden nasıl bağlanacağını bulmak için Greengrass Discovery API kullanabilirsiniz, bu API ile Greengrass Core'a ait bütün IP/Port gibi bağlantı opsiyonlarına erişebilirsiniz.  

Yukarıda da bahsettiğimiz üzere uç noktalarda (Greengrass Core) toplanan veriyi, daha buluta (IoT Core) göndermeden işleyerek daha uygun bir yapıya getirmek mümkün. Bunun için AWS'in bir diğer servisinden yararlanacağız. Lambda (AWS Serverless Compute) servisini kullanarak uygulama geliştirip, IoT verilerini işleyeceğiz ve bunu AWS buluta gitmeden, uç noktada Greengrass üzerinde yapacağız. Bu noktada Lambda'nın uç noktada (bizim örnek için Cloud9) çalıştırılıyor olması ilginç gelebilir, fakat Greengrass üzerinde Lambda fonksiyonu çalıştırmayı sağlayan yapıyı barındırıyor. Bunun için AWS Lambda üzerinde geliştirdiğimiz ve veriyi işlemek için kullanacağımız kodu, Greengrass Core'a deploy edeceğiz.

Greengrass Core aynı IoT Core'da olduğu gibi pub/sub mantığı ile çalışır. Bu sebeple Greengrass Core'a gelecek veri akışını yönetmek için Publisher/Subscription konfigürasyonunu yapmak gerekiyor. Lab çalışması için Robo'lardan gelen veriyi, Greengrass üzerinde çalışan Lambda fonksiyonlarına göndermek için de pub/sub tanımlamalarına ihtiyacımız var. Sonrasında da Lambda fonksiyonu veriyi işleyip yine pub/sub ile bu sefer IoT Core'a veriyi gönderecek, yine burada da benzer bir konfigürasyon yapacağız. 

Yaptğımız konfigürasyon ve yazdığımız Lambda fonksiyonunun doğru çalışıp çalışmadığını denetlemek için de AWS IoT Core arayüzündeki AWS IoT MQTT Client kullanacağız. 



![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab5.jpg)




##Greengrass Konfigürasyonu##

**Greengrass Grubu Oluşturma**

Bu aşamada AWS IoT Core Web arayüzünü kullanarak, Greengrass için gerekli kaynakları oluşturmamızı sağlayacak Greengrass Grup oluşturacağız.


1. AWS Web Arayüzünden 'IoTRoboUser' kullanıcısı ile giriş yapın 

2. AWS Web arayüzünde üst menüden _Servises_ altından **IoT Greengrass** tıklayın (sorgu alanından yararlanabilirsiniz) 

3. AWS IoT Greengrass ana sayfasında, sağ üs köşeden AWS Region olarak "EU (Ireland)" seçildiğinden emin olun. IoT Greengrass sayfası IoT Core ile aynı arayüzde bulunur.

4. **Create a Group** butonuna tıklayın.

5. **Use easy creation** tıklayın. Böylece tek tek uğraşmadan, Greengrass Grup, Greengrass'ın etkileşimde olacağı diğer Lambda, IoT Core vs. servislere erişimi için gerekli IAM Role, Greengrass Core, Core için gerekli Key Pair ve Sertifika otomatik olarak oluşturulmuş olacak.

6. _Group Name_ alanına **IoTRoboGGGroup** yazın, _Next_ tıklayın.

7. _Group Core Name_ alanı otomatik olarak **IoTRoboGGGroup_Core** gelir, değiştirmeden _Next_ tıklayın.

8. **Create Group and Core** tıklayın. Böylece gerekli tüm aksiyonlar çalışıp, gerekli kaynakları yaratacak.

9. **Download these resources as a tar.gz** tıklayın ve dosyayı bilgisayarınıza kaydedin.

10. **Finish** tıklayın.

11. Oluşturduğumuz **IoTRoboGGGroup** _Greengrass Group_ sayfası açıldı. 

12. Ekranın solundaki menüden **Cores** tıklayın.

13. _IoTRoboGGGroup_ ile ilişkilendirilmiş **IoTRoboGGGroup_Core** Greengrass Core görebilirsiniz.

14. Menüden **Settings** tıklayın. 

15. _Settings_ ekranının sonuna doğru **CloudWatch logs configuration** bölümünde **Edit** tıklayın.

16. **Add Another Log Type** tıklayın ve her iki **User Lambdas (recommended)** ve **Greengrass system** işaretleyip **Update** butonuna tıklayın.

17. Log konfigürasyonu kadetmek için **Save** butonuna tıklayın.

18. Greengrass ekranından çıkıp, IoT Core sayfasına dönmek için ekranın sol üstündeki gri kutudaki ok --> işaretini tıklayın.

19. IoT Core sayfası menüsünden **Manage** tıklayın. 

20. IoT Thing listesine yeni bir **IoTRoboGGGroup_Core** adında Thing eklediğini görüyoruz. Zira Greengrass Core, IoT Core için diğer Robo'lar gibi IoT Thing olarak çalışıyor. 

21. Sayfadaki **IoTRoboGGGroup_Core** tıklayın.

22. Menüden **Security** seçin. 

23. Açılan _Security_ sayfasında _IoTRoboGGGroup_Core_ ilişkilendirilmiş **Sertifikayı** da görebilirsiniz.

24. Ekranda _sertifika_ tıklayın ve açılan sayfada **Policy** tıklayın.

25. Açılan _Policy_ sayfasında _IoTRoboGGGroup_Core_ ilişkilendirilmiş otomatik olarak kuralları belırlenmiş **Policy** de görebilirsiniz.

26. _Policy_ üzerinde tıklayın. **Policy Document** alanında detaylarını görebilirsiniz.

27. IoT Core ana sayfasına geri dönebilirsiniz.

Tebrikler!! Greengrass Group ve Greengrass Core başarı ile oluşturdunuz. 


**Greengrass Uç Nokta Ayarları (Cloud9)**

Bu aşamada, greengrass'ın kurulumu için Cloud9 konfigürasyonu yaparak, bir önceki aşamada indirdiğimiz _tar.gz_ kullanarak da Cloud9 üzerine Greengrass kurulumunu yapacağız.

1. Eğer, Cloud9 açık değilse, sol üst köşedeki 'Services' menüsünden Cloud9 seçip, Cloud9 Dashboard'u açın.

2. Ekranda kullandığınız IDE (IoTRobotsIDE) ortamını açmak için, Open IDE tıklayın.

3. **ggc_user** ve **ggc_group** kullanıcılarını Cloud9 sunucusuna tanımlayalım. Bu kullanıcıları Lambda fonksiyonları çalıştırmak için kullanacağız. Cloud9 terminal penceresinde aşağıdaki komutları çalıştırın.

```
sudo adduser --system ggc_user
sudo groupadd --system ggc_group

```

4. Greengrass, üzerinde çalıştığı sunucunun işletim sistemi ayarlarında hardlink ve softlink korumasını aktif hale getirmeyi gerektirir ki, güvenlik seviyesinin arttırılması için önemli bir değişikliktir. Bunun için aşağıdaki komutları Cloud9 terminal ekranında çalıştırın.

```
echo 'fs.protected_hardlinks = 1' | sudo tee -a /etc/sysctl.d/00-defaults.conf
echo 'fs.protected_symlinks = 1' | sudo tee -a /etc/sysctl.d/00-defaults.conf
sudo sysctl --system

```

5. AWs Iot Greengrass için gerekli olan Linux Control group (cgroups) komutlarını Cloud9 terminal ekranında çalıştırın.

```
cd /tmp
curl https://raw.githubusercontent.com/tianon/cgroupfs-mount/951c38ee8d802330454bdede20d85ec1c0f8d312/cgroupfs-mount > cgroupfs-mount.sh
chmod +x cgroupfs-mount.sh 
sudo bash ./cgroupfs-mount.sh
```

**Greengrass Yazılımının Kurulumu**

1. Greengrass yazılımını indirin ve sıkıştırma dosyasını açın. Bunun için aşağıdaki komutları Cloud9 terminal ekranında çalıştırın.


```
cd /tmp
wget https://d1onfpft10uf5o.cloudfront.net/greengrass-core/downloads/1.8.0/greengrass-linux-x86-64-1.8.0.tar.gz
sudo tar -xzf greengrass-linux-x86-64-1.8.0.tar.gz -C /

```

2. Bir önceki bölümde makinenize indirdiğiniz _tar.gz_  uzantılı dosyayı, Cloud9 sunucusuna yüklememiz gerekiyor. Bunun için Cloud9 Environment penceresinde en üst seviye klasör olan **IoTRobotsIDE** seçiniz.

3. Cloud9 Menüsünden **File** tıklayın, açılan listeden **Upload local files** seçin.

4. Açılan pencereden **Select Files** tıklayın ve makinenizdeki adı **..setup.tar.gz** ile biten dosyayı seçin.

5. Dosya yükleme penceresini kapatın. (X tıklayın)

6. **..setup.tar.gz** dosyasının içinde _Certificate_ ve _Private Key_ dosyalarını taşıyan _greengrass/certs_ klasörü ile IoT Core'a bağlanmak için gerekli bilgilerin bulunduğu _config.json_ dosyası taşıyan _greengrass/config_ klasörü bulunmakta. Sıkıştırılmış dosyayı açmak için aşağıdaki komutları Cloud9 terminal ekranında çalıştırın.

```
cd /tmp
mv ~/environment/*-setup.tar.gz setup.tar.gz
sudo tar -xzf setup.tar.gz -C /greengrass

```
7. Ayrıca _Root Certificate Authority_ dosyasını da _greengrass/certs_ klasörüne kopyalayalım. Bu dosya hali hazırda kullandığımız, _environment_ penceresinden de görebileceğiniz **root-CA.crt** dosyası. Aşağıdaki komutları Cloud9 terminal ekranında çalıştırın. Dosyanın adını _root.ca.pem_ olarak değiştirmemizin sebebi _config.json_ da tanımlı değer ile aynı olması gerektiği için. Dosya adını değiştirmek, _config.json_ içindeki değerideğiştirmekten daha kolay :)

```
cd /home/ec2-user/environment/
sudo cp root-CA.crt /greengrass/certs/root.ca.pem

```

Gerekli tüm konfigürasyonları tamamladık ve Greengrass kurulumunu Cloud9 üzerine yaptık. Şimdi Greengrass'ı çalıştırma zamanı.

**Greengrass Çalıştırma**

1. Aşağıdaki komutları Cloud9 terminal ekranında çalıştırın.


```
cd /greengrass/ggc/core/
sudo ./greengrassd start
```

Komutu çalıştırdıktan sonra aşağıdakine benzer bir çıktı gördüyseniz, Greengrass başarı ile çalışmış demektir.
 
```
Setting up greengrass daemon
Validating hardlink/softlink protection
Waiting for up to 40s for Daemon to start

Greengrass successfully started with PID: .....
```

Tebrikler, Greengrass'ı uç nokta sunucuda başarı ile çalıştırdınız..


** Greengrass Lambda Fonksiyonu Hazırlama**








