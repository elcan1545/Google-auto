#!/usr/bin/env bash
# ============================================================
# Mail & Link Generator — APK Builder (NixOS / Replit Shell)
# Kullanım: bash build.sh   (kivy_app/ klasöründen çalıştırın)
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================="
echo "  Mail & Link Generator — APK Builder  "
echo "======================================="
echo "Dizin: $SCRIPT_DIR"
echo ""

# ── Zlib ve diğer nix kütüphanelerinin yollarını bul ──────
ZLIB_INC=$(pkg-config --cflags zlib | sed 's/-I//')
ZLIB_LIB=$(pkg-config --libs-only-L zlib | sed 's/-L//')
OPENSSL_INC=$(pkg-config --cflags openssl 2>/dev/null | sed 's/-I//' || echo "")
OPENSSL_LIB=$(pkg-config --libs-only-L openssl 2>/dev/null | sed 's/-L//' || echo "")
LIBFFI_INC=$(pkg-config --cflags libffi 2>/dev/null | sed 's/-I//' || echo "")

# ── Derleme ortamını hazırla ──────────────────────────────
export CPATH="$ZLIB_INC:$OPENSSL_INC:$LIBFFI_INC:${CPATH:-}"
export LIBRARY_PATH="$ZLIB_LIB:$OPENSSL_LIB:${LIBRARY_PATH:-}"
export C_INCLUDE_PATH="$ZLIB_INC:$OPENSSL_INC:$LIBFFI_INC:${C_INCLUDE_PATH:-}"
export LD_LIBRARY_PATH="$ZLIB_LIB:$OPENSSL_LIB:${LD_LIBRARY_PATH:-}"
export JAVA_HOME="$(dirname $(dirname $(readlink -f $(which java))))"
export PATH="$JAVA_HOME/bin:$PATH"

echo "Java:      $(java -version 2>&1 | head -1)"
echo "Buildozer: $(buildozer --version)"
echo "Zlib inc:  $ZLIB_INC"
echo ""
echo ">> Derleme başlıyor... (ilk seferinde SDK/NDK indirir, 20-40 dk sürebilir)"
echo ""

buildozer android debug

echo ""
echo "======================================="
echo "  TAMAMLANDI!"
ls bin/*.apk 2>/dev/null && echo "  APK: $(ls bin/*.apk)" || echo "  HATA: APK bulunamadı, log'ları kontrol edin."
echo "======================================="
