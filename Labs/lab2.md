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



