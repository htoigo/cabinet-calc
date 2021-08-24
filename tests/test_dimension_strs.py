# test_dimension_strs.py    -*- coding: utf-8 -*-


from cabinet_calc import dimension_strs as DS


class TestDimstr:
    def test_zero(self):
        assert DS.dimstr(0) == '0'

    def test_one_fourth(self):
        assert DS.dimstr(0.25) == '1/4'

    def test_one_eighth(self):
        assert DS.dimstr(0.125) == '1/8'

    def test_eleven_and_two_sevenths(self):
        # We need the `.' in `2./7' for this not to fail on Python 2.7.
        # Do we care about supporting Python 2.7, since it's EOL?
        assert DS.dimstr(11 + 2./7) == '11 5/16-'


class TestDimstrCol:
    def test_zero(self):
        assert DS.dimstr_col(0) == ' 0'

    def test_one(self):
        assert DS.dimstr_col(1) == ' 1'

    def test_nine(self):
        assert DS.dimstr_col(9) == ' 9'

    def test_one_fourth(self):
        assert DS.dimstr_col(0.25) == '1/4'

    def test_point_two_seven(self):
        assert DS.dimstr_col(0.27) == '1/4+'


class TestSDAlign:
    def test_four(self):
        assert DS.sdalign('4') == ' 4'

    def test_eight_and_three_fourths(self):
        assert DS.sdalign('8 3/4') == ' 8 3/4'

    def test_double_digit_mixed(self):
        assert DS.sdalign('22 3/8') == '22 3/8'

    def test_double_digit_whole(self):
        assert DS.sdalign('17') == '17'


# test_dimension_strs.py  ends here
