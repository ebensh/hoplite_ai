from grid_lib import *
from enum import Enum
from itertools import groupby

class TileType(Enum):
    # Monsters (anything that can hurt you)
    BombMon = 1
    BombMonCooldown = 2
    Bomb = 3
    BowMon = 4
    SwordMon = 5
    WizardMon = 6
    WizardMonCooldown = 7

    # Special tiles - places to interact with
    Altar = 11
    UsedAltar = 12
    Fleece = 13
    LadderDown = 14
    Portal = 15
    
    # Ground
    Floor = 20
    Liquid = 21
    
    
    # Status tiles like health, jump, bash, etc.
    


class Board(dict):
  ALL_HEXES = [Hex(q, -q - s, s)
               for q in xrange(-4, 4 + 1)
               for s in xrange(-5, 5 + 1)
               if abs(-q - s) <= 5]

  def __str__(self):
    row_col_hex = []
    for h in ALL_HEXES:
      qoffset = qoffset_from_cube(EVEN, h)
      row_col_hex.append((qoffset.row, qoffset.col, h))
    row_col_hex.sort()
    board_str = ''
    for _, r_c_h_iter in groupby(row_col_hex, key=lambda (r, c, h): r):
      r_c_hs = list(r_c_h_iter)
      odd_cols_str = ' '.join(['1' for (r, c, h) in r_c_hs if c % 2 == 1])
      even_cols_str = ' '.join(['0' for (r, c, h) in r_c_hs if c % 2 == 0])
      if odd_cols_str: board_str += odd_cols_str.center(9) + '\n'
      if even_cols_str: board_str += even_cols_str.center(9) + '\n'
    return board_str
