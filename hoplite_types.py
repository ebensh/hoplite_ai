from collections import OrderedDict
from enum import Enum

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
  self._tiles = collections.OrderedDict()  

  # TODO: This is super hacky, replace with iteration over "y" coordinate.
  def __str__(self):
    # Any flat layout will do!
    layout = Layout(layout_flat, Point(50, 50), Point(1000, 1000))
    def annotate_hex(h): return (p.y, p.x, h)
    # TODO: Replace with proper group_by (y), order_by(x)
    for y, x, h in sorted([annotate_hex(h) for h in ALL_HEXES]):
      if y != cur_y:
        sys.out.print('\n')
        old_y
    
      
    def sorted_pts(h): return (hex_to_pixel(layout, h).y, hex_to_pixel(layout, h).x)
    print_order = sorted(ALL_HEXES, key=sorted_pts)

    for hex in print_order:
      print 
    hexes.sort(lambda h: hex_to_pixel
