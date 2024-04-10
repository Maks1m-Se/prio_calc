[app]

# (str) Title of your application
title = TaskEvaluationApp

# (str) Package name
package.name = taskevaluation

# (str) Package domain (needed for android/ios packaging)
package.domain = org.kivy

# (str) Source code where the main.py file is located
source.dir = .

# (list) Application requirements
requirements = kivy, pandas, tabulate

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (list) Permissions
android.permissions = INTERNET

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
