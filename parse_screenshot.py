import cv2
from grid_lib import *
import numpy as np

TILE_WIDTH = 40
TILE_HEIGHT = 37
WHITE = (255, 255, 255)

ALL_HEXES = [Hex(q, -q - s, s)
             for q in xrange(-4, 4 + 1)
             for q in xrange(-5, 5 + 1)
             if abs(-q - s) <= 5]

def main():
  img = cv2.imread('screenshots/screenshot1.png', cv2.IMREAD_GRAYSCALE)
  screen_height, screen_width = img.shape
  layout = Layout(layout_flat, Point(TILE_WIDTH, TILE_HEIGHT),
                  Point(screen_width / 2, screen_height / 2 - 33))

  tile_hexes = []
  for h in ALL_HEXES:
    label = "{0},{1},{2}".format(h.q, h.r, h.s)
    img = cv2.putText(img, label, point_round(hex_to_pixel(layout, h)),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255))
    for p1, p2 in polygon_edges(layout, h):
      print p1, p2
      img = cv2.line(img, p1, p2, WHITE)

  cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
  cv2.imshow('image', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
      
  

if __name__ == '__main__':
  main()

