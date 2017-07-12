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
def GetImageByCorners(img, points, pad=0):
  WHITE = (255, 255, 255)
  
  # Create the mask image and fill it with white poly bounding the points.
  mask = np.zeros(img.shape, dtype=np.uint8)
  cv2.fillConvexPoly(mask, points, WHITE)

  # Get the bounding rectangle of the mask; we'll only return this region.
  x,y,w,h = cv2.boundingRect(points)
  x -= pad/2
  y -= pad/2
  w += pad
  h += pad

  # Apply the mask and crop to the bounding rectangle, returning the result.
  return img[y:y+h,x:x+w].copy()
  #return np.bitwise_and(img, mask)[y:y+h,x:x+w].copy()


OPTIMAL_SCALES = {}

def GetBoard(screenshot):
  TILE_WIDTH = 69
  TILE_HEIGHT = 64
  BOARD_CENTER_Y = 841

  ALL_HEXES = [Hex(q, -q - s, s)
               for q in xrange(-4, 4 + 1)
               for s in xrange(-5, 5 + 1)
               if abs(-q - s) <= 5]
  DEBUG_HEXES = [Hex(0, 0, 0),    # Empty
                 Hex(-2, -3, 5),  # SwordMon
                 Hex(4, -4, 0),   # ArcherMon
                 Hex(0, 4, -4)]   # Player
  THRESHOLD = 0.7

  screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
  #screen_height, screen_width, screen_depth = screenshot.shape
  screen_height, screen_width = screenshot.shape
  layout = Layout(orientation_flat, Point(TILE_WIDTH, TILE_HEIGHT),
                  Point(screen_width / 2, BOARD_CENTER_Y))

  ASSETS_BASE_PATH  = 'hoplite_assets/cleaned/'
  asset_file_to_tile_type = {
    #'dung_altar_1.png': TileType.Altar,
    #'dung_altar_2.png': TileType.Altar,
    #'dung_altar_3.png': TileType.Altar,
    #'dung_altar_used_1.png': TileType.UsedAltar,
    #'dung_fleece_1.png': TileType.Fleece,
    #'dung_portal_1.png': TileType.Portal,
    #'dung_portal_2.png': TileType.Portal,
    #'dung_portal_3.png': TileType.Portal,
    #'mon_bomb_1.png': TileType.BombMon,
    #'mon_bomb_cd_1.png': TileType.BombMonCooldown,
    #'proj_bomb_1.png': TileType.Bomb,
    #'proj_bomb_2.png': TileType.Bomb,
    #'proj_bomb_3.png': TileType.Bomb,
    #'dung_ladderdown_1.png': TileType.LadderDown,
    'tile_floor_1.png': TileType.Floor,
    'tile_floor_2.png': TileType.Floor,
    'tile_liquid_1.png': TileType.Liquid,
    'tile_liquid_2.png': TileType.Liquid,
    'tile_liquid_3.png': TileType.Liquid,
    'mon_bow_1.png': TileType.BowMon,
    'mon_sword_1.png': TileType.SwordMon,
    'mon_wizard_1.png': TileType.WizardMon,
    'mon_wizard_cd_1.png': TileType.WizardMonCooldown,    
  }

  tile_hexes = []
  for h in DEBUG_HEXES:  #ALL_HEXES:  #DEBUG_HEXES:
    print "Looking in hex %s" % (h,)
    hex_img = GetImageByCorners(screenshot,
                                np.array(map(lambda p: p.Round(),
                                             polygon_corners(layout, h))),
                                pad=10)
    hex_width, hex_height = hex_img.shape[::-1]
    cv2.imshow('tile', hex_img)
    cv2.waitKey(1)

    for asset_file, tile_type in asset_file_to_tile_type.iteritems():
      asset_path = os.path.join(ASSETS_BASE_PATH, asset_file)
      asset = cv2.imread(asset_path, cv2.IMREAD_GRAYSCALE)
      asset_width, asset_height = asset.shape[::-1]

      if asset_file not in OPTIMAL_SCALES:
        optimal_scale = None
        optimal_match_value = 0

        for dpi_multiple in xrange(1, 5, 1):
          for scale_factor in [x / 10.0 for x in range(5, 20)]:  # 0.5 to 1.9
            #print asset_path, dpi_multiple, scale_factor
            scaled_width = int(asset_width * dpi_multiple * scale_factor)
            scaled_height = int(asset_height * dpi_multiple * scale_factor)
            asset_scaled = np.repeat(np.repeat(asset, dpi_multiple, axis=0), dpi_multiple, axis=1)
            asset_scaled = cv2.resize(asset_scaled, (scaled_width, scaled_height))
            if scaled_width > hex_width or scaled_height > hex_height: break

            cv2.imshow('asset', asset_scaled)
            cv2.waitKey(1)
            res = cv2.matchTemplate(hex_img, asset_scaled, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)

            if maxVal > optimal_match_value and maxVal > THRESHOLD:
              optimal_scale = (dpi_multiple, scale_factor)
              optimal_match_value = maxVal
        if optimal_scale:
          print "Optimal scale found for %s: %s" % (asset_file, optimal_scale)
          OPTIMAL_SCALES[asset_file] = optimal_scale

      if asset_file in OPTIMAL_SCALES:
        dpi_multiple, scale_factor = OPTIMAL_SCALES[asset_file]
        scaled_width = int(asset_width * dpi_multiple * scale_factor)
        scaled_height = int(asset_height * dpi_multiple * scale_factor)
        asset_scaled = np.repeat(np.repeat(asset, dpi_multiple, axis=0), dpi_multiple, axis=1)
        asset_scaled = cv2.resize(asset_scaled, (scaled_width, scaled_height))
        
        cv2.imshow('asset', asset_scaled)
        res = cv2.matchTemplate(hex_img, asset_scaled, cv2.TM_CCOEFF_NORMED)
        
        loc = np.where(res >= THRESHOLD)
        for pt in zip(*loc[::-1]):
          print "ScreenInterpter: %s: %s" % (h, asset_file)
          cv2.rectangle(hex_img, pt,
                        (pt[0] + scaled_width, pt[1] + scaled_height),
                        (0,0,255), 2)
          cv2.imshow('tile', hex_img)
          cv2.waitKey(100)
          break
        
  

def GetStateFromScreenshot(screenshot):
  """Given a screenshot builds game state."""
  state = State()
  
