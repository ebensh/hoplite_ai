import cv2
import numpy as np
import os

from grid_lib import *
from hoplite_types import Board, TileType

# TODO: Keep the assets in RAM (there aren't many) to avoid reloading and
# scaling every time. Plenty of room for optimization in this file :)

# Given an image and a set of points that bound a region of interest (ROI),
# most often the corners of a Hex, will use the points as a contour
# to create a masking polygon, returning just the image in the ROI.
def GetImageByCorners(img, points):
  WHITE = (255, 255, 255)
  
  # Create the mask image and fill it with white poly bounding the points.
  mask = np.zeros(img.shape, dtype=np.uint8)
  cv2.fillConvexPoly(mask, points, WHITE)

  # Get the bounding rectangle of the mask; we'll only return this region.
  x,y,w,h = cv2.boundingRect(points)

  # Apply the mask and crop to the bounding rectangle, returning the result.
  return np.bitwise_and(img, mask)[y:y+h,x:x+w].copy()


def GetBoard(screenshot):
  TILE_WIDTH = 65  # 40
  TILE_HEIGHT = 62  # 37

  ALL_HEXES = [Hex(q, -q - s, s)
               for q in xrange(-4, 4 + 1)
               for s in xrange(-5, 5 + 1)
               if abs(-q - s) <= 5]

  screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
  #screen_height, screen_width, screen_depth = screenshot.shape
  screen_height, screen_width = screenshot.shape
  layout = Layout(orientation_flat, Point(TILE_WIDTH, TILE_HEIGHT),
                  Point(screen_width / 2, screen_height / 2 - 33))

  ASSETS_BASE_PATH  = 'hoplite_assets/cleaned/'
  asset_file_to_tile_type = {
    'dung_altar_1.png': TileType.Altar,
    'dung_altar_2.png': TileType.Altar,
    'dung_altar_3.png': TileType.Altar,
    'dung_altar_used_1.png': TileType.UsedAltar,
    'dung_fleece_1.png': TileType.Fleece,
    'dung_ladderdown_1.png': TileType.LadderDown,
    'dung_portal_1.png': TileType.Portal,
    'dung_portal_2.png': TileType.Portal,
    'dung_portal_3.png': TileType.Portal,
    'mon_bomb_1.png': TileType.BombMon,
    'mon_bomb_cd_1.png': TileType.BombMonCooldown,
    'mon_bow_1.png': TileType.BowMon,
    'mon_sword_1.png': TileType.SwordMon,
    'mon_wizard_1.png': TileType.WizardMon,
    'mon_wizard_cd_1.png': TileType.WizardMonCooldown,
    'proj_bomb_1.png': TileType.Bomb,
    'proj_bomb_2.png': TileType.Bomb,
    'proj_bomb_3.png': TileType.Bomb
  }

  tile_hexes = []
  for h in ALL_HEXES:
    print "Looking in hex %s" % (h,)
    hex_img = GetImageByCorners(screenshot,
                                np.array(map(lambda p: p.Round(),
                                             polygon_corners(layout, h))))
    cv2.imshow('tile', hex_img)
    cv2.waitKey(1000)

    for asset_file, tile_type in asset_file_to_tile_type.iteritems():
      asset_path = os.path.join(ASSETS_BASE_PATH, asset_file)
      asset = cv2.imread(asset_path, cv2.IMREAD_GRAYSCALE)
      width, height = asset.shape[::-1]

      res = cv2.matchTemplate(hex_img, asset, cv2.TM_CCOEFF_NORMED)
      threshold = 0.7
      loc = np.where(res >= threshold)
      for pt in zip(*loc[::-1]):
        print "ScreenInterpter: %s: %s" % (h, asset_file)
        cv2.rectangle(hex_img, pt, (pt[0] + width, pt[1] + height), (0,0,255), 2)
        cv2.imshow('tile', hex_img)
        cv2.waitKey(1000)
        
  

def GetStateFromScreenshot(screenshot):
  """Given a screenshot builds game state."""
  state = State()
  
