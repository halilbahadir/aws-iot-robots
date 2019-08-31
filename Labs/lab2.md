## Lab 2: AWS IoT Rules 

  
  Bu lab çalışmasında, robotlardan herhangi birinin pil seviyesinin %10'un altına düştüğü durumda operatörlere eposta gönderilmesini tetikleyen bir kural tanımlayacağız. Bunun için öncelikle bir SNS (Simple Notification Service) Topic oluşturup ve SNS Topic'e bır eposta adresi ile abone (subscribe) olacağız. Öncelikle IoT Servisinin, SNS Topic'e mesaj yayınlaması (publish) için yetki vermemiz gerekiyor. Sonrasında da SNS Topic'e gelen mesajlar üzerinde SQL Sorgusu kullanarak pil seviyesini kontrol eden bir IoT Rule tanımlayacağız.  
 
 Amazon Simple Notification Service (SNS) servisi, dağıtık sistemleri ve serverless uygulamaları birbirinden ayırmanıza imkan tanıyan yüksek oranda erişilebilir, sağlam, güvenli ve tam olarak yönetilen bir pub/sub mesajlaşma hizmetidir. SNS ayrıca, son kullanıcılara mobil anlık bildirimler, SMS ve e-posta yollarıyla bildirim dağıtılması için kullanılabilir. 
  
  Bu lab çalışmasında aşağıdaki mimari ve akışı gerçekleştireceğiz.

![alt text](https://github.com/halilbahadir/aws-iot-robots/blob/master/images/iot-lab2.png)


