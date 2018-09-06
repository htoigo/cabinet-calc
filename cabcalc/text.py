# text.py    -*- coding: utf-8 -*-

__doc__ = """
CabCalc text module
~~~~~~~~~~~~~~~~~~~

This library module contains text-related functions and styles.

:copyright: (c) 2018 by Harry H. Toigo II.
:license: MIT, see LICENSE file for more details.
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
