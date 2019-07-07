## Lab 1: Robotların IoT Core'a Bağlanması

  Bu lab çalışmasında 2 tane robot (Thing) oluşturup, bu robotları AWS IoT Core servisi ile bağlantısını kuracağız. Böylelikle Robot'lar IoT Core'daki IoT Topic'lerine data gönderebilecekler. Bu bağlantıyı güvenli bir şekilde sağlayabilmek için Robot (Thing), politika (policy) ve sertifika (certification) oluşturmamız gerekecek. Sertifika kimlik doğrulama için kullanılırken, politika ise kimlik doğrulaması alan robotun ne yapmaya yetkilendirildiğini tarifleyecek.
  Birinici robotu AWS web konsoldan, ikincisini ise komut satırından.
  
  Tabi elimizde gerçek robotlar olmadığı için :smile: simülasyonu Amazon Cloud9 kullanarak gerçekleştireceğiz. Fakat sonraki lab'larda Rasberry Pi bizim robotlarımız olacak. 
 
 Aşağıda bu lab'da oluşturup, kullanacağımız AWS kaynaklarını ve veri akışını görebilirsiniz.
 
![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab1.jpg)


### A. AWS Kullanıcı Oluşturma

AWS Hesabı açtıktan sonra hesabınıza tüm yetkilere sahip, 'Root User' ile giriş yaptınız. Fakat 'root user' projelerde kullanılması tavsiye edilmez, onun yerine AWS IAM (Identity Access Management) servisini kullanarak, projeleriniz için hesabınıza farklı yetkilere sahip yeni kullanıcılar tanımlanabilir. Kullanıcılara da yetki politikaları (IAM Policy) tanımlanabilir. 

**Policy Tanımlama**
Öncelikle yeni oluşturacağımız kullanıcıya vereceğimiz yetkileri tanımlayalım. Diğer lab'lara geçtikçe aşağıda oluşturduğumuz policy'yi güncelleyerek yeni yetkiler de ekleyeceğiz. 

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.

[![AWS IoT Robots](http://img.youtube.com/vi/MBD8bsIcbkE/0.jpg)](http://www.youtube.com/watch?v=MBD8bsIcbkE "AWS IoT Robots Workshop")

1. AWS Web Arayüzünden giriş yapın ve IAM servisi ana sayfasına (dashboard) geçin.

2. IAM servisi ana sayfasındaki sol tarafta bulunan menüden "Policies" tıklayın.

3. "Create Policy" butonuna tıklayın.

4. JSON sekmesine tıklayarak geçin.

5. Editör kutusundaki yazıları silip, aşağıdaki policy'i kopyalayıp kutuya yapıştırın. 

6. "Review Policy" tıklayın.

7. Name alanına **iotRobotsPolicy** yazıp

8. "Create Policy" tıklayın.


```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:*",
        "cloud9:*",
        "iam:*",
        "logs:*",
        "ec2:*",
        "cloudwatch:*",
        "greengrass:*",
        "tag:getResources"
        ],
      "Resource": "*"
    }
  ] 
}

```

Tebrikler..!! Policy'yi başarı ile tanımladınız.


**Yeni Kullanıcı Oluşturma ve Kullanıcı Yetkilendirme**

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.

[![AWS IoT Robots](http://img.youtube.com/vi/l9C80KwI7TE/0.jpg)](http://www.youtube.com/watch?v=l9C80KwI7TE "AWS IoT Robots Workshop")

1. IAM ana sayfasına geçin.

2. IAM servisi ana sayfasındaki sol tarafta bulunan menüden "Users" tıklayın.

3. "Add User" butonuna tıklayın.

4. User Name alanına **IoTRoboUser** yazın.

5. Access Type alanından ise sadece **AWS Management Console access** seçin.

6. "Next: Permissions" butonuna tıklayın.

7. Yeni sayfadan "Attach Existing Policies Directly" yazan kutuya tıklayın.

8. "Filter Policies" alanına **iotRobotsPolicy** yazıp, filtrelenen liste alanından daha önce oluşturduğumuz policy'yi seçin.

9. "Next: Tags" butonuna tıklayın.

10."Next: Review" butonuna tıklayın.

11. Tüm yaptığınız girişlerin doğruluğundan emin olduktan sonra "Create User" butonuna tıklayın.

12. Tablodaki password alanındakı 'Show' linkine tıklayın ve görüntülenen şifrenizi bir yere kaydedin. Ya da "Download .csv" butonu tıklayrak, tablodaki bilgileri indirebilirsiniz.

13. "Close" butonu tıklayın. 


Tebrikler..!! Yeni Kullanıcıyı başarı ile oluşturdunuz.


**Yeni Kullanıcı ile AWS Login Olma**

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.

[![AWS IoT Robots](http://img.youtube.com/vi/7_JVVkLa2RU/0.jpg)](http://www.youtube.com/watch?v=7_JVVkLa2RU "AWS IoT Robots Workshop")

IAM Ana sayfasındaki sol taraftaki menüden "Dashboard" tıklayın, ve sayfanın en üstünde bulunan 'IAM users sign-in link:' de https://.. ile başlayan linki kopyalayıp browser'da yeni sekmede sayfayı açın.  Yeni kullanıcı adınız ve şifrenizi kullanarak sisteme giriş yapın. İlk defa yeni kullanıcı ile giriş yaptığınız için şifre değişikliği sayfası açılacaktır. O sayfadan yeni şifrenizi tanımlamanız gerekecektir. Bu örnek için şifre kuralları eklemedim fakat, yeni oluşturacağınız şifrenin kaç karakterden oluşması gerektiği, hangi tip karakterden kaçar tane kullanmanız gerektiği, şifrenin geçerlilik periyodu gibi değerleri şifreleme kuralı olarak tanımlayıp, o kurala uygun şifre oluşturmak zorunlu hale getirilebilir. 

Tebrikler..!! Yeni Kullanıcınız ile sisteme giriş yaptınız. Şimdi biraz IoT servisinin kullanalım.



**AWS Cloud9 Ortamı Oluşturma**

AWS Cloud9, bulut tabanlı çalışan, herhangi bir kurulum yapmadan doğrudan browser üzerinde kod geliştirme, debug yapma ve kodu çalıştırma yapabileceğiniz bir yazılım geliştirme aracıdır (IDE). Cloud9 içinde kod editörü, debugger ve komut satır arayüz terminali bulunmaktadır.

AWS Cloud9 ortamı IoT Thing olarak tanımlanacak ve robotlarımızı simüle edecektir. 

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.

[![AWS IoT Robots](http://img.youtube.com/vi/woDrWD7bSTM/0.jpg)](http://www.youtube.com/watch?v=woDrWD7bSTM "AWS IoT Robots Workshop")

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.

1. AWS Web Arayüzünden 'IoTRoboUser' kullanıcısı ile giriş yapın ve Cloud9 servisi ana sayfasına (dashboard) geçin.

2. Sağ üs köşeden AWS Region olarak **"EU (Ireland)"** seçildiğinden emin olun.

3. Cloud9 Dashboard ekranında turuncu "Create Environment" butonuna tıklayın.

4. Name alanına **IoTRobotsIDE** yazın. Sonrasında "Next Step" butonuna tıklayın.

5. "Configuration Settings" ekraninda, mevcut değerleri (minimum gerekleri sağlayacak değerler işimizi görecektir) değiştirmeden "Next Step" butonuna tıklayın. 'Cost Saving Setting' alanında 30 dakika olarak atanan değer, sizin Cloud9 ortamını 30 dk kullanmadığınız durumda otomatik olarak uyku moduna geçmesine sebep olur. Bu durumda herhangi bir o anki durum kaydedilir, tekrar çalıştırdığınızda kaldığınız yerde devam edebilirsiniz. 

6. Onay sayfasında, Cloud9 IDE kullanırken önerilen en iyi pratiklere göz atmakta fayda var. Sonrasında "Create Environment" butonuna tıklayın.


**Cloud9 Ortamının Konfigürasyonu**

Öncelikle Cloud9 ortamına Python için IoT SDK kurulumu yapmamız gerekecek. Kurulum ile ilgili detayları ve son versiyonlarları linkten ulaşabilirsiniz: https://github.com/aws/aws-iot-device-sdk-python

1. Aşağıda alternatif kurulum yöntemleri için gerekli açıklama ve komutları bulabilirsiniz. Komutları çalıştırmak için AWS Cloud9 **Terminal** kullanacağız. AWS Cloud9 IDE ekranında, **_bash_** tab'ında **iotRoboUser:~/environment: $** alanına komutları yazabilirsiniz. 

1.1. PIP ile kurulum

```
pip install AWSIoTPythonSDK
```

1.2. ya da alternatif olarak, kaynak kodu derleyerek kurulum

```
git clone https://github.com/aws/aws-iot-device-sdk-python.git
cd aws-iot-device-sdk-python
python setup.py install
```
1.3. ya da bir diğer alternatif, zip dosyası olarak kurulum dosyalarını indirerek kurulum. Bunun için dosyayı [buradan](https://s3.amazonaws.com/aws-iot-device-sdk-python/aws-iot-device-sdk-python-latest.zip) indirip, zip dosyasını açtıktan sonra, aşağıdaki komutu çalıştırarak kurulum yapabilirsiniz.

```
python setup.py install
```

2. AWS Cloud9 IDE klasör yapısını oluşturalım ki, scriptleri, sertifika dosyalarını kolay yönetebilelim. Cloud9 ortamında 2 tane robot'u (Robo1 ve Robo2) koşturacağız. O yüzden her bir robot için ayrı klasör yapısı oluşturacağız.

```
mkdir ~/environment/robo1; 
mkdir ~/environment/robo2
```
3. Yeni klasörleri sol taraftaki 'Environment' penceresinde görebilirsiniz. Robo'ları AWS IoT Core'a bağlanıp MQTT mesajlarını gönderebilmeleri için küçük bir Python (desteklenen diğer [diller](https://docs.aws.amazon.com/iot/latest/developerguide/iot-sdks.html)) koduna ihtiyacım olacak.
Bunun için _Robo1_ klasörü üzerinde sağ tıklayıp, 'New File' seçin. Dosya. klasörün altında görülecektir. Dosyanın ismini **lab1.py** olarak değiştirin.


4. Dosya seçip, çift tıklayın. **lab1.py** dosyası ana ekranda açıldı. Aşağıdaki kodu dosyanın içine kopyalayıp, dosyayı kaydedin. (Ctrl+S ya da Command+S ya da ACW Cloud9 menüsünden File/Save)

```python
KOD GELECEK..

```

5. Aynı işlemi _Robo2_ içinde yapın. (3. ve 4. adımları tekrarlayın. Robo2 klasörünü kullanacağız).

6. Sonraki adımlarda AWS IoT Core'da oluşturacağımız 'Thing'lerin (yani robotlar) IoT Sertifikalarını imzalamak için Sertifika Otoritesinden (CA) _public certificate_ ihtiyacımız olacak. Bunun için AWS IoT Certicate Authority Public Certicate dosyasını aşağıdaki linkten indirebilirsiniz. (Önerilen)     


```
cd ~/environment
wget -O root-CA.crt https://www.amazontrust.com/repository/AmazonRootCA1.pem
```

Alternatif olarak şu [link](https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem) diğer bir CA olan Verisign sertifikasını da kullanabilirsiniz. (Eski yöntem)

```
cd ~/environment
wget -O root-CA.crt https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem
```

7. Sonucunda aşağıdaki klasör yapısına sahip olacağız. <EKRAN GORUNTUSU>
  
**AWS Web Arayüzünden IoT Thing Oluşturulması - Robo1 **

Bu bölümde AWS IoT Core servini kullanarak AWS Web Arayüzünden IoT Thing, sertifika ve yetki politikasını oluşturacağız. Web arayüzü kullanarak manuel yöntemlerle IoT Thing yaratmak basit olsa da, IoT Thing sayısının yüzbinler binler, milyonlar mertebesinde olduğu durumlarda çok da basit olmayacaktır. O durumlarda [AWS IoT Device Management](https://aws.amazon.com/iot-device-management/) servisinin kullanılması uygun olacaktır. Bu aşamada Robo1 için Web Arayüzünü, Robp2 için ise CLI Komut satırını kullanarak tanımlamaları yapacağız. Sonrasında AWS IoT Core üzerinde herbir robot için oluşturduğumuz sertifika ve politikaları AWS Cloud9'a (Robotların simülatörü göreviyle) yükleyeceğiz.

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.

[![AWS IoT Robots](http://img.youtube.com/vi/SPHsCvtAwMk/0.jpg)](http://www.youtube.com/watch?v=SPHsCvtAwMk "AWS IoT Robots Workshop")

1. Eğer Cloud9 Dashboardunda iseniz, ekranın üstündeki Cloud9 menüsünün sol üst köşedeki **AWS Cloud9** tıklayıp açılan menüde 'Go to Your Dashboard' seçin. Yeni bir browser sekmesinde AWS Cloud9 Dashboard'u açılacaktır. 

2. AWS Cloud Dashboard'da üst menüden 'Services' tıklayıp, açılan servis listesinde **AWS IoT Core** seçin. Sorgu alanına 'IoT Core' yazarak listeyi filtreleyebilirsiniz.

3.  AWS IoT Core Dashboard açılacaktır. Sol üst köşeden AWS Region IRELAND seçili olduğuna emin olun, değilse de listeden EU  (ireland) seçin.

4. 'Get Started' tıklayın

5. Sol taraftaki menüden **Manage** tıklayın.

6. Sayfanın ortasındaki **Register a thing** butonunu tıklayın.

7. Sayfadaki **Create a single thing** butonlarından herhangi birini tıklayın.

8. 'Name' alanına **Robo1** yazın (Diğer alanlar mevcut değerlerinde kalabilir.), ve **Next** tıklayın.

9. Sertifika oluşturma işlemi için, 'One-click certificate creation (recommended)' opsiyonu ile hızla oluşturup, IoT Thing (Robo1) ile ilişkilendirebiliriz fakat, şimdilik en son seçenek olan **Create thing without certicate** ile ilerleyelim. Sertifikaya IoT Thing'i sonraki adımda ilişkilendirelim.

10. 'Thing' sayfasında yeni oluşturduğumuz **Robo1** listelenecektir.


**AWS Web Arayüzünden IoT Policy Oluşturulması - Robo1 **

Bu bölümde IoT Thing'lerin **_yetkilendirmesinde_** kullanmak için IoT Policy oluşturulacaktır.

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.

1. Sol taraftaki menüden **Secure** tıklayın.

2. **Policies** tıklayın

3. **Create a policy** butonuna tıklayın.

4. 'Name' alanına **RoboPolicy** yazın.

5.'Add Statement' alanının solunda **Advanced Mode** tıklayın. (Basic Mode'da çalıştığınızda da 'Action' alanında otomatik filtreleme ile kolaylıkla aksiyon secilebilir. Örneğin 'iot' yazmaya başladığınızda, tüm iot aksiyonları listelenecektir.)

6. 'Advanced Mode' Policy'lerin doğrudan JSON formatında yazılması şeklindedir. Robotların aşağıdaki aksiyonları gerçekleştirmeye yetkisi olması gerektiği için
    * IoT Core Endpoint2e bağlantı kurabilme
    * IoT Topic'lere Publisher ya da Subscriber olabilme
    * Subscribe olduğu IoT Topic'den Mesaj okuyabilme
  
  Bunun için 'advanced mode' alanındaki mevcut JSON Policy kaydını silip, yerine aşağıdakini yapıştırın.
  
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iot:Connect",
        "iot:Publish",
        "iot:Subscribe",
        "iot:Receive",
        "greengrass:Discover"
      ],
      "Resource": [
         "*" 
       ]
    } 
  ]
}
```

7. **Create** butonuna tıklayın.

8. Yetkilendirme için kullanacağınız Policy başarıyla tanımlandı. Policy listesinde görebilirsiniz.


**AWS Web Arayüzünden IoT Sertifikasyonu Oluşturulması - Robo1 **

Bu bölümde kimlik doğrulama (authentication) için kullanılacak IoT Sertifikası oluşturacağız.

Aşağıdaki adımları takip edebilir ya da videodan izleyerek de ilerleyebilirsiniz.



1. Sol taraftaki menüden **Secure** tıklayın.

2. **Certificates** tıklayın

3. **Create a certificates** butonuna tıklayın.

4. Seçeneklerden en üstteki **Create Certificates** butonuna tıklayın.

5. 'AWS IoT's Certicate Authority' otomatik olarak Public Key ve Private Key dosyalarını oluşturacaktır ki, bunları download etmemiz gerekiyor. Isterseniz kendi Certicate Authority (CA) yükleyebilirsiniz. Ya da mevcut Private Key kullanarak 'certificate signing request (CSR)' oluşturabilirim. Biz bu aşamada hızlı ve kolay olması açısından AWS IoT's CA kullanacağız.

6. Sertifikalar oluşturuldu, şimdi tüm Public Key, Private Key ve Sertifika dosyasını makinanıza indirmeniz gerekecektir. 

7. Sayfanın en altındaki **Activate** butonuna tıklayın. Aktivasyondan sonra bu sertifika ile ilişkilendirilecek IoT Thing'leri AWS IoT Core ile bağlanabilir hale gelmiş oldu.  

8. **A certificate for this thing** sertifikasını indirmek için **download** linkini tıklayın. ve dosyanın adını **_certificate.pem_** olarak değiştirin.

9. **A private key** dosyasını indirmek için **download** linkini tıklayın. ve dosyanın adını **_privateKey.pem_** olarak değiştirin.

10. Public Key dosyasını indirmeye ihtiyacımız yok. Zaten IoT Core içinde tanımlı olarak duruyor.

11. **DONE** butonuna tıklayın. Dikkat _Attach a policy_ butonu değil..

12. Öncelikle oluşturduğunuz Sertifika INACTIVE görünecektir, Sol taraftaki menüden **Certificates**  tekrar tıkladığınızda (ya da sayfayı güncelleyin) sertifikanın ACTIVE olduğunu göreceksiniz.


 **AWS Web Arayüzünden IoT Sertifikasyonu ile IoT Thing ve IoT Policy'nin İlişkilendirilmesi - Robo1 **

    

 



