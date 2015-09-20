import cv2
import numpy as np

img = cv2.imread('screenshots/screenshot1.png', cv2.IMREAD_GRAYSCALE)
print img
cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

