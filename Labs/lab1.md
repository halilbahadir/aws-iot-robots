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

1. AWS Web Arayüzünden 'IoTRoboUser' kullanıcısı ile giriş yapın ve Cloud9 servisi ana sayfasına (dashboard) geçin.
2. Sağ üs köşeden AWS Region olarak **"EU (Ireland)"** seçildiğinden emin olun.
3. Cloud9 Dashboard ekranında turuncu "Create Environment" butonuna tıklayın.
4. Name alanına **IoTRobotsIDE** yazın. Sonrasında "Next Step" butonuna tıklayın.
5. "Configuration Settings" ekraninda, mevcut değerleri (minimum gerekleri sağlayacak değerler işimizi görecektir) değiştirmeden "Next Step" butonuna tıklayın. 'Cost Saving Setting' alanında 30 dakika olarak atanan değer, sizin Cloud9 ortamını 30 dk kullanmadığınız durumda otomatik olarak uyku moduna geçmesine sebep olur. Bu durumda herhangi bir o anki durum kaydedilir, tekrar çalıştırdığınızda kaldığınız yerde devam edebilirsiniz. 
6. Onay sayfasında, Cloud9 IDE kullanırken önerilen en iyi pratiklere göz atmakta fayda var. Sonrasında "Create Environment" butonuna tıklayın.








