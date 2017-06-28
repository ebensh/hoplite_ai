import time

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

# Installs the Android package. Returns boolean.
# device.installPackage('myproject/bin/MyApplication.apk')

# sets a variable with the package's internal name
package = 'com.magmafortress.hoplite'

# sets a variable with the name of an Activity in the package
activity = 'com.magmafortress.hoplite.MainActivity'

# sets the name of the component to start
runComponent = package + '/' + activity

# Runs the component
device.startActivity(component=runComponent)

# Presses the Menu button
# device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)

time.sleep(5)

# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile('hoplite_screen.png','png')
