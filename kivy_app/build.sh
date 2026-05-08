#!/usr/bin/env bash
set -e

echo "======================================="
echo "  Mail & Link Generator — APK Builder  "
echo "======================================="

cd "$(dirname "$0")"

# Java kontrolü
if ! java -version &>/dev/null; then
  echo "HATA: Java bulunamadı."
  exit 1
fi

# Buildozer kontrolü
if ! buildozer --version &>/dev/null; then
  echo "Buildozer kuruluyor..."
  pip install buildozer cython
fi

echo ""
echo ">> APK derleniyor... (ilk seferinde SDK/NDK indirir, 20-40 dk sürebilir)"
echo ""

buildozer android debug

echo ""
echo "======================================="
echo "  TAMAMLANDI!"
ls bin/*.apk 2>/dev/null && echo "  APK: $(ls bin/*.apk)"
echo "======================================="
