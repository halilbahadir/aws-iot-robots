## Lab 2: AWS IoT Rules 

  
  Bu lab çalışmasında, robotlardan herhangi birinin pil seviyesinin %10'un altına düştüğü durumda operatörlere eposta gönderilmesini tetikleyen bir kural tanımlayacağız. Bunun için öncelikle bir SNS (Simple Notification Service) Topic oluşturup ve SNS Topic'e bır eposta adresi ile abone (subscribe) olacağız. Öncelikle IoT Servisinin, SNS Topic'e mesaj yayınlaması (publish) için yetki vermemiz gerekiyor. Sonrasında da SNS Topic'e gelen mesajlar üzerinde SQL Sorgusu kullanarak pil seviyesini kontrol eden bir IoT Rule tanımlayacağız.  
 
 Amazon Simple Notification Service (SNS) servisi, dağıtık sistemleri ve serverless uygulamaları birbirinden ayırmanıza imkan tanıyan yüksek oranda erişilebilir, sağlam, güvenli ve tam olarak yönetilen bir pub/sub mesajlaşma hizmetidir. SNS ayrıca, son kullanıcılara mobil anlık bildirimler, SMS ve e-posta yollarıyla bildirim dağıtılması için kullanılabilir. 
  
  Bu lab çalışmasında aşağıdaki mimari ve akışı gerçekleştireceğiz.

![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab2.png)


### Amazon SNS (Amazon Simple Notification Service)

**SNS Topic Tanımlama**

Bu bölümde SNS Topic tanımlayıp, bır eposta adresi kullanarak o SNS Topic'e abone olup, abonelik için eposta adresine gelen epostadaki linki kullanıp onay vereceğiz.

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.


1. AWS Web Arayüzünden giriş yapın ve AWS Region olarak IRELAND (eu-west-1) seçili olduğundan emin olun.

2. Sol üst köşedeki 'Services'menüsünden SNS seçip, SNS Dashboard'u açın.

3. Açılan ekranın sol üst tarafındaki hamburger menüden (3 tane çizgi üst üste) Topics tıklayın.

4. _Create Topic_ butonuna tıklayın.

5. 'Topic Name' alanına *IoTBatteryTopic* yazın.

6. _Create Topic_ butonuna tıklayın. SNS Topic oluşturuldu.

7. Bir eposta adresi ile yeni oluşturulan **IoTBatteryTopic** SNS Topic'e abone olmak için _Create Subscription_ butonuna tıklayın

8. 'Protocol' alanında **Email** seçin.

9. 'Endpoint' alanına mesajlarını görmeye yetkiniz olan bir eposta adresi giriniz.

10. **Create Subscription** butonuna tıklayın. Eposta adresi ile **IoTBatteryTopic** SNS Topic'e abone oldunuz.

11. Bir kaç dakika içinde abone olduğunuz eposta adresine _AWS Notification - Subscription Confirmation_ konulu _no- reply@sns.amazonaws.com_ adresinden bir eposta gelecek. O epostayı açıp içindeki **Confirm Subscription** linkine tıklayın. Açılan web sayfasında, sizin abonelik kaydınızı onayladığınızı görebilirsiniz. (**Subscription Confirmed**)

12. Hamburger menüdeki listeden bu sefer **Subscriptions** tıklayın. Açılan ekranda, abonelik bilgilerini görebilirsiniz. 

SNS Topic oluşturup, eposta adresinizle SNS Topic aboneliğini başarı ile tamamladınız.!!!


**IAM Rolü Tanımlama**

Bir önceki bölümde tanımladığımız SNS Topic'e  AWS IoT servislerinden mesaj yayınlamak (publish) için yetki tanımlamamız gerekiyor. AWS üzerinde bir servisin, bir diğer servisi kullanabilmesi için yetkiye ihtiyacı olacaktır. Bu aynı bizim Lab'larda kullandığımız **IoTRoboUser** kullancısının (IAM User) servisleri kullanabilmek için yetkiye (policy) ihtiyaç duyması gibidir. Bir AWS Servisinin diğer bir servisi kullanabilmesini sağlamak için **IAM Role** özelliğini kullanacağız. Bu aşamada yeni bir AWS IAM Rolü tanımlayacağız, bu IAM Rol _iot.amazonaws.com_ servis öğesi ile 'Trust Relationship' kurmalı ve aynı zamanda SNS Topic'e mesaj yayınlama (publish) yetkisine (IAM Policy) sahip olmalıdır.

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.

**VIDEO**

1. AWS Web Arayüzünden giriş yapın ve AWS Region olarak IRELAND (eu-west-1) seçili olduğundan emin olun.

2. Sol üst köşedeki 'Services' menüsünden IAM (Identity and Access Management) seçip, IAM Dashboard'u açın.

3. Sol taraftaki listeden **Roles** seçin.

4. **Create Role** butonuna tıklayın.

5. Açılan pencerede Trusted Entity olarak **AWS Service** seçin.

6. Bu rolü kullanacak servis olarak (_Choose the service that will use this role_) **IoT** seçin.

7. Kullanılacak use case için (_Select your use case_) **IoT** seçin.

8. **Next: Permissions**  tıklayın.

9. İlk sayfadaki IoT seçimlerimizden dolayı bazı IAM Policy'ler tanımlı olarak geldi. Bizim Lab 2'de kullanacağımız senaryo için seçili gelenlerden **AWSIoTRuleActions** ve detayındaki **sns:Publish** tanımı işimizi görecektir. 

10. **Next: Tag** tıklayın.

11. **Next: Review** tıklayın.

12. _Role Name_ alanına **IoTRobotsRole** yazın.

13. **Create Role** butonuna tıklayın. Role oluşturuldu..

Tebrikler.!!! Bir sonraki adımda kullanacağımız IAM Rolü başarı ile oluşturuldu.


**IoT Rule Tanımlama (SNS)**

Bu bölümde, Roboların pillerinin %10 altına düştüğü durumları takip eden bir SQL sorgusunu kullanan IoT Rule tanımlayacağız. Eğer bu durumda olan bir robo varsa, ilk bölümde oluşturduğumuz SNS Topic'e mesaj publish edeceğiz.

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.


1. AWS Web Arayüzünden giriş yapın ve AWS Region olarak IRELAND (eu-west-1) seçili olduğundan emin olun.

2. Sol üst köşedeki 'Services' menüsünden IoT Core seçip, IoT Core Dashboard'u açın.

3. IoT Core Rule tanımlamak için sol menüden **Act** tıklayın.

4. **Create Rule** butonuna tıklayın.

5. _Name_ alanına **BatteryRule** yazın.

6. _Set one or more actions_ altındaki **Add Action** butonuna tıklayın.

7. Listeden **Send a message as an SNS push notification** seçin.

8. Listenin en altındaki **Configure Action** butonuna tıklayın.

9. Açılan konfigürasyon sayfasında, _SNS Target_ alanında **Select** tıklayın.

10. **IoTBatteryTopic** en sağında yer alan **Select** tıklayın.

11. _Message Format_ alanında **Raw** seçin.

12. _Choose or create a role to grant AWS IoT access to perform this action_ alanında **Select** tıklayın

13. Listeden **IoTRobotsRole** en sağında yer alan **Select** tıklayın.

14. **Add Action** butonuna tıklayın. SNS Action tanımı IoT Rule'a eklendi.

15. _Rule query statement_ alanındaki siyah kutunun içine imleci götürün ve tıklayın. Böylece bu alana SQL sorgusu yazabileceğiz. 

16. SQL Sorgu alanına aşağıdaki sorguyu yazın.

```
SELECT 
  roboName + ' pil seviyesi şu an ' + battery + ' seviyesinde, pili şarj etmek gerekiyor. ' +  roboName + ' şu an '  + latitude + ' ve '  + longtitude + ' koodrinatlarında bulunuyor.' AS batteryQ
FROM 'iot/robots'
WHERE
 battery < 10   

```

Bu sorguda **iot/robots** IoT Topic'deki (ki Lab 1 de oluşturmuştuk) **battery** parametresinin değerini sorgulayıp, eğer değer 10'un altına düşerse Robo'nun adını, pil seviyesini ve bulunduğu koordinatları döndüreceğiz. 

17. **Create Rule** butonuna tıklayın. 

Tebrikler.. IoT Rule başarı ile tanımlandı..

### Amazon S3 (Amazon Simple Storage Service)

İlk tanımladığımız IoT Rule ile Robo'ların pil seviyesinde %10 altına düşme durumu olduğunda _gerçek zamanda_, son kullanıcılara (fabrikadaki operatörler) eposta gönderen bir kural tanımladık. 

Bu aşamada da ise IoT Core'a gelen MQTT mesajları üzerinde sonraki aşamalarda kullanabileceğimiz _batch_ analiz çalışması yapabilmek için gelen tüm mesajları AWS S3 üzerinde saklamak için gerekli IoT Rule tanımlayalım.

Bu lab çalışmasında aşağıdaki mimari ve akışı gerçekleştireceğiz.

![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab2-s3.jpg)


Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.


1. AWS Web Arayüzünden giriş yapın ve AWS Region olarak IRELAND (eu-west-1) seçili olduğundan emin olun.

2. Sol üst köşedeki 'Services' menüsünden S3 seçip, S3 Dashboard'u açın.

3. **Create Bucket** butonuna tıklayın.

4. _Bucket Name_ alanına DNS uyumlu bir S3 bucket ismi gerektiği için  'adınızın soyadınızın bas harfleri' ile birlikte **-iot-robo-messages** yazın. Örneğin benim için **hb-iot-robo-messages** 

5. _Region_ olarak **EU(Ireland)**

6. Next..Next..Next.. **Create Bucket** butonlarına tıklayın.

7. S3 bucket listesinde yeni oluşturduğunuz bucket'ı göreceksiniz.

Tebrikler!! S3 Bucket başarı ile oluşturdunuz.

**IoT Rule Tanımlama (S3)**

Bu bölümde, Roboların tüm gönderdiği mesajları (SQL sorgusu ile) alan IoT Rule tanımlayacağız ve bu mesajları S3'e kaydedeceğiz. Sonrasında bu verileri analiz için kullanabiliriz.

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.


1. AWS Web Arayüzünden giriş yapın ve AWS Region olarak IRELAND (eu-west-1) seçili olduğundan emin olun.

2. Sol üst köşedeki 'Services' menüsünden IoT Core seçip, IoT Core Dashboard'u açın.

3. IoT Core Rule tanımlamak için sol menüden **Act** tıklayın.

4. Sağ üstteki **Create** butonuna tıklayın.

5. _Name_ alanına **AllMsgToS3** yazın.

6. _Set one or more actions_ altındaki **Add Action** butonuna tıklayın.

7. Listeden **Store a message in an Amazon S3 bucket** seçin.

8. Listenin en altındaki **Configure Action** butonuna tıklayın.

9. _S3 Bucket_ listesinden bir önceki bölümde oluşturduğunuz S3 bucket seçiniz. Benim senaryoda **hb-iot-robo-messages** seçiyorum. 

10. _Key_ alanına  **${topic()}/${timestamp()}** girin. Bu alana değişken bir değer vermemiz gerekiyor ki her mesaj farklı dosya olarak kaydedilsin, yoksa statik isim verirsek aynı dosyanın üzere yazar ve eski mesajları kaybedersiniz. Bu sebeple ?_Topic_ alanına IoT Topic ismi geliyor olacak ki S3'e klasör olarak eklenecek. _timestamp_ ise mesajın tarihi, bu da tekilliği sağlayacak.
 
11. _Choose or create a role to grant AWS IoT access to perform this action_ alanında **Select** tıklayın

12. Listeden **IoTRobotsRole** en sağında yer alan **Select** tıklayın.

13. **Add Action** butonuna tıklayın. S3 Action tanımı IoT Rule'a eklendi.

14. _Rule query statement_ alanındaki siyah kutunun içine imleci götürün ve tıklayın. Böylece bu alana SQL sorgusu yazabileceğiz. 

15. SQL Sorgu alanına aşağıdaki sorguyu yazın.

```
SELECT * as AllMsgQ
FROM 'iot/robots'   

```

16. **Create Rule** butonuna tıklayın. 

Tebrikler.. IoT Rule başarı ile tanımlandı..



**Roboları Çalıştırma**

Bu bölümde, robotları Cloud9 üzerinden aktif hale getirip, 5 sn'de bir IoT Core'a MQTT mesajı göndermesini sağlayacağız. Bunun için gerekli kodu zaten Lab 1'de hazırlamıştık. Bu aşamada sadece kodları çalıştırmamız yeterli.


1. Sol üst köşedeki 'Services' menüsünden Cloud9 seçip, Cloud9 Dashboard'u açın.

2. Ekranda kullandığınız IDE (**IoTRobotsIDE**) ortamını açmak için, Open IDE tıklayın.

3. Cloud9 IDE'de ekranın alt tarafındaki 'Terminal' penceresinde aşağıdaki komutları çalıştırın.

```
cd robo1
python lab1.py

```
4. Aşağıdaki gibi bir çıktı göreceksiniz.

```
RoboName--> robo1
IoT Core Baglandi
Mesaj Gonderildi
```

5. Kod içinde random olusturulan pil durumu, lokasyon için koordinatlar, robotun o an meşgul olup olmadığı gibi değerler IoT Core'a MQTT mesajı olarak iletiliyor.

Eğer random üretilen pil değeri %10 altında ise IoT Rule tanımı ile SNS üzerinden eposta alıyor olacaksınız. Aynı zamanda her bir MQTT mesajı S3 üzerinde bir dosyaya yazılıp saklanıyor olacak. 

6. Sol üst köşedeki 'Services' menüsünden S3 seçip, S3 Dashboard'u açın.

18.  _S3 Bucket_ listesinden bir önceki bölümde oluşturduğunuz S3 bucket tıklayın. Benim senaryoda **hb-iot-robo-messages** 

19. **iot** klasörü tıklayın.. **robots** tıklayın.. _robots_ klasörü altında IoT Mesajlarının kaydedildiği dosyaları göreceksiniz. Sağ üst köşede EU (Ireland) yanında yer alan _güncelle_ butonuna tıklayıp, klasörün içini güncelleyebilirsiniz.

 **iot/robots** IoT Topic adı. Herbir dosyanın adı da mesajın geldiği zaman.
 
 20. Dosyalardan birinin üzerinde tıklayın. Açılan ekranda **Download** butonuna tıklayıp, dosyayı bilgisayarınıza indirin.
 
 21. Dosyayı herhangi bir text editörü ile açtığınızda, aşağıdakine benzer bir bilgiyi göreceksiniz.
 
 ```
 {"AllMsgQ":{"battery":72,"longtitude":-138.80774898211118,"roboName":"robo1","latitude":-35.654477328777986,"isBusy":0,"ID":37611}}
 
 ```
 
 **AllMsq** SQL Sorgusuna verdiğimiz isim. Diğer alanlar ise Robo1 adındaki robotun o andaki durumu ile ilgili bilgiler. 
 
 
 




