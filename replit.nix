{pkgs}: {
  deps = [
    pkgs.automake
    pkgs.which
    pkgs.ccache
    pkgs.git
    pkgs.zip
    pkgs.unzip
    pkgs.openssl
    pkgs.libffi
    pkgs.cmake
    pkgs.zlib
    pkgs.pkg-config
    pkgs.libtool
    pkgs.autoconf
    pkgs.openjdk17
  ];
}
