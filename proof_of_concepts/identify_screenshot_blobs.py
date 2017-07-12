# https://www.learnopencv.com/blob-detection-using-opencv-python-c/

import cv2
import numpy as np

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 1500
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False

params.minDistBetweenBlobs = 100
 
img = cv2.imread("screenshot.png", cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)

# Connect the blobs!
kernel = np.ones((25,25),np.uint8)
img = cv2.dilate(img, kernel, iterations=1)

# The blob detector likes black spots instead of white, so we invert.
img = cv2.bitwise_not(img)
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(img)
for keypoint in keypoints:
  print keypoint.pt, keypoint.size
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle
# corresponds to the size of blob.
img_with_keypoints = cv2.drawKeypoints(
    img, keypoints, np.array([]), (0,255,0),
    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.namedWindow("keypoints", cv2.WINDOW_NORMAL)
cv2.imshow("keypoints", img_with_keypoints)
cv2.waitKey(0)
