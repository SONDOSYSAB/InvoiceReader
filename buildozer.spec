[app]
title = InvoiceReader
package.name = invoicereader
package.domain = org.invoice
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
source.dir = .
requirements = python3,kivy==2.2.1,kivymd==1.2.0,pymupdf,pillow
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 21
android.ndk = 23b
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
p4a.branch = develop