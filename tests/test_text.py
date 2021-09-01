# test_text.py    -*- coding: utf-8 -*-


from reportlab.rl_config import canvas_basefontname as _baseFontName
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

from cabinet_calc import text as T


def test_normal_style():
    assert T.normal_style.name == 'Normal'
    assert T.normal_style.fontName == _baseFontName
    assert T.normal_style.fontSize == 10
    assert T.normal_style.leading == 12
    assert T.normal_style.alignment == TA_LEFT


def test_rt_style():
    assert T.rt_style.name == 'RightText'
    assert T.rt_style.parent == T.normal_style
    assert T.rt_style.alignment == TA_RIGHT


# test_text.py  ends here
