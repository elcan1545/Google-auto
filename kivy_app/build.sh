#!/usr/bin/env bash
# ============================================================
# Mail & Link Generator — APK Builder
# NOT: Bu script Replit shell'de çalışmayabilir (NixOS uyumsuzluğu).
# Önerilen yöntem: GitHub Actions (bkz. KURULUM.md)
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================="
echo "  Mail & Link Generator — APK Builder  "
echo "======================================="

export PYTHONPATH="/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages:${PYTHONPATH:-}"
ZLIB_INC=$(pkg-config --cflags zlib 2>/dev/null | sed 's/-I//' || echo "")
ZLIB_LIB=$(pkg-config --libs-only-L zlib 2>/dev/null | sed 's/-L//' || echo "")
OPENSSL_INC=$(pkg-config --cflags openssl 2>/dev/null | sed 's/-I//' || echo "")
OPENSSL_LIB=$(pkg-config --libs-only-L openssl 2>/dev/null | sed 's/-L//' || echo "")
LIBFFI_INC=$(pkg-config --cflags libffi 2>/dev/null | sed 's/-I//' || echo "")

export CPATH="$ZLIB_INC:$OPENSSL_INC:$LIBFFI_INC:${CPATH:-}"
export LIBRARY_PATH="$ZLIB_LIB:$OPENSSL_LIB:${LIBRARY_PATH:-}"
export C_INCLUDE_PATH="$CPATH"
export LD_LIBRARY_PATH="$ZLIB_LIB:$OPENSSL_LIB:${LD_LIBRARY_PATH:-}"
export JAVA_HOME="$(dirname $(dirname $(readlink -f $(which java))))"
export PATH="$JAVA_HOME/bin:$PATH"

echo "Java:      $(java -version 2>&1 | head -1)"
echo "Buildozer: $(buildozer --version)"
echo ""
echo ">> Derleme başlıyor..."
echo ""

buildozer android debug

echo ""
echo "======================================="
ls bin/*.apk 2>/dev/null && echo "APK: $(ls bin/*.apk)" || echo "HATA: APK bulunamadi."
echo "======================================="
