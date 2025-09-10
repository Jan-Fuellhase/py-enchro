[app]
title = EncDecApp
package.name = encdecapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,pycryptodome
orientation = portrait
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
