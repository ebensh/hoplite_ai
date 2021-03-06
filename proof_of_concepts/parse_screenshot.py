import cv2
from grid_lib import *
import numpy as np
from screen_reader_lib import *

TILE_WIDTH = 69
TILE_HEIGHT = 64
WHITE = (255, 255, 255)
BOARD_CENTER_Y = 841

ALL_HEXES = [Hex(q, -q - s, s)
             for q in xrange(-4, 4 + 1)
             for s in xrange(-5, 5 + 1)
             if abs(-q - s) <= 5]

def main():
  img = cv2.imread('screenshot.png', cv2.IMREAD_COLOR)
  screen_height, screen_width, screen_depth = img.shape
  print img.shape
  layout = Layout(orientation_flat, Point(TILE_WIDTH, TILE_HEIGHT),
                  Point(screen_width / 2, BOARD_CENTER_Y))

  tile_hexes = []
  for h in ALL_HEXES:
    hex_img = GetImageByCorners(img, np.array(map(lambda p: p.Round(),
                                                   polygon_corners(layout, h))))
    #cv2.imwrite('hex_images/hex_{0}_{1}_{2}.png'.format(h.q, h.r, h.s), hex_img)

    label = 'r{0},c{1}'.format(qoffset_from_cube(EVEN, h).row,
                               qoffset_from_cube(EVEN, h).col)
    #label = "{0},{1},{2}".format(h.q, h.r, h.s)
    img = cv2.putText(img, label, hex_to_pixel(layout, h).Round(),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))

    for p1, p2 in polygon_edges(layout, h):
      print p1, p2
      img = cv2.line(img, p1, p2, WHITE)

  cv2.namedWindow('image', cv2.WINDOW_NORMAL)
  cv2.imshow('image', img)
  cv2.waitKey(0)
  #cv2.imwrite('screenshot1_labeled.png', img)
  cv2.destroyAllWindows()
      
  

if __name__ == '__main__':
  main()

