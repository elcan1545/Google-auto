[app]
# Uygulama adı ve paketi
title = Mail Link Generator
package.name = mailinkgenerator
package.domain = org.maillink

# Kaynak dosyaları
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Versiyon
version = 1.0

# Gereksinimler (Android üzerinde çalışacak kütüphaneler)
requirements = python3==3.11.0,kivy==2.3.0,requests,urllib3,certifi,charset-normalizer,idna

# Android bildirimleri
android.permissions = INTERNET

# Android API seviyeleri
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True

# Orientation
orientation = portrait

# Tam ekran (Android)
fullscreen = 0

# Log seviyesi
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
