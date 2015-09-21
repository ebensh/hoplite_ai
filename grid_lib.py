# Note that most of the concepts and code in this library come from
# http://www.redblobgames.com/grids/hexagons/ and
# http://www.redblobgames.com/grids/hexagons/implementation.html

import collections
import math

class Hex(collections.namedtuple('Hex', ['q', 'r', 's'])):
  _NEIGHBORS = [(1, 0, -1), (1, -1, 0), (0, -1, 1),
                (-1, 0, 1), (-1, 1, 0), (0, 1, -1)]
  _DIAGONAL_NEIGHBORS = [(2, -1, -1), (1, -2, 1), (-1, -1, 2),
                         (-2, 1, 1), (-1, 2, -1), (1, 1, -2)]
  
  @staticmethod
  def _Direction(direction): return Hex(*Hex._NEIGHBORS[direction])
  @staticmethod
  def _Diagonal(direction): return Hex(*Hex._DIAGONAL_NEIGHBORS[direction])
  @staticmethod
  def Lerp(a, b, t): return a + (b - a).Scale(t)
  @staticmethod
  def LineDraw(a, b):
    N = a.Distance(b)
    results = []
    step = 1.0 / max(N, 1)
    return [Hex.Lerp(a, b, step * i).Round() for i in xrange(0, N + 1)]
    
  def __add__(a, b): return Hex(a.q + b.q, a.r + b.r, a.s + b.s)
  def __sub__(a, b): return Hex(a.q - b.q, a.r - b.r, a.s - b.s)
  def Scale(self, k): return Hex(self.q * k, self.r * k, self.s * k)
  def Neighbor(self, direction): return self + Hex._Direction(direction)
  def DiagonalNeighbor(self, direction): return self + Hex._Diagonal(direction)
  def Length(self): return (abs(self.q) + abs(self.r) + abs(self.s)) // 2
  def Distance(self, b): return (self - b).Length()
  def Round(self):
    q = int(round(self.q))
    r = int(round(self.r))
    s = int(round(self.s))
    q_diff = abs(q - self.q)
    r_diff = abs(r - self.r)
    s_diff = abs(s - self.s)
    if q_diff > r_diff and q_diff > s_diff:
      q = -r - s
    else:
      if r_diff > s_diff:
        r = -q - s
      else:
        s = -q - r
    return Hex(q, r, s)

class Point(collections.namedtuple("Point", ["x", "y"])):
  def Round(self): return Point(int(round(self.x)), int(round(self.y)))

OffsetCoord = collections.namedtuple("OffsetCoord", ["col", "row"])

Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])

# === OffsetCoord methods
EVEN = 1
ODD = -1
def qoffset_from_cube(offset, h):
  col = h.q
  row = h.r + (h.q + offset * (h.q & 1)) // 2
  return OffsetCoord(col, row)

def qoffset_to_cube(offset, h):
  q = h.col
  r = h.row - (h.col + offset * (h.col & 1)) // 2
  s = -q - r
  return Hex(q, r, s)

def roffset_from_cube(offset, h):
  col = h.q + (h.r + offset * (h.r & 1)) // 2
  row = h.r
  return OffsetCoord(col, row)

def roffset_to_cube(offset, h):
  q = h.col - (h.row + offset * (h.row & 1)) // 2
  r = h.row
  s = -q - r
  return Hex(q, r, s)

# === Orientation and Layout methods
layout_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
layout_flat = Orientation(3.0 / 2.0, 0.0, math.sqrt(3.0) / 2.0, math.sqrt(3.0), 2.0 / 3.0, 0.0, -1.0 / 3.0, math.sqrt(3.0) / 3.0, 0.0)
def hex_to_pixel(layout, h):
  M = layout.orientation
  size = layout.size
  origin = layout.origin
  x = (M.f0 * h.q + M.f1 * h.r) * size.x
  y = (M.f2 * h.q + M.f3 * h.r) * size.y
  return Point(x + origin.x, y + origin.y)

def pixel_to_hex(layout, p):
  M = layout.orientation
  size = layout.size
  origin = layout.origin
  pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
  q = M.b0 * pt.x + M.b1 * pt.y
  r = M.b2 * pt.x + M.b3 * pt.y
  return Hex(q, r, -q - r)

def hex_corner_offset(layout, corner):
  M = layout.orientation
  size = layout.size
  angle = 2.0 * math.pi * (corner + M.start_angle) / 6
  return Point(size.x * math.cos(angle), size.y * math.sin(angle))

def polygon_corners(layout, h):
  corners = []
  center = hex_to_pixel(layout, h)
  for i in range(0, 6):
    offset = hex_corner_offset(layout, i)
    corners.append(Point(center.x + offset.x, center.y + offset.y))
  return corners

def polygon_edges(layout, h):
  corners = map(lambda p: p.Round(), polygon_corners(layout, h))
  return zip(corners, corners[1:] + [corners[0]])
