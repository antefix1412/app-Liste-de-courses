[app]
title = Liste de courses
package.name = courses
package.domain = org.example
icon.filename = icon.png  # Utilisez un fichier PNG pour l'icône

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE
android.minapi = 21  # Version minimale d'Android
android.debug = True  # Activer le débogage

[buildozer]
log_level = 2