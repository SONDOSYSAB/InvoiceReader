[app]
title = InvoiceReader
package.name = invoicereader
package.domain = org.invoice
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
source.dir = .
# تأكد من أن المتطلبات مكتوبة هكذا بدون مسافات زائدة
requirements = python3,kivy,kivymd,pymupdf,pillow
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
