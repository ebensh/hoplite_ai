import cv2
import numpy as np
import time
import xmlrpclib

import screen_interpreter

def main():
  emulator_server = xmlrpclib.ServerProxy("http://localhost:8000/")

  screenshot_bytes = emulator_server.GetScreenshot().data
  nparr = np.fromstring(screenshot_bytes, np.uint8)
  screenshot = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

  cv2.namedWindow('screenshot', cv2.WINDOW_NORMAL)
  cv2.namedWindow('tile', cv2.WINDOW_NORMAL)
  cv2.imshow('screenshot', screenshot)

  cv2.waitKey(1)
  screen_interpreter.GetBoard(screenshot)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()
