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


# text.py ends here
