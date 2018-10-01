# text.py        -*- coding: utf-8 -*-

# Module containing text related functions for Cabinet Calc.

# Copyright (C) 2018  Harry H. Toigo II

# This file is part of Cabinet Calc, the ....

# Cabinet Calc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Cabinet Calc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Cabinet Calc.  If not, see <https://www.gnu.org/licenses/>.

# To contact us:
#
# Email:       hhtpub@gmail.com
# Snail mail:  433 Buena Vista Ave. #310
#              Alameda CA  94501


"""CabCalc text module.

This library module contains text-related functions and styles.
"""

#__all__ = [max_cabinet_width, door_hinge_gap, cabinet_run, num_cabinets,
#           Run, Job]
__version__ = '0.1'
__author__ = 'Harry H. Toigo II'


import textwrap

from reportlab.rl_config import canvas_basefontname as _baseFontName
from reportlab.lib.fonts import tt2ps
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY


def wrap(lines, width=70):
    """Wrap lines longer than `width', returning a new list of lines."""
    result = []
    for line in lines:
        if len(line) <= width:
            result.append(line)
        else:
            # If line ends in a newline, preserve it (textwrap returns a list
            # of lines without final newlines).
            ls = textwrap.wrap(line, width)
            if line[-1] == '\n':
                # Remember, ls[-1] is a line (a string)
                ls[-1] = ls[-1] + '\n'
            result.extend(ls)
    return result


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
    fontName = _baseFontNameB,
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


# text.py ends here
