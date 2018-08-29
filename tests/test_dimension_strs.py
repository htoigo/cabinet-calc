# test_dimension_strs.py    -*- coding: utf-8 -*-


import unittest
from dimension_strs import dimstr, dimstr_col, sdalign


class DimstrTest(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(dimstr(0), '0')

    def test_one_fourth(self):
        self.assertEqual(dimstr(0.25), '1/4')

    def test_one_eighth(self):
        self.assertEqual(dimstr(0.125), '1/8')

    def test_eleven_and_two_sevenths(self):
        self.assertEqual(dimstr(11 + 2/7), '11 5/16-')


class Dimstr_colTest(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(dimstr_col(0), ' 0')

    def test_one(self):
        self.assertEqual(dimstr_col(1), ' 1')

    def test_nine(self):
        self.assertEqual(dimstr_col(9), ' 9')

    def test_one_fourth(self):
        self.assertEqual(dimstr_col(0.25), '1/4')

    def test_point_two_seven(self):
        self.assertEqual(dimstr_col(0.27), '1/4+')


class SDAlignTest(unittest.TestCase):

    def test_four(self):
        self.assertEqual(sdalign('4'), ' 4')

    def test_eight_and_three_fourths(self):
        self.assertEqual(sdalign('8 3/4'), ' 8 3/4')

    def test_double_digit_mixed(self):
        self.assertEqual(sdalign('22 3/8'), '22 3/8')

    def test_double_digit_whole(self):
        self.assertEqual(sdalign('17'), '17')


if __name__ == '__main__':
    unittest.main()

# test_dimension_strs.py ends here
