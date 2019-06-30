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


Tebrikler..!! Yeni Kullanıcı'yı başarı ile oluşturdunuz.

IAM Ana sayfasındaki sol taraftaki menüden "Dashboard" tıklayın, ve sayfanın en üstünde bulunan 'IAM users sign-in link:' de https://.. ile başlayan linki kopyalayıp browser'da yeni sekmede sayfayı açın.  Yeni kullanıcı adınız ve şifrenizi kullanarak sisteme giriş yapın. 




