import os

from grid_lib import *
from hoplite_types import Board, TileType

# TODO: Keep the assets in RAM (there aren't many) to avoid reloading and
# scaling every time. Plenty of room for optimization in this file :)

def GetBoard(screenshot):
  TILE_WIDTH = 40
  TILE_HEIGHT = 37
  WHITE = (255, 255, 255)

  ALL_HEXES = [Hex(q, -q - s, s)
               for q in xrange(-4, 4 + 1)
               for s in xrange(-5, 5 + 1)
               if abs(-q - s) <= 5]

  screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
  screen_height, screen_width, screen_depth = screenshot.shape
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
    hex_img = GetImageByCorners(screenshot,
                                np.array(map(lambda p: p.Round(),
                                             polygon_corners(layout, h))))

    for asset_file, tile_type in asset_file_to_tile_type.iteritems():
      asset_path = os.path.join(ASSETS_BASE_PATH, asset_file)
      asset = cv2.imread(asset_path, cv2.IMREAD_GRAYSCALE)
      w, h = asset.shape[::-1]

      res = cv2.matchTemplate(screenshot, asset, cv2.TM_CCOEFF_NORMED)
      threshold = 0.7
      loc = np.where(res >= threshold)
      if loc:
        print "%s: %s" % (h, asset_file)
  

def GetStateFromScreenshot(screenshot):
  """Given a screenshot builds game state."""
  state = State()
  
