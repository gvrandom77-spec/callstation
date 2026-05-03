[app]
title = Call Station
package.name = callstation
package.domain = net.gvho
source.dir = .
source.include_exts = py,png,jpg
version = 1.0

# Иконка
icon.filename = %(source.dir)s/icon.png

# Ориентация экрана
orientation = portrait

# Разрешения Android для перехвата звонков
android.permissions = INTERNET, READ_PHONE_STATE, READ_CALL_LOG

# Требования для сборки
requirements = python3,kivy,pyjnius,android

# (bool) Оставлять ли экран включенным
android.wakelock = True

# (int) Минимальный и целевой Android API
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1