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


**IoT Rule Tanımlama**

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


