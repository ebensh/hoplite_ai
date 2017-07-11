#!/usr/bin/env monkeyrunner

import array
from SimpleXMLRPCServer import SimpleXMLRPCServer
import time
import xmlrpclib

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

class EmulatorInterface(object):
  _device = None  # A MonkeyDevice object
  
  def __init__(self):
    self._device = MonkeyRunner.waitForConnection()

  def RunHoplite(self):
    package = 'com.magmafortress.hoplite'
    activity = 'com.magmafortress.hoplite.MainActivity'
    runComponent = package + '/' + activity
    self._device.startActivity(component=runComponent)
  
  def GetScreenshot(self):
    monkey_img = self._device.takeSnapshot()

    # Get the image as a string (iterable of binary bytes).
    # NOTE: These bytes are *signed*, because they're coming from java!
    img_bytes_signed = monkey_img.convertToBytes('png')

    # Convert to unsigned.
    img_bytes = array.array('B', [b & 255 for b in img_bytes_signed])

    # In order to send the unsigned bytes we wrap them in a Binary object.
    return xmlrpclib.Binary(img_bytes.tostring())

  # def GetAndSaveScreen(self, path):
  #   screen = self.GetScreen()  # Takes a screenshot.
  #   screen.writeToFile(path,'png')

  # def TouchPixel(self, p):
  #   # device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
  #   assert(False)  # TODO

server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
emulator_interface = EmulatorInterface()
server.register_instance(emulator_interface)
server.serve_forever()
