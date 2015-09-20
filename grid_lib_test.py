import unittest
from grid_lib import *

class TestHexMethods(unittest.TestCase):
  def test_hex_arithmetic(self):
    self.assertEqual(Hex(4, -10, 6), hex_add(Hex(1, -3, 2), Hex(3, -7, 4)))
    self.assertEqual(Hex(-2, 4, -2), hex_subtract(Hex(1, -3, 2), Hex(3, -7, 4)))

  def test_hex_direction(self):
    self.assertEqual(Hex(0, -1, 1), hex_direction(2))

  def test_hex_neighbor(self):
    self.assertEqual(Hex(1, -3, 2), hex_neighbor(Hex(1, -2, 1), 2))

  def test_hex_diagonal(self):
    self.assertEqual(Hex(-1, -1, 2), hex_diagonal_neighbor(Hex(1, -2, 1), 3))

  def test_hex_distance(self):
    self.assertEqual(7, hex_distance(Hex(3, -7, 4), Hex(0, 0, 0)))

  def test_hex_round(self):
    a = Hex(0, 0, 0)
    b = Hex(1, -1, 0)
    c = Hex(0, -1, 1)
    self.assertEqual(Hex(5, -10, 5),
                     hex_round(hex_lerp(Hex(0, 0, 0), Hex(10, -20, 10), 0.5)))
    self.assertEqual(a, hex_round(hex_lerp(a, b, 0.499)))
    self.assertEqual(b, hex_round(hex_lerp(a, b, 0.501)))
    self.assertEqual(a, hex_round(Hex(a.q * 0.4 + b.q * 0.3 + c.q * 0.3,
                                      a.r * 0.4 + b.r * 0.3 + c.r * 0.3,
                                      a.s * 0.4 + b.s * 0.3 + c.s * 0.3)))
    self.assertEqual(c, hex_round(Hex(a.q * 0.3 + b.q * 0.3 + c.q * 0.4,
                                      a.r * 0.3 + b.r * 0.3 + c.r * 0.4,
                                      a.s * 0.3 + b.s * 0.3 + c.s * 0.4)))

  def test_hex_linedraw(self):
    self.assertEqual([Hex(0, 0, 0), Hex(0, -1, 1), Hex(0, -2, 2),
                      Hex(1, -3, 2), Hex(1, -4, 3), Hex(1, -5, 4)],
                     hex_linedraw(Hex(0, 0, 0), Hex(1, -5, 4)))

  def test_layout(self):
    h = Hex(3, 4, -7)
    flat = Layout(layout_flat, Point(10, 15), Point(35, 71))
    self.assertEqual(h, hex_round(pixel_to_hex(flat, hex_to_pixel(flat, h))))
    pointy = Layout(layout_pointy, Point(10, 15), Point(35, 71))
    self.assertEqual(h,
                     hex_round(pixel_to_hex(pointy, hex_to_pixel(pointy, h))))

  def test_conversion_roundtrip(self):
    a = Hex(3, 4, -7)
    b = OffsetCoord(1, -3)
    self.assertEqual(a, qoffset_to_cube(EVEN, qoffset_from_cube(EVEN, a)))
    # conversion_roundtrip even-q:
    self.assertEqual(b, qoffset_from_cube(EVEN, qoffset_to_cube(EVEN, b)))
    # conversion_roundtrip odd-q:
    self.assertEqual(a, qoffset_to_cube(ODD, qoffset_from_cube(ODD, a)))
    # conversion_roundtrip odd-q:
    self.assertEqual(b, qoffset_from_cube(ODD, qoffset_to_cube(ODD, b)))
    # conversion_roundtrip even-r:
    self.assertEqual(a, roffset_to_cube(EVEN, roffset_from_cube(EVEN, a)))
    # conversion_roundtrip even-r:
    self.assertEqual(b, roffset_from_cube(EVEN, roffset_to_cube(EVEN, b)))
    # conversion_roundtrip odd-r:
    self.assertEqual(a, roffset_to_cube(ODD, roffset_from_cube(ODD, a)))
    # conversion_roundtrip odd-r:
    self.assertEqual(b, roffset_from_cube(ODD, roffset_to_cube(ODD, b)))

  def test_offset_from_cube(self):
    # offset_from_cube even-q:
    self.assertEqual(OffsetCoord(1, 3), qoffset_from_cube(EVEN, Hex(1, 2, -3)))
    # offset_from_cube odd-q:
    self.assertEqual(OffsetCoord(1, 2), qoffset_from_cube(ODD, Hex(1, 2, -3)))

  def test_offset_to_cube(self):
    # offset_to_cube even-:
    self.assertEqual(Hex(1, 2, -3), qoffset_to_cube(EVEN, OffsetCoord(1, 3)))
    # offset_to_cube odd-q
    self.assertEqual(Hex(1, 2, -3), qoffset_to_cube(ODD, OffsetCoord(1, 2)))

if __name__ == '__main__':
  unittest.main()
