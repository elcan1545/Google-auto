# Mail & Link Generator — APK Kurulum Rehberi

## Dosyalar

| Dosya | Açıklama |
|-------|----------|
| `main.py` | Kivy uygulaması (5 alan) |
| `buildozer.spec` | APK derleme ayarları |
| `.github/workflows/build-apk.yml` | GitHub Actions APK builder |

---

## Yöntem 1: GitHub Actions (Önerilen — Ücretsiz)

**Neden?** Replit NixOS tabanlıdır, buildozer ise Debian/Ubuntu ister. GitHub Actions standart Ubuntu kullanır ve buildozer sorunsuz çalışır.

### Adımlar

1. **GitHub'da yeni bir repo oluşturun** (ör. `mail-link-generator`)

2. **`kivy_app/` klasörünün içeriğini** bu repoya yükleyin:
   ```
   main.py
   buildozer.spec
   .github/workflows/build-apk.yml
   ```

3. **Push edin** — Actions otomatik başlar

4. **APK'yı indirin:**
   - GitHub repo sayfası → **Actions** sekmesi
   - Son başarılı run → **Artifacts** → `mail-link-generator-apk` → İndir

5. `.zip` içindeki `.apk` dosyasını telefona atın → yükleyin

> İlk çalıştırma ~20-30 dakika sürer. Sonrakiler ~5-10 dakika (cache var).

---

## Yöntem 2: Google Colab (Alternatif — Ücretsiz)

1. [colab.research.google.com](https://colab.research.google.com) açın
2. Yeni notebook oluşturun, hücrelere sırayla yapıştırıp çalıştırın:

```python
# Hücre 1 — Kurulum
!sudo apt-get update -qq
!sudo apt-get install -y git zip unzip openjdk-17-jdk \
  autoconf libtool pkg-config zlib1g-dev \
  cmake libffi-dev libssl-dev build-essential
!pip install buildozer cython
```

```python
# Hücre 2 — main.py ve buildozer.spec'i yükleyin
# Sol panelden dosyaları sürükleyip bırakın: main.py, buildozer.spec
```

```python
# Hücre 3 — Build
!buildozer android debug
```

```python
# Hücre 4 — APK indir
from google.colab import files
import glob
apk = glob.glob('bin/*.apk')[0]
files.download(apk)
```

---

## Gmail Uygulama Şifresi

Uygulamada "E-posta Şifresi" alanına **normal Gmail şifresi değil** Uygulama Şifresi girin:

1. **Google Hesabı** → **Güvenlik**
2. **2 Adımlı Doğrulama** açın (kapalıysa)
3. Arama kutusuna **"Uygulama şifreleri"** yazın
4. "Diğer (özel ad)" → "Mail Link Generator" → **Oluştur**
5. Üretilen **16 karakterlik** şifreyi kopyalayın

---

## APK'yı Telefona Yükleme

1. `.apk` dosyasını telefona kopyalayın (USB / Google Drive / WhatsApp)
2. Dosya yöneticisinden açın
3. **"Bilinmeyen kaynaklardan yüklemeye izin ver"** → Yükle

---

## Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| `SMTPAuthenticationError` | Gmail Uygulama Şifresi yanlış |
| `Bağlantı Hatası` | Uygulamanın deploy edilmiş olması gerekiyor |
| APK yüklenmiyor | Ayarlar → Güvenlik → Bilinmeyen kaynaklar → İzin ver |
| E-posta spam'a düştü | Spam/Junk klasörünü kontrol edin |
