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

17. Log konfigürasyonu kaydetmek için **Save** butonuna tıklayın.

18. _Settings_ ekranının sonuna doğru **Local logs configuration** bölümünde **Edit** tıklayın.

19. **Add Another Log Type** tıklayın ve her iki **User Lambdas (recommended)** ve **Greengrass system** işaretleyip **Update** butonuna tıklayın.

20. Log konfigürasyonu kaydetmek için **Save** butonuna tıklayın.

21. _Settings_ ekranının en üstünde yer alan **Group Role** bölümünde **Add Role** tıklayın.

22. Açılan ekranda **Greengrass_ServiceRole** rolünü seçin. **Save** tıklayın. 


23. Greengrass ekranından çıkıp, IoT Core sayfasına dönmek için ekranın sol üstündeki gri kutudaki ok --> işaretini tıklayın.

24. IoT Core sayfası menüsünden **Manage** tıklayın. 

25. IoT Thing listesine yeni bir **IoTRoboGGGroup_Core** adında Thing eklediğini görüyoruz. Zira Greengrass Core, IoT Core için diğer Robo'lar gibi IoT Thing olarak çalışıyor. 

26. Sayfadaki **IoTRoboGGGroup_Core** tıklayın.

27. Menüden **Security** seçin. 

28. Açılan _Security_ sayfasında _IoTRoboGGGroup_Core_ ilişkilendirilmiş **Sertifikayı** da görebilirsiniz.

29. Ekranda _sertifika_ tıklayın ve açılan sayfada **Policy** tıklayın.

30. Açılan _Policy_ sayfasında _IoTRoboGGGroup_Core_ ilişkilendirilmiş otomatik olarak kuralları belırlenmiş **Policy** de görebilirsiniz.

31. _Policy_ üzerinde tıklayın. **Policy Document** alanında detaylarını görebilirsiniz.

32. IoT Core ana sayfasına geri dönebilirsiniz.

Tebrikler!! Greengrass Group ve Greengrass Core başarı ile oluşturdunuz. 



**Greengrass_ServiceRole IAM Rolüne yetki verme**

1. AWS Web arayüzünde üst menüden _Servises_ altından **IAM** tıklayın (sorgu alanından yararlanabilirsiniz) 

2. Sol menüden **Roles** tıklayın.

3. _Roles_ listesinden **Greengrass_ServiceRole** bulup, tıklayın. (_Search_ alanına 'Greengrass_ServiceRole' yazarak filtereleyebilirsiniz)

4. _Greengrass_ServiceRole_ detay sayfasında _permissions_ tabında **Attach Policies** tıklayın.

5. _Filtre_ alanında **CloudWatchLogsFullAccess** yazınız. Filtrelenmis policy listesinden **CloudWatchLogsFullAccess** işaretleyip, **Attach Policy** tıklayın.

6. _Greengrass_ServiceRole_ ait policy listesine eklendiğini görebilirsiniz.



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


**Greengrass Lambda Fonksiyonu Hazırlama**

Bu bölümde Greengrass Core'a gelen verilerin işlenmesinde kullanacağımız Lambda fonksiyonu geliştirip, bunu Greengrass'ın bulunduğu uç nokta sunucuya (Cloud9) yükleyeceğiz.

1. Cloud9 arayüzünde sol üst köşedeki AWS Cloud9 tıklayın. Açılan menüde Go to your dashboard seçin. Yeni browser sekmesinde Cloud9 web arayüzü açılacaktır.

2. Üst menüden Services tıklayın. Açılan menüden Compute grubundan **Lambda** seçin.

3. AWS Lambda web arayüzü açılacaktır. Ekranda **Create a function** butonuna tıklayın.

4. **Author from scratch** ile sıfırdan bir fonksiyon geliştirebilirsiniz. Lambda fonksiyonları için hazır oluşturulmuş şablonları kullanabilirsiniz (Use a blueprint) ya da kendi uygulama kütüphanesinden mevcut fonksiyonları kullanabilirsiniz (Browse Serverless App Repository)

5. _Function Name_ alanına **IoTRobotsGGLambda** yazın.

6. _Runtime_ için **Python 2.7** seçin. Bunun dışında bir çok farklı dil destekliyor ayrıca siz kendi Runtime ortamınızı getirebiliyorsunuz.

7. _Permissions_ alanı altında **choose or create an execution role** tıklayıp, diğer giriş alanlarına ulaşın.

8. **Create a new role with basic Lambda permissions** seçin. Burada oluşturulan rol aslında greengrass senaryomuz için kullanılmayacak, çünkü biz Lambda fonksiyonunu bulutta değil, uç noktada bulunan Greengrass Core üzerinde çalıştıracağız. 

9. **Create Function** butonuna tıklayın ve Lamba fonksiyonu ve IAM Rolünün oluşturulmasını bekleyin.

10. Geliştirilen Lambda fonksiyonu için Greengrass Python kütüphanesine de ihtiyaç olacak ki, oraaki fonksiyonları da kullanabilelim. Bunun için hazırladığım kodu indirebilirsiniz (https://github.com/halilbahadir/aws-iot-robots/blob/master/Scripts/lab5/lab5-IoTRobotsGGLambda.zip)

11. _Function Code_ bölümünde _Code Entry Type_ alanında **Upload a .zip file** seçin. 

12. **Upload** butonuna tıklayın. Bir önceki adımda indirdiğiniz **lab5-IoTRobotsGGLambda.zip** dosyasını seçip. _Open_ butonuna tıklayın.

13. _Upload_ butonu yanında yüklenecek dosyanın ismi görünecektir.

14. _Handler_ alanındaki yazıyı silip **IoTRobotsGGLambda.lambda_handler** yazın.

14. Ekranın sol üst köşesindeki turuncu renkli **Save** butonuna tıklayın.

15. Kayıt sonrasında, kod editörü ekranında Lambda fonksiyonunu görebilirsiniz. Kodu incelediğinizde; fonksiyondaki lambda_handler methodu, Robo1 ve Robo2'den **iot/robots**'e publish edilen mesajları, Lambda yine aynı Topic'e subscribe olarak okuyacak ve bu mesajları AWS bulut üzerindeki **iot/gg/robots** IoT Topic'e publish edecek şekilde geliştirildi. Kod üzerinde değişiklik yaparak gelen mesajları işleyebilirsiniz.

16. Lambda arayüzünde **Actions** butonı tıklayın, açılan menüde **Publish New version** seçin.

17. Açılan pencerede _version description_ alanına **1** yazın. ve **Publish** tıklayın.

**Robotların ve Lambda'nın Aboneliklerini (Subscription) Tanımlama**

Lab'ın bu adımında daha önce Lab1'de oluşturduğumuz Robo1 ve Robo2 IoT Thing'leri ile bir önceki adımda oluşturduğumuz Lambda fonksiyonu Greengrass Group (IoTRoboGGGroup) ekleyeceğiz ve sonrasında uç noktadaki sunucuya (Cloud9) deploy edeceğiz. 

Ayrıca Robo1 ve Robo2'nin **iot/robots** gönderdikleri mesajların Lambda fonksiyona aktarılması, be Lambda fonksiyonuna gelen mesajlarında IoT Core üzerindeki **iot/gg/robots**  aktarılması için gerekli aboneliklerin (Subscription) tanımlanmasını yapacağız.

1. AWS Web arayüzünde üst menüden _Servises_ altından **IoT Greengrass** tıklayın (sorgu alanından yararlanabilirsiniz) 

2. AWS IoT Greengrass ana sayfasında, sağ üs köşeden AWS Region olarak "EU (Ireland)" seçildiğinden emin olun. IoT Greengrass sayfası IoT Core ile aynı arayüzde bulunur.

3. Sol menüden **Groups** tıklayın 

4. Açılan ekranda Greengrass grupları listelenecektir **IoTRoboGGGroup** tıklayın. 

5. Açılan Greengrass Group ekranında menüden **Devices** seçin. 

6. **Add Device** butonuna tıklayın.

7. **Select an IoT Thing** tıklayın.

8. Açılan Listeden **Robo1** seçin ve **Finish tıklayın.

9. Aynı şekilde **Robo2** içinde 5.adımdan başlayarak **Robo2** IoT Thing greengrass grubuna ekleyin.

10. _Devices_ ekranında Robo1 ve Robo2'nin eklendiğini görebilirsiniz.

11. Greengrass Group ekranında menüden **Lambdas** tıklayın.

12. **Add Lambda** butonuna tıklayın.

13. **Use existing Lambda** tıklayın.

14. Açılan ekranda **IoTRobotsGGLambda** seçin ve **Next** tıklayın.

15. Lambda fonksiyonu versiyonu olarak **Version 1** seçin ve **Finish** tıklayın.

16. _Lambdas_ ekranında eklediniz **IoTRobotsGGLambda** fonksiyonunu görebilirsiniz.

17. Açılan Greengrass Group ekranında menüden **Subscriptions** seçin.

18. **Add Subscription** butonuna tıklayın.

19. **Select a Source** alanında **Select** tıklayın.

20. **Devices** tıklayın ve listeden **Robo1** seçin.

21. **Select a Target** alanında **Select** tıklayın.

22. **Lambdas** tıklayın ve listeden **IoTRobotsGGLambda** seçin.

23. **Next** tıklayın.

24. **Topic filter** alanına **iot/robots** yazın.

25. **Next** tıklayın.

26. **Finish** tıklayın.

27. Aynı şekilde **Robo2** --> **IoTRobotsGGLambda** olacak şekilde **iot/robots** topic tanımlayın (18.adımdan 26. adıma kadar tekrarlayın)

28.  Aynı şekilde  **IoTRobotsGGLambda** (Source)--> **IoT Cloud** (Target) olacak şekilde **iot/gg/robots** topic tanımlayın (18.adımdan 26. adıma kadar tekrarlayın)

29. Bütün hepsini ekledikten sonra _Subscriptions_ ekranında 3 tane tanım göreceksiniz.  


Tebrikler!! Greengrass Grup ve Subscription tanımlarını başarı ile bitirdiniz..


**Konfigürasyon ve Lambda Fonksiyonu Greengrass Core'a Yükleme**

Bır önceki bölümde yaptığımız konfigürasyon tanımlarını AWS bulut üzerinde IoT Greengrass servisi üzerinde yaptık, Lambda fonksiyonunu da yine AWS bulut üzerinde Lambda servisi üzerine yükledik (geliştirdik). Şimdi bu konfigürasyon ve Lambda fonksiyonlarını uç noktadaki Greengrass Core'a yükleyeceğiz.

1. Greengrass Group ekranında sol üst köşede **Actions** tıklayın, açılan menüde **Deploy** tıklayın.

2. İlk _deployment_ olduğu için yetki tanımlamamız gerekiyor. Tüm Greengrass grupları için sadece bir kere yapılacak bir işlem. Açılan ekranda **Grant permissions** butonuna tıklayın.

3. Greengrass grubuna eklediğimiz _device'ların_ (Robo1, Robo2) Greengrass Core'u otomatik olarak bulup erişebilmeleri için **Automatic Detection** butonuna tıklayın. Bu Greengrass Discovery Service kullanarak sağlanacak. Bunun için sonraki adımlarda device için yazdığımız kodlarda ufak bir ekleme yapacağız.

4. Greengrass Deployment başlattığına dair bir pop-up mesajı görünecektir.

5. Deployment başarı ile tamamlandığında GreenGrass Group adının (IoTRoboGGGroup) altında yeşil bir ikon yanında **Successfully completed** yazıldığını görebilirsiniz. 

6. Sol menüde **Deployments** tıklayın. _Deployment History Review_ listesinde başarılı / başarısız olmuş deploymentları görebilirsiniz.

7. Deployment'da hata almanız durumunda listenin en solunde yer alan üç nokta tıklayıp, **re-deploy** ile tekrar yükleme başlatabilirsiniz. 2. adımda _grant access_ dedikten sonra AWS IAM servisinde oluşturulan yeni rolün tanımlanması bitmeden yükleme başlattığınızda hata alabilirsiniz. Bu lab sırasında sıkça karşılaştığımız bir hata, bu durumda 30 sn kadar bekleyip sonra tekrar yükleme (re-deploy) yapın.




1. 










