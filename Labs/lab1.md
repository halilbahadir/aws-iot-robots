## Lab 1: 2 Robotların IoT Core'a Bağlanması

  Bu lab çalışmasında 2 tane robot (Thing) oluşturup, bu robotları AWS IoT Core servisi ile bağlantısını kuracağız. Böylelikle Robot'lar IoT Core'daki IoT Topic'lerine data gönderebilecekler. Bu bağlantıyı güvenli bir şekilde sağlayabilmek için Robot (Thing), politika (policy) ve sertifika (certification) oluşturmamız gerekecek. Sertifika kimlik doğrulama için kullanılırken, politika ise kimlik doğrulaması alan robotun ne yapmaya yetkilendirildiğini tarifleyecek.
  Birinici robotu AWS web konsoldan, ikincisini ise komut satırından.
  
  Tabi elimizde gerçek robotlar olmadığı için :smile: simülasyonu Amazon Cloud9 kullanarak gerçekleştireceğiz. Fakat sonraki lab'larda Rasberry Pi bizim robotlarımız olacak. 
 
