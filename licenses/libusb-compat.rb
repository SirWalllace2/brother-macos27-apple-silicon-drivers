class LibusbCompat < Formula
  desc "Library for USB device access"
  homepage "https://libusb.info/"
  url "https://downloads.sourceforge.net/project/libusb/libusb-compat-0.1/libusb-compat-0.1.9/libusb-compat-0.1.9.tar.bz2"
  sha256 "179d934676ad3bd172a5a37cf5c6351b8e9d7816feb3029252e79b30a518a3be"
  license all_of: [
    "LGPL-2.1-or-later",
    any_of: ["LGPL-2.1-or-later", "BSD-3-Clause"], # libusb/usb.h
  ]
  compatibility_version 1

  livecheck do
    url :stable
    regex(%r{url=.*?/libusb-compat[._-]v?(\d+(?:\.\d+)+)\.t}i)
  end

  depends_on "autoconf" => :build
  depends_on "automake" => :build
  depends_on "libtool" => :build
  depends_on "pkgconf" => :build
  depends_on "libusb"

  def install
    system "./configure", *std_configure_args
    system "make", "install"
  end

  test do
    system bin/"libusb-config", "--libs"
  end
end
