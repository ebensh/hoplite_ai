# Orig: http://docs.opencv.org/trunk/d4/dc6/tutorial_py_template_matching.html

import cv2
import glob
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('screenshots/screenshot1.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

for monster_image_path in glob.glob('hoplite_assets/cleaned/mon*.png'):
  print "Looking for monster:", monster_image_path
  template = cv2.imread(monster_image_path, cv2.IMREAD_GRAYSCALE)
  w, h = template.shape[::-1]

  res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
  threshold = 0.7
  loc = np.where(res >= threshold)
  for pt in zip(*loc[::-1]):
    print "Found %s at %s" % (monster_image_path, pt)
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imshow('found', img_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()
