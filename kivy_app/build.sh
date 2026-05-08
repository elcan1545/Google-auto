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

nix-shell \
  -p zlib openssl libffi autoconf libtool pkg-config cmake openjdk17 which ccache git unzip zip \
  --run '
    set -e

    # Java yolu
    export JAVA_HOME="$(dirname $(dirname $(readlink -f $(which java))))"
    export PATH="$JAVA_HOME/bin:$PATH"

    # Nix paket yollarını buildozer için dışa aç
    export CPATH="$NIX_CFLAGS_COMPILE"
    export LIBRARY_PATH="$(echo $NIX_LDFLAGS | tr " " "\n" | grep "^-L" | sed "s/-L//" | tr "\n" ":")"

    echo "Java:     $(java -version 2>&1 | head -1)"
    echo "Buildozer: $(buildozer --version)"
    echo ""
    echo ">> Derleme başlıyor... (ilk seferinde SDK/NDK indirir, 20-40 dk sürebilir)"
    echo ""

    buildozer android debug

    echo ""
    echo "======================================="
    echo "  TAMAMLANDI!"
    ls bin/*.apk 2>/dev/null && echo "  APK: $(ls bin/*.apk)" || echo "  APK bulunamadi, loglari kontrol edin."
    echo "======================================="
  '
