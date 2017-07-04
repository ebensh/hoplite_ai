from grid_lib import *
from enum import Enum
from itertools import groupby

class Monster(Enum):
    Bomb = 1
    Bow = 2
    Sword = 3
    Wizard = 4


ALL_HEXES = [Hex(q, -q - s, s)
             for q in xrange(-4, 4 + 1)
             for s in xrange(-5, 5 + 1)
             if abs(-q - s) <= 5]

class Board(object):
  _tiles = []

  # TODO: This is super hacky, replace with iteration over "y" coordinate.
  def __str__(self):
    return ','.join([str(qoffset_from_cube(EVEN, h)) for h in ALL_HEXES])

      
    # Any flat layout will do!
    ret = ''
    layout = Layout(orientation_flat, Point(50, 50), Point(1000, 1000))
    def annotate_hex(h):
      p = hex_to_pixel(layout, h).Round()
      return (p.y, p.x, h)
    annotated_hexes = sorted(map(annotate_hex, ALL_HEXES))  # Sorted by y, x, h
    for y, row_hexes in groupby(annotated_hexes, lambda (y, x, h): y):
      print row_hexes
      row_len = sum(1 for _ in row_hexes)
      row = ' '.join(map(str, range(row_len)))
      #for h in xrange(len(row_hexes)):
      #  ret = ret + '1' + ' '
      ret += row + '\n'
    return ret
