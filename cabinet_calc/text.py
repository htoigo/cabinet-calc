# text.py                             -*- coding: utf-8; -*-

"""The text module for Cabinet Calc.

Copyright © 2018-2021 Harry H. Toigo II, L33b0

This file is part of Cabinet Calc.

Cabinet Calc is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cabinet Calc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cabinet Calc.  If not, see <https://www.gnu.org/licenses/>.

This module provides fonts and paragraph styles for text layout and formatting
in reportlab PDF reports.
"""


__all__ = ['normal_style', 'rt_style', 'fixed_style', 'title_style',
           'wallwidth_style', 'heading_style']


from reportlab.rl_config import canvas_basefontname as _baseFontName
from reportlab.lib.fonts import tt2ps
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT


# Fonts

_baseFontNameB = tt2ps(_baseFontName, 1, 0)
_baseFontNameI = tt2ps(_baseFontName, 0, 1)
_baseFontNameBI = tt2ps(_baseFontName, 1, 1)


# Paragraph styles for text

# Normal text style
normal_style = ParagraphStyle(
    name='Normal',
    fontName=_baseFontName,
    fontSize=10,
    leading=12)

# Right-justified normaltext
rt_style = ParagraphStyle(
    name='RightText',
    parent=normal_style,
    alignment=TA_RIGHT)

# Fixed-width style for parts list so number columns line up
fixed_style = ParagraphStyle(
    name='FixedWidth',
    parent=normal_style,
    fontName='Courier',
    fontSize=10,
    leading=12)

# Title style (the Job Name used this style, as it is the title of the cutlist)
title_style = ParagraphStyle(
    name='Title',
    parent=normal_style,
    fontName=_baseFontNameB,
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=6)

# Total wall width style
wallwidth_style = ParagraphStyle(
    name='WallWidth',
    parent=normal_style,
    fontName=_baseFontNameB,
    fontSize=12,
    leading=14,
    spaceBefore=10,
    spaceAfter=5)

# Heading style for overview & parts list headings
heading_style = ParagraphStyle(
    name='Heading',
    parent=normal_style,
    fontName=_baseFontNameB,
    fontSize=12,
    leading=14,
    spaceBefore=12,
    spaceAfter=6)

# text.py  ends here
