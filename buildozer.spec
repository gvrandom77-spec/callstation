[app]

# (str) Title of your application
title = Call Station

# (str) Package name
package.name = callstation

# (str) Package domain (needed for android packaging)
package.domain = net.gvho

# (str) Source file where the main.py file is located
source.dir = .

# (list) Source files to include (let it empty to include all the files)
source.include_exts = py,png,jpg

# (list) List of inclusions
source.include_patterns = assets/*

# (list) Source files to exclude (let it empty to exclude all the files)
source.exclude_patterns = tests/*, test/*, lib2to3/*

# (str) Application versioning
version = 1.0

# (str) Application icon
icon.filename = icon.png

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, READ_PHONE_STATE, READ_CALL_LOG, FOREGROUND_SERVICE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (list) Application requirements
requirements = python3,kivy,pyjnius,android

# (bool) Indicate if the application should be steady
android.wakelock = True

# (int) Android API to target
android.api = 33

# (int) Minimum API required
android.minapi = 21

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
