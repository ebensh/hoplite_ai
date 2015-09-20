# Note that most of the concepts and code in this library come from
# http://www.redblobgames.com/grids/hexagons/ and
# http://www.redblobgames.com/grids/hexagons/implementation.html

import collections
import math

Hex = collections.namedtuple('Hex', ['q', 'r', 's'])
Point = collections.namedtuple("Point", ["x", "y"])

OffsetCoord = collections.namedtuple("OffsetCoord", ["col", "row"])

Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])


# === Hex related methods
def hex_add(a, b):
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)

def hex_subtract(a, b):
    return Hex(a.q - b.q, a.r - b.r, a.s - b.s)

def hex_scale(a, k):
    return Hex(a.q * k, a.r * k, a.s * k)

hex_directions = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1),
                  Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]
def hex_direction(direction):
    return hex_directions[direction]

def hex_neighbor(hex, direction):
    return hex_add(hex, hex_direction(direction))

hex_diagonals = [Hex(2, -1, -1), Hex(1, -2, 1), Hex(-1, -1, 2),
                 Hex(-2, 1, 1), Hex(-1, 2, -1), Hex(1, 1, -2)]
def hex_diagonal_neighbor(hex, direction):
    return hex_add(hex, hex_diagonals[direction])

def hex_length(hex):
    return (abs(hex.q) + abs(hex.r) + abs(hex.s)) // 2

def hex_distance(a, b):
    return hex_length(hex_subtract(a, b))

def hex_round(h):
    q = int(round(h.q))
    r = int(round(h.r))
    s = int(round(h.s))
    q_diff = abs(q - h.q)
    r_diff = abs(r - h.r)
    s_diff = abs(s - h.s)
    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    else:
        if r_diff > s_diff:
            r = -q - s
        else:
            s = -q - r
    return Hex(q, r, s)

def hex_lerp(a, b, t):
    return Hex(a.q + (b.q - a.q) * t, a.r + (b.r - a.r) * t, a.s + (b.s - a.s) * t)

def hex_linedraw(a, b):
    N = hex_distance(a, b)
    results = []
    step = 1.0 / max(N, 1)
    for i in range(0, N + 1):
        results.append(hex_round(hex_lerp(a, b, step * i)))
    return results

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
