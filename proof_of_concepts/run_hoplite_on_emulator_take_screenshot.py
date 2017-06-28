#!/usr/bin/env monkeyrunner

import time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

device = MonkeyRunner.waitForConnection()  # Returns a MonkeyDevice object.
# device.installPackage('myproject/bin/MyApplication.apk') # Returns a bool.

package = 'com.magmafortress.hoplite'
activity = 'com.magmafortress.hoplite.MainActivity'
runComponent = package + '/' + activity
device.startActivity(component=runComponent)

# Presses the Menu button
# device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)



time.sleep(3)

result = device.takeSnapshot() # Takes a screenshot
result.writeToFile('hoplite_screen.png','png') # Writes the screenshot to a file
