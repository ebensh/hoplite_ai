from grid_lib import *
from enum import Enum
from itertools import groupby

class TileType(Enum):
    Bomb = 1
    Bow = 2
    Sword = 3
    Wizard = 4


ALL_HEXES = [Hex(q, -q - s, s)
             for q in xrange(-4, 4 + 1)
             for s in xrange(-5, 5 + 1)
             if abs(-q - s) <= 5]

class Board(object):
  _tiles = {}  # Map from Hex to TileType

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
