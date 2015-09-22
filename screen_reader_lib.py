import cv2
from grid_lib import *
import numpy as np

WHITE = (255, 255, 255)

# Given an image and a set of points that bound a region of interest (ROI),
# most often the corners of a Hex, will use the points as a contour
# to create a masking polygon, returning just the image in the ROI.
def GetImageByCorners(img, points):
  # Create the mask image and fill it with white poly bounding the points.
  mask = np.zeros(img.shape, dtype=np.uint8)
  cv2.fillConvexPoly(mask, points, WHITE)
  
  # Get the bounding rectangle of the mask; we'll only return this region.
  x,y,w,h = cv2.boundingRect(points)

  # Apply the mask and crop to the bounding rectangle, returning the result.
  return np.bitwise_and(img, mask)[y:y+h,x:x+w].copy()
