import cv2
import numpy as np
import time
import xmlrpclib

import screen_interpreter

def main():
  emulator_server = xmlrpclib.ServerProxy("http://localhost:8000/")

  screenshot_bytes = emulator_server.GetScreenshot().data
  nparr = np.fromstring(screenshot_bytes, np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

  cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
  cv2.imshow('image', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
   #screen_interpreter.GetBoard()


if __name__ == '__main__':
  main()
