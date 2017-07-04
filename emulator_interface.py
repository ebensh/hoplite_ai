#!/usr/bin/env monkeyrunner

import time

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

class EmulatorInterface(object):
  self._device = None  # A MonkeyDevice object
  
  def __init__(self):
    self._device = MonkeyRunner.waitForConnection()

  def RunHoplite(self):
    package = 'com.magmafortress.hoplite'
    activity = 'com.magmafortress.hoplite.MainActivity'
    runComponent = package + '/' + activity
    self._device.startActivity(component=runComponent)
  
  def GetScreen(self):
    result = self._device.takeSnapshot()
    return result

  def GetAndSaveScreen(self, path):
    screen = self.GetScreen()  # Takes a screenshot.
    screen.writeToFile(path,'png')

  def TouchPixel(self, p):
    # device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
    assert(False)  # TODO
