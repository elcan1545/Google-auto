[app]
title = Mail Link Generator
package.name = maillinkgenerator
package.domain = org.maillink

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

# Android'de HTTPS (requests + smtplib ssl) için openssl şart
requirements = python3,kivy==2.3.0,openssl,requests,urllib3,certifi,charset-normalizer,idna

android.permissions = INTERNET

android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.private_storage = True
android.accept_sdk_license = True

# Arkaplan servisleri kapalı
android.enable_androidx = True

orientation = portrait
fullscreen = 0

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
