# https://www.learnopencv.com/blob-detection-using-opencv-python-c/

import cv2
import numpy as np
from itertools import izip_longest

# https://stackoverflow.com/questions/434287/what-is-the-most-pythonic-way-to-iterate-over-a-list-in-chunks
def grouper(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return izip_longest(*args, fillvalue=fillvalue)
 
img = cv2.imread("screenshot.png", cv2.IMREAD_GRAYSCALE)

# Threshold the image so that background is black and objects are white.
_, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)

# Reduce to one column of values by taking the minimum value across rows.
maximums = np.amax(img, axis=1)
# Get the indexes of every row where the value *changes*.
change_ixs = np.where(np.roll(maximums, 1) != maximums)[0]
# Group the changes into pairs (start and end).
for group in grouper(change_ixs, 2, len(maximums)):
  print group

# Brittle? Yes. Proof of concept? Absolutely :)
# 0th group is the status at the top.
# 1st group is the hexagonal grid.
# 2nd group is health.
# 3rd group is skills / abilities.
# 4th group is menu buttons.
board_start, board_end = list(grouper(change_ixs, 2, len(maximums)))[1]
board_height = board_end - board_start
print board_height

# There are 11 tiles (and 10 gaps) in the height of the grid.
tile_height = board_height / 11
print "Tile height: ", tile_height
print "Board y-center: ", board_start + board_height / 2

exit(1)
